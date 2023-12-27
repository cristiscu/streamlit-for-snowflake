use schema tests.public;

create or replace stage streamlit_stage;

put file://C:\Projects\streamlit-for-snowflake-test\first-streamlit-app\app.py @streamlit_stage
    overwrite=true auto_compress=false;

create or replace streamlit first_streamlit_app
    root_location = '@tests.public.streamlit_stage'
    main_file = '/app.py'
    query_warehouse = 'COMPUTE_WH';
show streamlits;