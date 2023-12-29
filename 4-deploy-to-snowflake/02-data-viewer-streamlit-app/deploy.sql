-- to be deployed as a Streamlit App with: snowsql -c demo_conn -f deploy.sql
!set variable_substitution=true
!define CRT_DIR=file://C:\Projects\streamlit-for-snowflake-test\data-viewer-snowflake

use schema tests.public;

create stage if not exists streamlit_stage;

put &CRT_DIR\app.py @streamlit_stage overwrite=true auto_compress=false;
put &CRT_DIR\modules\*.py @streamlit_stage/modules overwrite=true auto_compress=false;
put &CRT_DIR\data\*.csv @streamlit_stage/data overwrite=true auto_compress=false;
-- put &CRT_DIR\animated\templates\*.html @streamlit_stage/animated/templates overwrite=true auto_compress=false;
put &CRT_DIR\environment.yml @streamlit_stage overwrite=true auto_compress=false;

create or replace streamlit data_viewer_snowflake
    root_location = '@tests.public.streamlit_stage'
    main_file = '/app.py'
    query_warehouse = 'COMPUTE_WH';
show streamlits;