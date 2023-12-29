-- to be deployed as a Native App with: snowsql -c my_conn -f deploy.sql

-- create app package
DROP APPLICATION IF EXISTS ip2location_app CASCADE;
DROP APPLICATION PACKAGE IF EXISTS ip2location_package;
CREATE APPLICATION PACKAGE ip2location_package;
USE APPLICATION PACKAGE ip2location_package;
SHOW APPLICATION PACKAGES;

DROP SCHEMA public;
CREATE SCHEMA private;
GRANT USAGE ON SCHEMA private TO SHARE
   IN APPLICATION PACKAGE ip2location_package;

-- upload files in new stage
CREATE FILE FORMAT location_csv
  SKIP_HEADER = 0
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  COMPRESSION = AUTO;
CREATE STAGE stage
  FILE_FORMAT = location_csv;

PUT file://.\manifest.yml @stage overwrite=true auto_compress=false;
PUT file://.\script.sql @stage overwrite=true auto_compress=false;
PUT file://.\app.py @stage overwrite=true auto_compress=false;
PUT file://.\data\ip2location-small.csv @stage/data overwrite=true auto_compress=false;
LIST @stage;

-- upload CSV raw data into a table
CREATE TABLE litedb11 (
  ip_from INT,
  ip_to INT,
  country_code char(2),
  country_name varchar(64),
  region_name varchar(128),
  city_name varchar(128),
  latitude DOUBLE,
  longitude DOUBLE,
  zip_code varchar(30),
  time_zone varchar(8)
);
GRANT SELECT ON TABLE litedb11 TO SHARE
   IN APPLICATION PACKAGE ip2location_package;
COPY INTO litedb11 FROM @stage/data;
SELECT count(*) FROM litedb11;
SELECT * FROM litedb11 LIMIT 10;

-- set app version
ALTER APPLICATION PACKAGE ip2location_package
  ADD VERSION v1_0
  USING '@stage'
  LABEL = 'IP2Location v1.0';
  
ALTER APPLICATION PACKAGE ip2location_package
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = v1_0
  PATCH = 0;

-- create app
CREATE APPLICATION ip2location_app
    FROM APPLICATION PACKAGE ip2location_package
    USING '@stage'
    DEBUG_MODE = true;
SHOW APPLICATIONS;
