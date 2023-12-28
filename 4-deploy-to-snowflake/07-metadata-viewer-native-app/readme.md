# Deploy the Hierarchical Metadata Viewer as a Snowflake Native App

Explore Object Dependencies and Data Lineage. 

## Required Consumer Privileges

You must grant read-only access for our app to your own data with:

**`GRANT IMPORTED PRIVILEGES ON DATABASE snowflake TO APPLICATION hierarchical_metadata_app;`**

## Project Files

* **create-scripts/*.sql** - SQL scripts to create Snowflake test data for object dependencies and data lineage. (Wait until changes are propagated into the Account Usage views!)
* **manifest.yml** - required by the Snowflake Native App Framework.
* **script.sql** - required by the Snowflake Native App Framework.
* **deploy.sql** - deployment script, as a native app.
* **Main.py** - Python code as entry-point of the Snowflake native app.
* **pages/*.py** - Python code for each page of the app.