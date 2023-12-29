# Convert the Hierarchical Data Viewer to a Streamlit Web App

This very simple local Streamlit web app:

* Install Streamlit - with **`pip install streamlit`**  (or **`pip install -r requirements.txt`**) - and reference it with **import streamlit as st**.
* Show an application title with *st.title*.
* Display the CSV data loaded in a Pandas data frame in a Streamlit *st.dataframe* output control.
* Display the rendered GraphViz graph, in DOT notation, in a *st.graphviz_chart* output control.
* **app1.py** shows multiple ways to display formatted text with Streamlit.

## Actions

From the current subfolder, run from a Terminal: **`streamlit run app.py`** (or **`streamlit run app1.py`** for the second use case). You are supposed to be automatically redirected to a browser page, with your first Streamlit app running as a local web app. Quit the session with CTRL+C from the Terminal.