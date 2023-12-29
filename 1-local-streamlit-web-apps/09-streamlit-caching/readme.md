# Cache Data Between Page Reruns in Streamlit

The **@st.cache_data** Streamlit function decorator can be used to cache the same data already loaded between reruns. Here we'll no longer reload the same CSV file when we change just the child or parent column selection.

## Actions

From the current subfolder, run from a Terminal **`streamlit run app.py`**. Quit the local Streamlit web app session with CTRL+C.