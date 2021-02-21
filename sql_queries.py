import configparser


# CONFIG
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

DWH_ROLE_ARN = config.get('IAM_ROLE', 'ARN')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS log_data"
staging_songs_table_drop = "DROP TABLE IF EXISTS song_data"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = ("""
    CREATE TABLE IF NOT EXISTS log_data (
        artist TEXT,
        auth TEXT,
        firstname TEXT,
        gender TEXT,
        iteminsession INT,
        lastname TEXT,
        length DECIMAL,
        level TEXT,
        location TEXT,
        method TEXT,
        page TEXT,
        registration BIGINT,
        sessionid BIGINT,
        song TEXT,
        status INT,
        ts BIGINT,
        useragent TEXT,
        userid TEXT
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS song_data (
        artist_id TEXT,
        artist_latitude DECIMAL,
        artist_location TEXT,
        artist_longitude DECIMAL,
        artist_name TEXT,
        duration DECIMAL,
        num_songs INT,
        song_id TEXT,
        title TEXT,
        year INT
    )
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id BIGINT NOT NULL IDENTITY(0, 1) distkey,
        start_time DATETIME NOT NULL sortkey,
        user_id TEXT,
        level TEXT,
        song_id TEXT,
        artist_id TEXT,
        session_id BIGINT,
        location TEXT,
        user_agent TEXT
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        level TEXT NOT NULL
    )
    diststyle all
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id TEXT NOT NULL,
        title TEXT NOT NULL,
        artist_id TEXT NOT NULL,
        year INT,
        duration DECIMAL
    )
    diststyle all
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id TEXT NOT NULL,
        name TEXT NOT NULL,
        location TEXT,
        lattitude DECIMAL,
        longitude DECIMAL
    )
    diststyle all
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time DATETIME NOT NULL sortkey,
        hour INT NOT NULL,
        day INT NOT NULL,
        week INT NOT NULL,
        month INT NOT NULL,
        year INT NOT NULL,
        weekday INT NOT NULL
    )
    diststyle all
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY {} FROM 's3://udacity-dend/{}' 
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2'
    FORMAT AS JSON 'auto ignorecase';
""").format('log_data', 'log_data', DWH_ROLE_ARN)

staging_songs_copy = ("""
    COPY {} FROM 's3://udacity-dend/{}' 
    CREDENTIALS 'aws_iam_role={}'
    REGION 'us-west-2'
    FORMAT AS JSON 'auto ignorecase';
""").format('song_data', 'song_data', DWH_ROLE_ARN)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (
        start_time,
        user_id,
        level,
        song_id,
        artist_id,
        session_id,
        location,
        user_agent
    )
    SELECT
        TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' AS start_time,
        userid,
        level,
        s.song_id,
        a.artist_id,
        sessionid,
        a.location,
        useragent
    FROM log_data ld
    LEFT JOIN songs s ON ld.song = s.title
    LEFT JOIN artists a ON ld.artist = a.name
""")

user_table_insert = ("""
    INSERT INTO users (
        user_id,
        first_name,
        last_name,
        gender,
        level
    )
    SELECT
        userid,
        firstname,
        lastname,
        gender,
        level
    FROM log_data
    WHERE firstname IS NOT NULL AND lastname IS NOT NULL
    GROUP BY
        userid,
        firstname,
        lastname,
        gender,
        level
""")

song_table_insert = ("""
    INSERT INTO songs (
        song_id,
        title,
        artist_id,
        year,
        duration
    )
    SELECT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM song_data
    GROUP BY
        song_id,
        title,
        artist_id,
        year,
        duration
""")

artist_table_insert = ("""
    INSERT INTO artists (
        artist_id,
        name,
        location,
        lattitude,
        longitude
    )
    SELECT
        artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM song_data
    GROUP BY
        artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
""")

time_table_insert = ("""
    INSERT INTO time (
        start_time,
        hour,
        day,
        week,
        month,
        year,
        weekday
    )
    WITH timestamps AS (
    SELECT
        TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' AS start_time
    FROM log_data
    GROUP BY
        ts
    )
    SELECT
        start_time,
        extract(hour from start_time),
        extract(day from start_time),
        extract(week from start_time),
        extract(month from start_time),
        extract(year from start_time),
        extract(dow from start_time)
    FROM timestamps
""")

# QUERY LISTS

create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]

drop_table_queries = [
    staging_events_table_drop,
    staging_songs_table_drop,
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]

copy_table_queries = [
    staging_events_copy,
    staging_songs_copy,
]

insert_table_queries = [
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
    songplay_table_insert,
]
