quandl-py: Simple Quandl Python Wrapper
=======================================
Simple Python wrapper to return Quandl Api information as Pandas DataFrames 

Simple Example
==============
This example shows all of the potential options for this wrapper

```python

import quandl-py as qp
qp.get('YAHOO', 'AAPL', api_key='xxxxx' start_date='2010-01-01', 
        end_date='2015-09-30', order='dsc', rows=10, collapse='monthly', 
        transform='rdiff',  column_index=3)

```

This will return:

```
           Date               Low
0          2015-09-30         -0.031161
1          2015-08-31         -0.073691
2          2015-07-31         -0.031635
3          2015-06-30         -0.038799
4          2015-05-31          0.042703
5          2015-04-30          0.001769
6          2015-03-31         -0.030256
7          2015-02-28          0.097475
8          2015-01-31          0.060249
9          2014-12-31         -0.066413

```           

In the above example, setting the dataset ('YAHOO'), and
ticker('AAPL') are required.  All other parameters are optional.  

Input Options
=============
``api_key`` API key obtained from quandl

``start_date`` and ``end_date`` should be specified in yyyy-mm-dd format

``order`` ['asc', 'dsc']

``rows`` an integer representing the numbers of rows to return

``collapse`` ['daily', 'weekly', 'monthly', 'quarterly', 'annual']

``transform`` ['diff', 'rdiff', 'cumul']

``column_index`` an integer representing the column to return

Installation
============
    pip install quandlpy

