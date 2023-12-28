import urllib.parse
import streamlit as st
import utils

st.set_page_config("Data Lineage", layout="wide")
st.title("Hierarchical Metadata Viewer")
st.header("Data Lineage")

# must wait a while to propagate into ACCOUNT_USAGE!
query = """
select distinct
directSources.value:objectName::string as source,
objects_modified.value:objectName::string as target
from snowflake.account_usage.access_history,
lateral flatten(input => objects_modified) objects_modified,
lateral flatten(input => objects_modified.value:"columns", outer => true) cols,
lateral flatten(input => cols.value:directSources, outer => true) directSources
"""
rows = utils.getSession().sql(query).collect()

# build graph in DOT notation
edges = ""
for row in rows:
    nFrom = str(row[0]) if row[0] is not None and len(str(row[0])) > 0 else ' '
    nTo = str(row[1]) if row[1] is not None and len(str(row[1])) > 0 else ' '
    nFrom, nTo = nFrom.replace('"', '\\"'), nTo.replace('"', '\\"')
    if nFrom != ' ' or nTo != ' ': edges += f'\t"{nFrom}" -> "{nTo}";\n'
graph = ('digraph {\n'
    + '\tgraph [rankdir="LR"]\n'
    + '\tnode [shape="rect"]\n\n'
    + f'\t " " [shape="ellipse"];\n\n'
    + f'{edges}'
    + '}')

# show graph
try: st.link_button("Visualize Online",
    f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(graph)}')
except: pass
st.graphviz_chart(graph)
