import urllib.parse
import streamlit as st
import utils

st.set_page_config(layout="wide")
st.title("Entity-Relationship Diagram Viewer")

# select database and schema
database, schema = utils.getDatabaseAndSchema()
if database is None or schema is None:
    st.warning("Select a database and a schema!")
    st.stop()

# get tables linked by PK-FK relationships
query = f'show imported keys in schema "{database}"."{schema}"'
rows = utils.getSession().sql(query).collect()

# build graph
edges, links = "", set()
for row in rows:
    pk, fk = str(row["pk_table_name"]), str(row["fk_table_name"])
    style = ' [style="dashed"]' if pk == fk else ''
    link = f'\t"{fk}" -> "{pk}"{style};\n'
    if link not in links: links.add(link); edges += link

graph = ('digraph {\n'
    + '\tgraph [rankdir="RL"]\n'
    + '\tnode [shape="rect"]\n'
    + '\tedge [arrowhead="none" arrowtail="crow" dir="both"]\n\n'
    + f'{edges}'
    + '}')

# show graph
st.link_button("Visualize Online",
    f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(graph)}')
st.graphviz_chart(graph)

