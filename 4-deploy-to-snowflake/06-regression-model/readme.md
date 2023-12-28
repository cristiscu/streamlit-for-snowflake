# Train a Linear Regression ML Model and Predict with UDF

Simplified version of the [**Building a data application with Snowflake Marketplace, Snowpark and Streamlit**](https://quickstarts.snowflake.com/guide/data_apps_summit_lab/index.html?index=..%2F..index#0) quickstart tutorial. It is using the free [**Cybersyn Financial & Economic Essentials**](https://quickstarts.snowflake.com/guide/getting_started_with_cybersyn_financial_and_economic_essentials_app/index.html?index=..%2F..index#0) dataset from the Snowflake Marketplace.

* **setup.sql** - SQL script to execute in a SQL worksheet after getting the free dataset from the Snowflake Marketplace.
* **notebook.ipynb** - Jupyter Notebook notebook, that trains a Linear Regression model with scikit-learn, in an experimental sequential manner. And creates an UDF with Snowpark, to serve the model and make predictions.
* **app.py** - single-page Python code to deploy as a Streamlit App in Snowflake.
* **orig/** - folder with some original files.