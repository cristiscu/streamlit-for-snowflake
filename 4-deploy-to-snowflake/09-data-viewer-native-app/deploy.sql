!set variable_substitution=true

-- create app package
DROP APPLICATION IF EXISTS hierarchical_data_app CASCADE;
DROP APPLICATION PACKAGE IF EXISTS hierarchical_data_package;
CREATE APPLICATION PACKAGE hierarchical_data_package;
USE APPLICATION PACKAGE hierarchical_data_package;
SHOW APPLICATION PACKAGES;

DROP SCHEMA public;
CREATE SCHEMA private;
GRANT USAGE ON SCHEMA private TO SHARE
   IN APPLICATION PACKAGE hierarchical_data_package;

-- upload files in new stage
CREATE STAGE stage
    directory = (enable=true)
    file_format = (type=CSV field_delimiter=None record_delimiter=None);

!define CRT_DIR=file://C:\Projects\streamlit-for-snowflake-test\data-native-app
PUT &CRT_DIR\app.py @stage overwrite=true auto_compress=false;
PUT &CRT_DIR\environment.yml @stage overwrite=true auto_compress=false;
PUT &CRT_DIR\modules\*.py @stage/modules overwrite=true auto_compress=false;
PUT &CRT_DIR\manifest.yml @stage overwrite=true auto_compress=false;
PUT &CRT_DIR\readme.md @stage overwrite=true auto_compress=false;
PUT &CRT_DIR\script.sql @stage overwrite=true auto_compress=false;
PUT &CRT_DIR\data\employees-raw.csv @stage/data overwrite=true auto_compress=false;
LIST @stage;

-- upload CSV raw data into EMPLOYEES table
CREATE TABLE employees (
	employee_name VARCHAR(20) NOT NULL UNIQUE,
	employee_id INT PRIMARY KEY,
	manager_id INT,
	phone_number VARCHAR(20),
	hire_date DATE,
	salary INT,
	job VARCHAR(20),
	department VARCHAR(20) NOT NULL);
GRANT SELECT ON TABLE employees TO SHARE
   IN APPLICATION PACKAGE hierarchical_data_package;
COPY INTO employees FROM @stage/data
    FILE_FORMAT = (TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"'
        NULL_IF='' EMPTY_FIELD_AS_NULL=true);

-- set app version
ALTER APPLICATION PACKAGE hierarchical_data_package
  ADD VERSION v1_0
  USING '@stage'
  LABEL = 'Hierarchical Data Viewer v1.0';
  
ALTER APPLICATION PACKAGE hierarchical_data_package
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = v1_0
  PATCH = 0;

-- create app
CREATE APPLICATION hierarchical_data_app
    FROM APPLICATION PACKAGE hierarchical_data_package
    USING '@stage'
    DEBUG_MODE = true;
SHOW APPLICATIONS;
