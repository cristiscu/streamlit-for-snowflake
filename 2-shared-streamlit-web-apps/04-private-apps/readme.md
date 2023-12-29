# Make App Private and Protect Public App Access

A Streamlit app deployed to the Streamlit Community Cloud can be made public or private.

Private apps can be shared with other people with email addresses in the Streamlit Cloud. 

Public apps can be eventually protected with a form, as implemented in **auth.py**, with either a password, or username and password. Valid values can be saved in the **.streamlit/secrets.toml** file, and entered again in the Secrets form when deploying to the cloud. Make sure you never save this file in GitHub!

## Actions

From the current subfolder, run from a Terminal **`streamlit run app.py`**. Test the local app with a password field, then with both username and password, for both right and wrong login parameters. Quit the local Streamlit web app session with CTRL+C.

For your already deployed app, save all your changes into the GitHub repository, except for the *.streamlit/secrets.toml* file. In the Session tab of the Settings, copy and paste the content of your secrets.tml file. Test the deployed application with both right and wrong login parameters.

Make the app *Private*, and share it with other people, by sending invites with other email addresses. Then go back and make the app *Public* again.