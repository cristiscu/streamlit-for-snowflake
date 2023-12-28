# Deploy the Hierarchical Data Viewer in Snowflake as a Streamlit App

D3 animated charts are not supported, as well as the Streamlit link button.

* **data/*.csv** - CSV test data, to be uploaded in Snowflake tables.
* **app.py** - Python entry code, to deploy as a Streamlit App in Snowflake.
* **modules/*.py** - Python code with specific functionality.
* **environment.yml** - required by the Streamlit App.
* **requirements.txt** - required local third-party Python packages.
* **deploy.sql** - SQL script to deploy as a Streamlit App in Snowflake.
* **animated/templates/*.html** - D3 animated chart templates.
* **animated/*.html** - generated D3 chart files.