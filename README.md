# Introduction

Read a csv input file and save it into a sqlite3 db by python

## Prerequisites
1. I tested it in ubuntu 18.0.4 LTS
2. python3

## Run
Assume you have installed ubuntu 18.0.4 LTS and python3

```sh
$ git clone https://github.com/gachen95/csv2sqlite.git
$ cd csv2sqlite
$ chmod +x csv2sqlite.py
$ ./csv2sqlite.py my.csv
```

### Configuration
All the configurations are in file convert.ini.
```
[CSV]
delimiter = ,
quotechar = |

[SQLITE3]
dbname = csv.sqlite3
tablename = csv
```

### Possible running issue
Assume python3 is installed as /usr/bin/python3.   
If not, please change below line in csv2sqlite3.py to specify it.

```sh
#!/usr/bin/python3
```

## Improvement
1. Now assume the 1st row of csv file is the header
2. Now only support INTEGER and TEXT data type from csv. Need to support more types like DATE, REAL in sqllite
