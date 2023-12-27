-- run from current folder with: snowsql -c demo_conn -f deploy.sql
CREATE OR REPLACE DATABASE environment_streamlit;

CREATE STAGE mystage;
PUT file://.\Main.py @mystage overwrite=true auto_compress=false;
PUT file://.\pages\*.py @mystage/pages overwrite=true auto_compress=false;

CREATE STREAMLIT environment_pages
    ROOT_LOCATION = '@environment_streamlit.public.mystage'
    MAIN_FILE = '/Main.py'
    QUERY_WAREHOUSE = "COMPUTE_WH";
