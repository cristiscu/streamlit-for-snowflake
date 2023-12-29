# Deploy the Connected Hierarchical Data Viewer to Streamlit Cloud

Has new *isLocal* and *getRemoteSession* functions, which will protect the deployed app with a connect form. A Snowflake account name, username and password, will be required when deployed to the Streamlit Cloud. CSV files will be uploaded only is the Streamlit web app is in local mode.

## Actions

From the local subfolder, run in a Terminal window **`streamlit run app.py`**. Quit the local Streamlit web app session with CTRL+C.

Deploy the app in the Streamlit Community Cloud, and check that it now requires a connection to a Snowflake account through a login form. Pass right and wrong connection parameters and see how it behaves.
