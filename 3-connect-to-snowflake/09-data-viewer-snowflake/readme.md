# Connect the Hierarchical Data Viewer to Snowflake

Can now either update a CSV file or query a Snowflake table or view, connecting to Snowflake with a Snowpark session. The child and parent columns are by default the first two columns, but can be changed. By default, the local *data/employees.csv* file is loaded transparently.

## Actions

Make sure your Snowflake account name and username are saved in a connection session in the local SnowSQL config file (that we will use from now on, rather than hard-coding these values). And that your password is saved in a local SNOWSQL_PWD environment variable.

From the local subfolder, run in a Terminal window **`streamlit run app.py`**. Quit the local Streamlit web app session with CTRL+C.
