import pandas as pd
from flask import Flask, request
import numpy as np

app = Flask(__name__)
pd.set_option('display.max_columns', None)


@app.route('/')
def login():
    return "Hello World"


@app.route('/report/<date>')
def ingest_data(date):
    """

    :param date:
    :return: download and store data of the usages of Top 10k ISRC that are on the isrcs file sorted by number of streams
    """

    # create variables for filenames
    report_filename_relativePath = "files/report_2020-11-{}.csv.gz".format(date)
    isrcs_filename_relativePath = "files/isrcs_2020-11-{}.csv.gz".format(date)
    result_filename_relativePath = "ingests/top10k_2020-11-{}.csv".format(date)

    # read the isrcs' csv file, extract all the lines and shape in a panda DataFrame
    # chunksize is to speed up
    with pd.read_csv(isrcs_filename_relativePath, encoding="utf-8", chunksize=1000000) as reader:
        list_isrcDF = pd.concat([chunk for chunk in reader])
        reader.close()

    print("isrcs loaded")

    # set name and the data type of the columns of the report file
    reports_columns = ['date', 'isrc', 'title', 'artists', 'streams']
    dtypes = {'date': str, 'isrc': str, 'title': str, 'artists': str, 'streams': np.int64}

    # read the report's file, extract all the lines and put in a panda DataFrame
    # chunksize is to speed up
    # python engine correct some errors : mostly parsing Errors
    with pd.read_csv(report_filename_relativePath, encoding="utf-8", delimiter="\\t", header=0,
                     chunksize=1000000, dtype=dtypes, names=reports_columns, engine='python') as reader:
        reports_frame = pd.concat([chunk for chunk in reader])
        reader.close()

    print("reports loaded")

    # inner join the two DataFrames -> filter the report's DataFrame to keep ISRCs that are in the ircs' file
    # the result DataFrame contains lines with same ircs -> group by isrc and prevent the default sort
    merged_groupedDataFrame = pd.merge(list_isrcDF, reports_frame, how="inner", on="isrc").groupby(["isrc"], sort=False)

    print("Merge & GroupBy performed")

    # sum the streams of each group of the merged_groupedDataFrame, removing the other columns

    print("Initialize aggregation -- sum duplicate values of isrc by adding streams")

    summedDataFrame = merged_groupedDataFrame.sum()

    print("Sum performed")

    # re-adding the other columns
    otherColumns = merged_groupedDataFrame[['date', 'artists', 'title']].first()

    # concatenate the two DataFrames : summedDataFrame & otherColumns
    # rearrange the DataFrame : date, isrc, title, artists, streams(total streams)
    fullDataFrame = pd.concat([otherColumns, summedDataFrame], 1).reset_index()
    fullDataFrame[['isrc', 'date']] = fullDataFrame[['date', 'isrc']]

    print("concatenate Performed")

    # sort the fullDataFrame to get the Top 10k - inplace sorting is faster

    print("Begin Sort")

    fullDataFrame.sort_values(by=['streams'], ascending=False, kind='mergesort', inplace=True)

    print("End Sort")

    # retrieve the Top 10k and store in the ingest folder under the name : top10k_2020-11-{date}.csv
    fullDataFrame[:10000].to_csv(result_filename_relativePath, index=False, sep="\t")

    return date


@app.route('/tracks')
def tracks_list():
    """

    :return: list of the tracks sorted by streams
    """

    return request.args
    reports_columns = ['date', 'isrc', 'title', 'artists', 'streams']
    dtype = {'date': str, 'isrc': str, 'title': str, 'artists': str}
    tracks_list = []
    for index in range(10, 15):
        filename_relativePath = "./ingests/2020-11-{}".format(index)
        with pd.read_csv(filename_relativePath, encoding="utf-8", delimiter="\t",
                         usecols=reports_columns, chunksize=1000000, dtype=dtype) as reader:
            tracks_list.append(pd.concat([chunk for chunk in reader]))
            reader.close()
    tracks_list = pd.concat(tracks_list)  # convert to DataFrame


if __name__ == "__main__":
    app.run('127.0.0.1')
