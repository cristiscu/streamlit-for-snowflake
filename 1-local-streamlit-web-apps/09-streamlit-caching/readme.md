# Cache Data Between Page Reruns in Streamlit

The **@st.cache_data** Streamlit function decorator can be used to cache the same data already loaded between reruns. Here we'll no longer reload the same CSV file when we change just the child or parent column selection.