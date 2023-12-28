# Create a Multi-Page Dashboard with Altair Charts as a Streamlit App

Simplified version of the [**Getting Started With Snowpark for Python and Streamlit**](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_for_python_streamlit/index.html?index=..%2F..index#0) quickstart tutorial. It is using the [**Knoema Environment Data Atlas**] free dataset, which was once found in the Snowflake Marketplace. It renders two charts with **Altair**, deployed as a Streamlit App in Snowflake.

* **app-orig.py** - original single-page file application.
* **app-sels.py** - improved single-page file application.
* **Main.py** - multi-page Python entry code, to deploy as a Streamlit App in Snowflake.
* **pages/*.py** - Python code for the multi-page Streamlit App.
* **deploy.sql** - SQL script to deploy as a Streamlit App in Snowflake.