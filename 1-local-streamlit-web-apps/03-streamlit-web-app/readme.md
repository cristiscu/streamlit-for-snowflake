# Convert the Hierarchical Data Viewer to a Streamlit Web App

This very simple local Streamlit web app:

* Installs Streamlit - with **`pip install streamlit`** - and reference it with **import streamlit as st**.
* Shows an application title with *st.title*.
* Displays the CSV data loaded in a Pandas data frame in a Streamlit *st.dataframe* output control.
* Displays the rendered GraphViz graph, in DOT notation, in a *st.graphviz_chart* output control.
* **app1.py** shows multiple ways to display formatted text with Streamlit.