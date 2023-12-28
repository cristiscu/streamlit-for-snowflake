# Make App Private and Protect Public App Access

A Streamlit app deployed to the Streamlit Community Cloud can be made public or private.

Private apps can be shared with other people with email addresses in the Streamlit Cloud. 

Public apps can be eventually protected with a form, as implemented in **auth.py**, with either a password, or username and password. Valid values can be saved in the **.streamlit/secrets.toml** file, and entered again in the Secrets form when deploying to the cloud. Make sure you never save this file in GitHub!