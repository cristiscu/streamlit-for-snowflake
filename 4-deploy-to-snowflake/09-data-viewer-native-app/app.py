import json
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
import modules.graphs as graphs
import modules.formats as formats
import modules.charts as charts

@st.cache_data(show_spinner="Running a Snowflake query...")
def getDataFrame(query):
    rows = get_active_session().sql(query).collect()
    return pd.DataFrame(rows).convert_dtypes()

st.set_page_config(layout="wide")
st.title("Hierarchical Data Viewer")
st.caption("Display your hierarchical data with charts and graphs.")

with st.sidebar:
    tableName = st.text_input("Full table/view name:")
    if tableName is None or len(tableName) == 0:
        tableName = "hierarchical_data_app.app.emp_man"
    df_orig = getDataFrame(f"select * from {tableName}")

    cols = list(df_orig.columns)
    child = st.selectbox("Child Column Name", cols, index=0)
    parent = st.selectbox("Parent Column Name", cols, index=1)
    df = df_orig[[child, parent]]

tabSource, tabPath, tabFormat, tabGraph, tabChart = st.tabs(
    ["Source", "Path", "Format", "Graph", "Chart"])

with tabSource:
    st.dataframe(df_orig, use_container_width=True)

with tabPath:
    query = ("call hierarchical_data_app.app.show_path("
        + f"'{tableName}', '{child}', '{parent}')")
    df_path = getDataFrame(query)
    st.dataframe(df_path, use_container_width=True)

# show in another data format
with tabFormat:
    sel = st.selectbox(
        "Select a data format:",
        ["JSON", "XML", "YAML", "JSON Path", "JSON Tree"])

    root = formats.getJson(df)
    if sel == "JSON":
        jsn = json.dumps(root, indent=2)
        st.code(jsn, language="json", line_numbers=True)
    elif sel == "XML":
        xml = formats.getXml(root)
        st.code(xml, language="xml", line_numbers=True)
    elif sel == "YAML":
        yaml = formats.getYaml(root)
        st.code(yaml, language="yaml", line_numbers=True)
    elif sel == "JSON Path":
        jsn = json.dumps(formats.getPath(root, []), indent=2)
        st.code(jsn, language="json", line_numbers=True)
    elif sel == "JSON Tree":
        st.json(root)

with tabGraph:
    st.graphviz_chart(graphs.getEdges(df))

# show as Plotly chart
with tabChart:
    labels = df[df.columns[0]]
    parents = df[df.columns[1]]

    sel = st.selectbox(
        "Select a chart type:",
        ["Treemap", "Icicle", "Sunburst", "Sankey"])
    if sel == "Treemap":
        fig = charts.makeTreemap(labels, parents)
    elif sel == "Icicle":
        fig = charts.makeIcicle(labels, parents)
    elif sel == "Sunburst":
        fig = charts.makeSunburst(labels, parents)
    elif sel == "Sankey":
        fig = charts.makeSankey(labels, parents)
    st.plotly_chart(fig, use_container_width=True)
