# Create a Multi-Page Dashboard with Altair Charts as a Streamlit App

Simplified version of the [**Getting Started With Snowpark for Python and Streamlit**](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_for_python_streamlit/index.html?index=..%2F..index#0) quickstart tutorial. It is using the [**Knoema Environment Data Atlas**] free dataset, which was once found in the Snowflake Marketplace. It renders two charts with **Altair**, deployed as a Streamlit App in Snowflake.

* **app-orig.py** - original single-page file application.
* **app-sels.py** - improved single-page file application.
* **Main.py** - multi-page Python entry code, to deploy as a Streamlit App in Snowflake.
* **pages/*.py** - Python code for the multi-page Streamlit App.
* **deploy.sql** - SQL script to deploy as a Streamlit App in Snowflake.

## Actions

If still available, get the free required dataset from the Snowflake Marketplace.

Paste the content of **app-orig.py**, then **app-sels.py**, over the generated Python file of a manually created Streamlit App. Run and test the apps in the Snowflake web UI.

Deploy the last multi-page version as a Streamlit App, running **`snowsql -c demo_conn -f deploy.sql`**. Check that there are no errors (i.e. no text in red on screen). Test the app in the Snowflake web UI.

Remark that none of these version allows for local test Snowflake connectivity!