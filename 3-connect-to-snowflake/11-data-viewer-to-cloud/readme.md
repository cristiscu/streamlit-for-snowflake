# Deploy the Connected Hierarchical Data Viewer to Streamlit Cloud

Has new *isLocal* and *getRemoteSession* functions, which will protect the deployed app with a connect form. A Snowflake account name, username and password, will be required when deployed to the Streamlit Cloud. CSV files will be uploaded only is the Streamlit web app is in local mode.