# Data Warehouse (Udacity Data Engineering Nanodegree Project `Data Warehouse`)

## Description of this project
Load song play events of a mobile application and register to RedShift database.

## ETL process
ETL consists from two processes.

- load song and user's song play data to temporary database.
- save them to database

## How to set up

```shell
# pull docker images (if not exists on local machine) and run necessary process
docker-compose up --build -d
# create tables
docker-compose exec app python3 create_tables.py
# run ETL
docker-compose exec app python3 etl.py
```
