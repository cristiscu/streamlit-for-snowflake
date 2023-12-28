# Deploy Your Local Web App to Streamlit Cloud

Deploy a Streamlit app to the cloud, as it is. The **requirements.txt** file will be executed with pip install.

The new **getFullPath(...)** function from **modules/utils.py** makes sure all local or remote files will appear with their full absolute path, as there may be some problems with relative file path when deployed.