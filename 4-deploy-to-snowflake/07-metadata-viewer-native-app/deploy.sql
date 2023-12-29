-- to be deployed as a Native App with: snowsql -c my_conn -f deploy.sql
!set variable_substitution=true

-- create app package
DROP APPLICATION IF EXISTS hierarchical_metadata_app CASCADE;
DROP APPLICATION PACKAGE IF EXISTS hierarchical_metadata_package;
CREATE APPLICATION PACKAGE hierarchical_metadata_package;
USE APPLICATION PACKAGE hierarchical_metadata_package;
SHOW APPLICATION PACKAGES;

DROP SCHEMA public;
CREATE SCHEMA private;

CREATE STAGE stage;
!define CRT_DIR=file://C:\Projects\streamlit-for-snowflake-test\metadata-native-app
PUT &CRT_DIR\Main.py @stage overwrite=true auto_compress=false;
PUT &CRT_DIR\pages\*.py @stage/pages overwrite=true auto_compress=false;
PUT &CRT_DIR\manifest.yml @stage overwrite=true auto_compress=false;
PUT &CRT_DIR\readme.md @stage overwrite=true auto_compress=false;
PUT &CRT_DIR\script.sql @stage overwrite=true auto_compress=false;
LIST @stage;

-- set app version
ALTER APPLICATION PACKAGE hierarchical_metadata_package
  ADD VERSION v1_0
  USING '@stage'
  LABEL = 'Hierarchical Metadata Viewer v1.0';
  
ALTER APPLICATION PACKAGE hierarchical_metadata_package
  SET DEFAULT RELEASE DIRECTIVE
  VERSION = v1_0
  PATCH = 0;

-- create app
CREATE APPLICATION hierarchical_metadata_app
    FROM APPLICATION PACKAGE hierarchical_metadata_package
    USING '@stage'
    DEBUG_MODE = true;
SHOW APPLICATIONS;
