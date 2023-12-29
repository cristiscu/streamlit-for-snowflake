# Deploy the Hierarchical Metadata Viewer in Snowflake as a Streamlit App

* **create-scripts/*.sql** - SQL scripts to create Snowflake test data for object dependencies and data lineage. (Wait until changes are propagated into the Account Usage views!)
* **Main.py** - multi-page Python entry code, to deploy as a Streamlit App in Snowflake.
* **utils.py** - common module with connecting to Snowflake, from local or from the Snowflake account.
* **pages/*.py** - Python code for object dependencies and data lineage.
* **deploy.sql** - SQL script to deploy as a Streamlit App in Snowflake.
* **requirements.txt** - required local third-party Python packages.

## Actions

Paste and run the two *"create-scripts"* in separate SQL Worksheets, in your Snowflake web UI. Wait until the changes are propagated to the Account Usage schema views.

From the local subfolder, run in a Terminal window **`streamlit run Main.py`**. Quit the local Streamlit web app session with CTRL+C.

To deploy it as a Streamlit App, run **`snowsql -c demo_conn -f deploy.sql`**. Check that there are no errors (i.e. no text in red on screen). Switch to the Snowflake web UI and run/edit the app there.