# Create a Hierarchical Metadata Viewer as a Streamlit Multi-Page App

Build a multi-page Streamlit app connecting to Snowflake through a Snowpark session and using Snowflake metadata. The app will query the object dependencies from the OBJECT_DEPENDENCIES Account Usage view, and data lineage from the ACCESS_HISTORY view.

Read more in my posts on the Snowflake Data Superheroes Medium blog:

* [**How to Display Object Dependencies in Snowflake**](https://medium.com/snowflake/how-to-display-object-dependencies-in-snowflake-43914a7fc275)
* [**How to Visualize the Data Lineage Graph in Snowflake**](https://medium.com/snowflake/how-to-visualize-the-data-lineage-graph-in-snowflake-f0a356046380)

## Files

* **1-create-scripts** - folder with SQL scripts to create test data in Snowflake. Must wait a while for the changes to propagate to the Account Usage views.
* **2-single-page-tabs/app.py** - single-page Streamlit app with the results appearing in different tabs. 
* **3-multi-page-old/app.py** - multi-page Streamlit app with a select box.
* **4-multi-page/Main.py** - multi-page Streamlit app with separate files in a *pages* subfolder. It also uses a separate **utils.py** file to get the Snowpark session.
* **requirements.txt** - external dependencies, for pip install.