-- to be deployed as a Streamlit App with: snowsql -c demo_conn -f deploy.sql
CREATE OR REPLACE DATABASE financial_streamlit;

CREATE STAGE mystage;
PUT file://.\Main.py @mystage overwrite=true auto_compress=false;
PUT file://.\pages\*.py @mystage/pages overwrite=true auto_compress=false;

CREATE STREAMLIT financial_pages
    ROOT_LOCATION = '@financial_streamlit.public.mystage'
    MAIN_FILE = '/Main.py'
    QUERY_WAREHOUSE = "COMPUTE_WH";
