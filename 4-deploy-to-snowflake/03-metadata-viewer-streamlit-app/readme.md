# Deploy the Hierarchical Metadata Viewer in Snowflake as a Streamlit App

* **create-scripts/*.sql** - SQL scripts to create Snowflake test data for object dependencies and data lineage. (Wait until changes are propagated into the Account Usage views!)
* **Main.py** - multi-page Python entry code, to deploy as a Streamlit App in Snowflake.
* **utils.py** - common module with connecting to Snowflake, from local or from the Snowflake account.
* **pages/*.py** - Python code for object dependencies and data lineage.
* **deploy.sql** - SQL script to deploy as a Streamlit App in Snowflake.
* **requirements.txt** - required local third-party Python packages.