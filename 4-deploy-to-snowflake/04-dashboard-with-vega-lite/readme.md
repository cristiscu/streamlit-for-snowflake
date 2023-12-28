# Create a Multi-Page Dashboard with Vega-Lite Charts as a Streamlit App

Simplified version of the [**Cybersyn Streamlit in Snowflake - Financial Demo**](https://quickstarts.snowflake.com/guide/getting_started_with_streamlit_in_snowflake/index.html?index=..%2F..index#0) quickstart guide. It is using the [**Cybersyn's Financial Data Package**] free dataset from the Snowflake Marketplace. It renders eight charts with **Vega-Lite**, deployed as a Streamlit App in Snowflake.

* **app-orig.py** - original single-page file application, with charts one below the other.
* **app-tabs.py** - improved single-page file application, with charts displayed one at a time.
* **Main.py** - multi-page Python entry code, to deploy as a Streamlit App in Snowflake.
* **pages/*.py** - Python code for the multi-page Streamlit App, one page per chart type.
* **deploy.sql** - SQL script to deploy as a Streamlit App in Snowflake.