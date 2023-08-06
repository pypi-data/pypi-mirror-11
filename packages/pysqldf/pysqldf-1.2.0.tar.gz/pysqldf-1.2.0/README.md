# pysqldf

[![Build Status](https://travis-ci.org/airtoxin/pysqldf.svg)](https://travis-ci.org/airtoxin/pysqldf)
[![PyPI Version](https://img.shields.io/pypi/v/pysqldf.svg)](https://pypi.python.org/pypi/pysqldf)
[![PyPI Monthly Downloads](https://img.shields.io/pypi/dm/pysqldf.svg)](https://pypi.python.org/pypi/pysqldf)
[![PyPI License](https://img.shields.io/pypi/l/pysqldf.svg)](https://pypi.python.org/pypi/pysqldf)

`pysqldf` allows you to query `pandas` DataFrames using SQL syntax.
It works similarly to `sqldf` in R.
`pysqldf` seeks to provide a more familiar way of manipulating and cleaning data for people new to Python or `pandas`.

## Installation

`$ pip install pysqldf`

## Basics

The main class in pysqldf is `SQLDF`. `SQLDF` accepts 1 enviroment variable sets or more parametrs in constructor.
   - an set of session/environment variables (dictionary of valiables, `locals()` or `globals()`)
   - temporary file type
   - user defined functions
   - user defined aggregate functions

`pysqldf` uses [SQLite syntax](http://www.sqlite.org/lang.html).
Any convertable data to `pandas` DataFrames will be automatically detected by `pysqldf`.
You can query them as you would any regular SQL table.


```python
$ python
>>> from pysqldf import SQLDF, load_meat, load_births
>>> sqldf = SQLDF(globals())
>>> meat = load_meat()
>>> births = load_births()
>>> print sqldf.execute("SELECT * FROM meat LIMIT 10;").head()
                  date  beef  veal  pork  lamb_and_mutton broilers other_chicken turkey
0  1944-01-01 00:00:00   751    85  1280               89     None          None   None
1  1944-02-01 00:00:00   713    77  1169               72     None          None   None
2  1944-03-01 00:00:00   741    90  1128               75     None          None   None
3  1944-04-01 00:00:00   650    89   978               66     None          None   None
4  1944-05-01 00:00:00   681   106  1029               78     None          None   None

>>> q = "SELECT m.date, m.beef, b.births FROM meat m INNER JOIN births b ON m.date = b.date;"
>>> print sqldf.execute(q).head()
                    date    beef  births
403  2012-07-01 00:00:00  2200.8  368450
404  2012-08-01 00:00:00  2367.5  359554
405  2012-09-01 00:00:00  2016.0  361922
406  2012-10-01 00:00:00  2343.7  347625
407  2012-11-01 00:00:00  2206.6  320195

>>> q = "SELECT strftime('%Y', date) AS year, SUM(beef) AS beef_total FROM meat GROUP BY year;"
>>> print sqldf.execute(q).head()
   year  beef_total
0  1944        8801
1  1945        9936
2  1946        9010
3  1947       10096
4  1948        8766
```

user defined functions and user defined aggregate functions also supported.

```python
$ python
>>> from pysqldf import SQLDF, load_iris
>>> import math
>>> import numpy
>>> ceil = lambda x: math.ceil(x)
>>> udfs = { "ceil": lambda x: math.ceil(x) }
>>> udafs = { "variance": lambda values: numpy.var(values) }
>>> # or you can also define aggregation function as class
>>> # class variance(object):
... #     def __init__(self):
... #         self.a = []
... #     def step(self, x):
... #         self.a.append(x)
... #     def finalize(self):
... #         return numpy.var(self.a)
...
>>> # udafs={ "variance": variance }
>>> iris = load_iris()
>>> sqldf = SQLDF(globals(), udfs=udfs, udafs=udafs)
>>> sqldf.execute("""
    SELECT
        ceil(sepal_length) AS sepal_length,
        ceil(sepal_width) AS sepal_width,
        ceil(petal_length) AS petal_length,
        ceil(petal_width) AS petal_width,
        species
    FROM iris;
    """).head()
   sepal_length  sepal_width  petal_length  petal_width      species
0             6            4             2            1  Iris-setosa
1             5            3             2            1  Iris-setosa
2             5            4             2            1  Iris-setosa
3             5            4             2            1  Iris-setosa
4             5            4             2            1  Iris-setosa
>>> sqldf.execute("SELECT species, variance(sepal_width) AS var FROM iris GROUP BY species;")
           species       var
0      Iris-setosa  0.142276
1  Iris-versicolor  0.096500
2   Iris-virginica  0.101924
```

## Documents

### `SQLDF(env, inmemory=True, udfs={}, udafs={})`

`env`: variable mapping dictionary of sql executed enviroment. key is sql variable name and value is your program variable. `locals()` or `globals()` is used for simple assign.

`inmemory`: sqlite db option.

`udfs`: dictionary of user defined functions. dictionary key is function name, dictionary value is function. see [sqlite3 document](https://docs.python.org/2.7/library/sqlite3.html#sqlite3.Connection.create_function)

`udafs`: dictionary of user defined aggregate functions. dictionary key is function name, dictionary value is aggregate function or class. If value is function, function gets one argument that is list of column values and it should return aggregated a value. Another case(value is class), see [sqlite3 document](https://docs.python.org/2.7/library/sqlite3.html#sqlite3.Connection.create_aggregate).

### `load_iris()`, `load_meat()`, `load_births()`

load example DataFrame data.

+ iris: [data description](https://archive.ics.uci.edu/ml/datasets/Iris)
+ meat: [data description](http://www.ers.usda.gov/data-products/livestock-meat-domestic-data.aspx)
+ births: [data description](http://data.un.org/Data.aspx?d=POP&f=tableCode:55)
