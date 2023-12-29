# Create and Deploy a Streamlit in Snowflake App

Manually create a STREAMLIT object in the Streamlit tab, in the Snowflake web UI. Then create and deploy with SnowSQL a Python file as a Streamlit App in Snowflake.

* **app.py** - single-page Python code, to be deployed as a Streamlit App in Snowflake.
* **deploy.sql** - SQL script to deploy a Streamlit App in Snowflake.

## Actions

From the local subfolder, run in a Terminal window **`streamlit run app.py`**. Quit the local Streamlit web app session with CTRL+C.

Then you can copy and paste the content of the same **app.py** file into a new Streamlit App manually created in your Snowflake web UI. Or you can run **`snowsql -c demo_conn -f deploy.sql`**. Check that there are no errors (i.e. no text in red on screen).