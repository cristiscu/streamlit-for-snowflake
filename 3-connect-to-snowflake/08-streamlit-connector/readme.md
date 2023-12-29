# Connect to Snowflake with Streamlit Connector in Multi-Page App

Traditional multi-page Streamlit app, with a *pages* folder. Each page presents one different way to connect to Snowflake from a client application:

* With the **Snowflake Connector for Python**
* With **Snowpark**
* With the [**Streamlit Connector for Snowflake**](https://docs.streamlit.io/knowledge-base/tutorials/databases/snowflake) (connection parameters in a hidden *.streamlit/secrets.toml* file)

## Actions

In a local *.streamlit/secrets.toml* file (excluded from GitHub!), make sure you provide proper Snowflake connection parameters for all three use cases. Including a hard-coded password for the Streamlit Connector!

From the local subfolder, run in a Terminal window **`streamlit run Main.py`**. Quit the local Streamlit web app session with CTRL+C.
