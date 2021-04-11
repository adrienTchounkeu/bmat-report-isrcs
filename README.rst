bmat-report-isrcs
==================

|Python-Versions| |pip-Verion| |Flask-Version| |Pandas-Version| |Numpy-Version|

``bmat-report-isrc`` is a Data Analysis REST API that consists of reading multiple CSV files which have to be 
analyzed, cleaned, and computed to bring out the Top 10k ISRCs.

--------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:
   
Technologies used and Why ?
---------------------------

To resolve this problem, we have used ``python``, ``flask``, ``pandas`` , and ``numpy``.

* ``python``: among the best programming language used for data analysis purposes.
* ``flask``: we are supposed to build a small REST API. Even though *Django* is a great python web framework, *flask* has been built for rapid development, provides API support, and has a lightweight codebase. Thereby, it best fits with the solution.
* ``pandas``: input CSV files contain millions of lines. *Pandas* is among the best modules used for data analysis along with DataFrames.
* ``numpy``: works along with *pandas*.


Installation
------------

To run my solution, you must have ``python`` and ``pip`` installed in your system. 

Download the project from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To clone my code, you run the command below in the CLI

.. code:: sh

    git clone "https://github.com/adrienTchounkeu/bmat-report-isrcs.git"

You can also download the project by clicking the link `bmat-report-isrcs <https://github.com/adrienTchounkeu/bmat-report-isrcs.git>`_


Install Dependencies
~~~~~~~~~~~~~~~~~~~~~

After downloading the code, Open the CLI in the root directory and execute the command :

.. code:: sh

   pip install -r requirements.txt


NB: *"requirements.txt is a file which contains all the project dependencies"*

All the project dependencies installed, run the command

.. code:: sh

   python app.py # on Windows

or 

.. code:: sh

   python3 app.py # on Linux

You can also run using the flask command 

.. code:: sh

   flask run

NB: *The first method is preferred*
    
    
Analyzing Data
--------------

While diving into the solution of this problem, we must, first of all, download the CSV files; Then, 
observe and come out with all relevant information, and finally, use that information 
to solve the problem. This step is one of the most important steps. We can also call it the
*Understanding Data* step. ALL the information gathered from the files : 

* files contain several millions of lines

* With data types, isrc files contain 01 column ``{isrc : string}`` whereas report files contain 05 columns ``[{date:string},{isrc:string},{title:string},{artists:string},{streams:long}]``

* Beware of duplicate isrc values in report files. 


Solving ``bmat-report-isrcs``
-----------------------------

Assumptions
~~~~~~~~~~~

To solve the problem, we did some hypothesis:

* data are well-formatted in the files
* user can only enter days in [10, 11, 12, 13, 14]
* number of plays of each isrc is the sum of all the streams of tracks with the same isrc (in case, it appears in multiple lines of report files)
* the first endpoint ``/report/<date>`` ingests the Top10k ISRCs in a file ``top10k_2020-11-{date}.csv`` contained in the folder named ``ingests`` 
* the second point ``/tracks`` lists all the tracks of **ingested data**. To filter by date and/or isrc, just call the endpoint with arguments ``/tracks?date={target_date}&isrc={target_isrc}``

Solution
~~~~~~~~~~~

To solve the problem, we use ``DataFrames`` and ``pandas as pd`` functions

* read in large CSV files with ``pd.read_csv`` in chunks(1000000)
* merge DataFrames with ``pd.merge``
* groupBy DataFrame with ``DataFrame.groupby`` returns *DataFrameGroupBy* object
* sum DataFrameGroupBy object with ``DataFrameGroupBy.sum``
* concat dataFrames with ``pd.concat``
* sort values with ``DataFrame.sort_values``
* write in CSV file with ``DataFrame.to_csv``

Use Case
~~~~~~~~

Below are the results when calling my endpoints: ``/report/<date>`` and ``/tracks``

* After running the server with the command ``python app.py``, the server will be available under the port *5000*. Thereby, ``127.0.0.1:5000``
* To test the first endpoint, you send a get request to the server ``127.0.0.1:5000/report/10``. You can track the process on the server command line. In the end, a file entitled ``ingests/top10k_2020-11-10.csv`` will be created under the folder **ingests** and the server will return all the information
* To test the second endpoint, you send a get request to the server ``127.0.0.1:5000/tracks``. The server will return all the information

NB: *You must have a high quality internet connexion to speed up the download files step*

Tests
~~~~~

*No unit tests* have been done to test the endpoints



Further perspectives
---------------------

Limitations & Optimizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Even though my code is solving the problem, I have some performance and resources used issues. 
To optimize my solution, I think

* implement parallelization : optimization of read CSV files
* resizing DataFrames before huge memory cost computations
* manually freeing up the memory of unused ongoing DataFrames


Real-life Adaptation
~~~~~~~~~~~~~~~~~~~~

Assuming that we have files coming from more than one country, streams count
of more than one DSP, we will have major problems:

* storing ingested data
* searching on huge amounts of data
* computing on huge amounts of data

To solve this problem, we need to use a near real-time search engine tool : *ElasticSearch* |ElasticSearch-Version|, 
for instance. I would then store ingested data in *ElasticSearch*, query and retrieve relevant information. 

After installing ElasticSearch on my computer, my API will easily communicate with *ElasticSearch*
through an *ElasticSearch Client* written in Python. My REST API will just perform storing, querying and retrieving functions.



.. |Python-Versions| image:: https://img.shields.io/pypi/pyversions/pip?logo=python&logoColor=white   :alt: Python Version 
.. |pip-Verion| image:: https://img.shields.io/pypi/v/pip?label=pip&logoColor=white   :alt: pip  Version
.. |Flask-Version| image:: https://img.shields.io/pypi/v/flask?label=flask&logo=flask&logoColor=white   :alt: flask Version
.. |Numpy-Version| image:: https://img.shields.io/pypi/v/numpy?label=numpy&logo=numpy&logoColor=white   :alt: numpy Version
.. |Pandas-Version| image:: https://img.shields.io/pypi/v/pandas?label=pandas&logo=pandas&logoColor=white   :alt: pandas Version
.. |ElasticSearch-Version| image:: https://img.shields.io/badge/elasticsearch-3.12-blue   :alt: elastic Search
