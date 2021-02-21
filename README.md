# Data Warehouse (Udacity Data Engineering Nanodegree Project `Data Warehouse`)

## Description of this project
Load song play events of a mobile application and register to Redshift database.

## Goal of this project
This project's goal is analyze data to find what attribute of users often play songs, what songs or artists are played often and when songs are often played.

## Description of process

First, script `create_tables.py` creates staging, dimension and fact tables.
Then, script `etl.py` loads json data from S3 to Redshift staging table.
Finally, it loads from staging table to dimension and fact table by using `INSERT INTO ... SELECT ...` syntax.

### Staging tables

- `log_data`
  provide event data recorded in json file under `log_data` directory

- `song_data`
  provide song and artist data recorded in json file under `song_data` directory
  
### Dimension tables

- `songs`
  provide song data which were played

- `artists`
  provide artist data whose songs were played

- `users`
  provide user data who played songs

- `time`
  provide time data when users played songs


### Fact table

- `songplays`
  provide event data which describe who, when and what songs are played

Those tables are designed using STAR schema, which can easily analyze various aspects.
I assumed we can specify artists and songs of event data by its name and title.

## How to set up

```shell
# pull docker images and build docker images
docker-compose up --build -d
# create tables
docker-compose exec app python3 create_tables.py
# run ETL
docker-compose exec app python3 etl.py
```

## Sample of analysis

### Whose song was played most frequently ?

**Query:**
```
SELECT sp.artist_id, a.name, COUNT(sp.artist_id)
FROM songplays sp
INNER JOIN artists a on sp.artist_id = a.artist_id
GROUP BY sp.artist_id, a.name
ORDER BY 3 DESC
LIMIT 5
```

**Result:**

artist_id | name | cnt
---------- | ------ | -----
AR5E44Z1187B9A1D74 | Dwight Yoakam | 37
ARD46C811C8A414F3F | Kid Cudi / Kanye West / Common | 10
ARD46C811C8A414F3F | Kid Cudi | 10
AR37SX11187FB3E164 | Ron Carter | 9
AR5EYTL1187B98EDA0 | Lonnie Gordon | 9

### What songs were played most frequently on the first week of November?

**Query:**
```
SELECT sp.song_id, s.title, COUNT(sp.song_id) AS cnt
FROM songplays sp
INNER JOIN songs s on sp.song_id = s.song_id
INNER JOIN time t ON sp.start_time = t.start_time
WHERE t.start_time BETWEEN '2018-11-01 00:00:00' AND '2018-11-08 00:00:00'
GROUP BY sp.song_id, s.title
ORDER BY 3 DESC
LIMIT 5
```

song_id | title | cnt
---------- | ------ | -----
SOBONKR12A58A7A7E0 | You're The One | 8
SONTFNG12A8C13FF69 | If I Ain't Got You | 3
SOHTKMO12AB01843B0 | Catch You Baby (Steve Pitron & Max Sanna Radio Edit) | 3
SOULTKQ12AB018A183 | Nothin' On You [feat. Bruno Mars] (Album Version) | 2
SOLZOBD12AB0185720 | Hey Daddy (Daddy's Home) | 2

## File descriptions

- `create_tables.py`
  creates necessary tables

- `docker-compose.yml`
  preference file to organize docker images

- `Dockerfile`
  provides docker image template

- `dwh.cfg`
  parameter file for paths of json data, IAM Role and redshift connection
  
- `etl.py`
  defines etl processes
  
- `init.sh`
  script launched initially when docker image started

- `README.md`
  describes about this project

- `requirements.txt`
  defines libraries need to execute processes
  
- `sql_queries.py`
  defines SQLs need to execute
