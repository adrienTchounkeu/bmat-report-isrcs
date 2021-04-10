import pandas as pd
from flask import Flask

app = Flask(__name__)
pd.set_option('display.max_columns', None)


@app.route('/')
def login():
    return "Hello World"


@app.route('/report/<date>')
def ingest_data(date):
    """

    :param date:
    :return: download and store data of the Top 10k ISRC that are on the isrcs file sorted by number of streams
    """
    report_filename_relativePath = "./files/report_2020-11-{}.csv.gz".format(date)
    isrcs_filename_relativePath = "./files/isrcs_2020-11-{}.csv.gz".format(date)
    with pd.read_csv(isrcs_filename_relativePath, encoding="utf-8", chunksize=500000) as reader:
        list_isrcDF = pd.concat([chunk for chunk in reader])
        reader.close()
    print("isrcs loaded")

    reports_columns = ['date', 'isrc', 'title', 'artists', 'streams']
    dtype = {'date': str, 'isrc': str, 'title': str, 'artists': str}
    with pd.read_csv(report_filename_relativePath, encoding="utf-8", delimiter="\t",
                     usecols=reports_columns, chunksize=1000000, dtype=dtype) as reader:
        reports_frame = pd.concat([chunk for chunk in reader])
        reader.close()
    print("reports loaded")
    intPd = pd.merge(list_isrcDF, reports_frame, how="inner", on="isrc").groupby(["isrc"])
    print("Merge performed")
    del list_isrcDF
    del reports_frame
    print("Initialize aggregation -- sum duplicate values of isrc by adding streams")
    j = intPd.sum()
    print("Sum performed")
    g = intPd[['date', 'artists', 'title']].first()
    intPd = pd.concat([g, j], 1).reset_index()
    print("concat OK")
    del g
    del j
    print("Begin Sort")
    intPd.sort_values(by=['streams'], ascending=False, kind='mergesort', inplace=True)
    print("End Sort")
    intPd[:10000].to_csv("files/results.csv", index=False, sep=";")
    return date


@app.route('/tracks')
def tracks_list():
    pass


if __name__ == "__main__":
    app.run('127.0.0.1')
