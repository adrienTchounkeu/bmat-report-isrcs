bmat-report-isrcs
==================

|Python-Versions| |pip-Verion| |Flask-Version| |Pandas-Version| |Numpy-Version|

``bmat-report-isrc`` is a Data Analysis REST API which consists of reading multiple CSV files that have to be 
analyzed, cleaned and computed to bring out the Top 10k ISRCs.

--------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:
   
Technologies used and Why ?
---------------------------

To resolve this problem, we have used ``python``, ``flask``, ``pandas`` , and ``numpy``.

* ``python``: among the most-widely programming language used for data analysis purposes
* ``flask``: we are supposed to build a small REST API. Even though *Django* is a great python web-framework, *flask* has been built for rapid development, provides support for API and has a lightweight codebase. Thereby, it best fits with the solution.
* ``pandas``: input CSV files contain millions of lines. *Pandas* is among the most-widely modules used for data analysis.
* ``numpy``: works along with *pandas*.


Installation
------------

To run my solution, you must have ``python`` and ``pip`` installed in your system. 

Clone the project from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To clone my code, you run the command below in the CLI

.. code:: sh

    git clone "https://github.com/adrienTchounkeu/bmat-report-isrcs.git"

You can also download the project by clinking the link `bmat-report-isrcs <https://github.com/adrienTchounkeu/bmat-report-isrcs.git>`_


Install Dependencies
~~~~~~~~~~~~~~~~~~~~~

After downloading the code, Open the CLI in the root directory and execute the command :

.. code:: sh

   pip install -r requirements.txt


NB: *"requirements.txt is a file which contains all the project dependencies"*

All the project dependencies installed, run the command

.. code:: sh

   python app.py # on windows

or 

.. code:: sh

   python3 app.py # on linux

You can also run using the flask command 

.. code:: sh

   flask run

NB: *The first method is preferred*
    
    
Analyzing Data
--------------

While diving into the solution of this problem, we must, first of all, download the CSV files; Then, 
observe and come out with all relevant information, and finally, use those information 
to solve the problem. This step is one of the most important steps. We can also call it the
*Understanding Data* step. ALL the information gather from the files : 

* files contain several millions of lines

* With data types, isrc files contain 01 column ``{isrc : string}`` whereas report files contain 05 columns ``[{date:string},{isrc:string},{title:string},{artists:string},{streams:long}]``

* Beware of duplicate isrc values for two different lines. 


Solving ``bmat-report-isrcs``
-----------------------------

Assumptions
~~~~~~~~~~~

To solve the problem, we did some hypothesis:

* data are well formatted in the files
* user can only enter dates in [10, 11, 12, 13, 14]
* number of plays of each isrc in the isrc file is the sum of all the streams of tracks with the same isrc (in case, it appears in multiple lines of report files)
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

Tests
~~~~~

*No tests* have been done to test the endpoints









Further perspectives
---------------------



Conclusion
-----------









.. |Python-Versions| image:: https://img.shields.io/pypi/pyversions/pip?logo=python&logoColor=white   :alt: Python Version 
.. |pip-Verion| image:: https://img.shields.io/pypi/v/pip?label=pip&logoColor=white   :alt: pip  Version
.. |Flask-Version| image:: https://img.shields.io/pypi/v/flask?label=flask&logo=flask&logoColor=white   :alt: flask Version
.. |Numpy-Version| image:: https://img.shields.io/pypi/v/numpy?label=numpy&logo=numpy&logoColor=white   :alt: numpy Version
.. |Pandas-Version| image:: https://img.shields.io/pypi/v/pandas?label=pandas&logo=pandas&logoColor=white   :alt: pandas Version
