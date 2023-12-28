# Create an Entity-Relationship Diagram Viewer with Streamlit

Build an ERD Viewer in Streamlit for Snowflake databases. Could try [different layouts](https://graphviz.org/docs/layouts/) with the generated GraphViz image.

Read more in my posts on the Snowflake Data Superheroes Medium blog:

* [**Streamlit ERD Viewer in Snowflake**](https://medium.com/snowflake/streamlit-erd-viewer-in-snowflake-88e33529d121)
* [**How to Generate ERDs from a Snowflake Model**](https://medium.com/snowflake/how-to-generate-erds-from-a-snowflake-model-3fc53abd0669)

For ER diagrams with Snowflake, could also use [**DBeaver Community Edition**](https://dbeaver.io/) or my own free [**Model Xtractor**](https://data-xtractor.com/model-xtractor/).

## Files

* **app.py** - calls **`show imported privileges`** to extract all PK-FK constraints for a selected database schema, at the table level.
* **utils.py** - utilities to get and cache the local Snowpark session, the list of Snowflake database names, and their schemas.
* **create-scripts** - folder with SQL scripts to create test Snowflake databases: *Chinook* and *Indian Reserves*.