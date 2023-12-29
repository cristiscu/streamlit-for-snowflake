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

## Actions

Paste and run the two *"create-scripts"* in separate SQL Worksheets, in both your consumer and provider Snowflake web UI. Wait until the changes are propagated to the Account Usage schema views.

To deploy the app as a Native App, run **`snowsql -c my_conn -f deploy.sql`**. Check that there are no errors (i.e. no text in red on screen). Switch to the Snowflake web UI and run/test/edit the app there.

To share it with other accounts from your organization, deploy the APPLICATION PACKAGE in a private listing, and specifying other account names. The consumer can get the shared app from its Apps folder.