# Deploy the Hierarchical Data Viewer as a Snowflake Native App

## User Interface

Display your parent-child data pairs in a better manner:

* *Source tab*: in an editable data frame.
* *Path tab*: with children indented below their parents, and the full path to the root node.
* *Format tab*: with a different data format (JSON, XML, YAML, or JSON Path)
* *Graph tab*: graphical representation, with nodes and edges between any parent and child.
* *Chart tab*: Plotly hierarchical charts.

## Required Consumer Privileges

The app comes with a few employee-manager pairs, displayed by default. But you may pass your own table or view name returning similar child-parent pairs, with one single top root node with no parent. Assuming you installed the app with its default name, you must grant read-only access to your own data with:

**`GRANT USAGE on DATABASE db TO APPLICATION hierarchical_data_app;`**
**`GRANT USAGE on SCHEMA db.schema TO APPLICATION hierarchical_data_app;`**
**`GRANT SELECT on TABLE/VIEW db.schema.name TO APPLICATION hierarchical_data_app;`**

## Project Files

The setup files will upload the CSV file into a new Snowflake table, exposed to the consumer through two secure views and one secure stored procedure.

* **manifest.yml** - required by the Snowflake Native App Framework.
* **script.sql** - required by the Snowflake Native App Framework.
* **deploy.sql** - deployment script, as a native app.
* **data/employees-raw.csv** - CSV raw file to be uploaded into Snowflake.
* **environment.yml** - required by the Snowflake Native App Framework.
* **requirements.txt** - ti run with pip install.

* **app.py** - Python code as entry-point of the Snowflake native app.
* **modules/formats.py** - convert tabular hierarchical data to JSON, XML, YAML, JSON Path.
* **modules/graphs.py** - render tabular hierarchical data with GraphViz graph.
* **modules/charts.py** - render tabular hierarchical data with Plotly charts.

## Actions

To deploy the app as a Native App, run **`snowsql -c my_conn -f deploy.sql`**. Check that there are no errors (i.e. no text in red on screen). Switch to the Snowflake web UI and run/test/edit the app there.

To share it with other accounts from your organization, deploy the APPLICATION PACKAGE in a private listing, and specifying other account names. The consumer can get the shared app from its Apps folder.

The app as it is right now will load the **data/employees-raw.csv** into a private Snowflake table, with transformed data exposed through two secure views to the consumer. The generic recursive SQL query is also encapsulated in a secure stored procedure. All secure objects are created in the **script.sql** consumer script.