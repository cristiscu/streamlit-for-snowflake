-- to be deployed as a Streamlit App with: snowsql -c demo_conn -f deploy.sql
!set variable_substitution=true
!define CRT_DIR=file://C:\Projects\streamlit-for-snowflake-test\metadata-viewer\4-multi-page

use schema tests.public;

create stage if not exists streamlit_stage;

put &CRT_DIR\*.py @streamlit_stage overwrite=true auto_compress=false;
put &CRT_DIR\pages\*.py @streamlit_stage/pages overwrite=true auto_compress=false;

create or replace streamlit metadata_viewer
    root_location = '@tests.public.streamlit_stage'
    main_file = '/Main.py'
    query_warehouse = 'COMPUTE_WH';
show streamlits;