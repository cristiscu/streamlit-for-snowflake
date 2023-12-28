import json
import streamlit as st
import streamlit.components.v1 as components
from io import StringIO
import modules.graphs as graphs
import modules.formats as formats
import modules.charts as charts
import modules.animated as animated
import modules.utils as utils

st.set_page_config(layout="wide")
st.title("Hierarchical Data Viewer")
st.caption("Display your hierarchical data with charts and graphs.")

with st.sidebar:
    tableName = st.text_input("Full table/view name:")
    hasTable = tableName is not None and len(tableName) > 0
    if hasTable:
        session = utils.getSession()
        df_orig = utils.getDataFrame(session, f"select * from {tableName}")
    else:
        filename = utils.getFullPath("data/employees.csv")
        uploaded_file = st.file_uploader(
            "Upload a CSV file", type=["csv"], accept_multiple_files=False)
        if uploaded_file is not None:
            filename = StringIO(uploaded_file.getvalue().decode("utf-8"))
        df_orig = utils.loadFile(filename)

    cols = list(df_orig.columns)
    child = st.selectbox("Child Column Name", cols, index=0)
    parent = st.selectbox("Parent Column Name", cols, index=1)
    df = df_orig[[child, parent]]

tabSource, tabPath, tabFormat, tabGraph, tabChart, tabAnim = st.tabs(
    ["Source", "Path", "Format", "Graph", "Chart", "Animated"])

with tabSource:
    st.dataframe(df_orig, use_container_width=True)

with tabPath:
    if not hasTable:
        st.warning("Select a table/view")
    else:
        child_index = cols.index(child) + 1
        parent_index = cols.index(parent) + 1
        query = f"""
select repeat('  ', level - 1) || ${child_index} as name,
ltrim(sys_connect_by_path(${child_index}, '.'), '.') as path
from {tableName}
start with ${parent_index} is null
connect by prior ${child_index} = ${parent_index}
order by path;
"""
        session = utils.getSession()
        df_path = utils.getDataFrame(session, query)
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
    graph = graphs.getEdges(df)
    url = graphs.getUrl(graph)
    st.link_button("Visualize Online", url)
    st.graphviz_chart(graph)

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

# show as D3 animated chart
with tabAnim:
    sel = st.selectbox(
        "Select a D3 chart type:",
        ["Collapsible Tree", "Linear Dendrogram", "Radial Dendrogram", "Network Graph"])
    if sel == "Collapsible Tree":
        filename = animated.makeCollapsibleTree(df)
    elif sel == "Linear Dendrogram":
        filename = animated.makeLinearDendrogram(df)
    elif sel == "Radial Dendrogram":
        filename = animated.makeRadialDendrogram(df)
    elif sel == "Network Graph":
        filename = animated.makeNetworkGraph(df)

    with open(filename, 'r', encoding='utf-8') as f:
        components.html(f.read(), height=2200, width=1000)
