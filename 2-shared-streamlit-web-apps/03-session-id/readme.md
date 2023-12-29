# Use Data Caching with a Generated Session ID

The new **getSessionId()** function generates and saves an UUID in the session state, that will be used as a hash parameter when calling the *loadFile* function. This way each file is cached for the current user. When two users upload a file with the same path, there will be no conflict anymore, as each will be cached separatelly.

## Actions

From the current subfolder, run from a Terminal **`streamlit run app.py`**. Quit the local Streamlit web app session with CTRL+C.