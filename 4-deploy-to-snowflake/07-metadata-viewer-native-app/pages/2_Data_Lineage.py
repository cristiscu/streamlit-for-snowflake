import streamlit as st
from snowflake.snowpark.context import get_active_session

def getGraph():
    edges = ""
    for row in rows:
        nFrom = str(row[0]) if row[0] is not None and len(str(row[0])) > 0 else ' '
        nTo = str(row[1]) if row[1] is not None and len(str(row[1])) > 0 else ' '
        nFrom, nTo = nFrom.replace('"', '\\"'), nTo.replace('"', '\\"')
        if nFrom != ' ' or nTo != ' ': edges += f'\t"{nFrom}" -> "{nTo}";\n'
    return ('digraph {\n'
        + '\tgraph [rankdir="LR"]\n'
        + '\tnode [shape="rect"]\n\n'
        + f'\t " " [shape="ellipse"];\n\n'
        + f'{edges}'
        + '}')


st.set_page_config("Data Lineage", layout="wide")
st.title("Hierarchical Metadata Viewer")
st.header("Data Lineage")

query = """
select distinct
    directSources.value:objectName::string as source,
    objects_modified.value:objectName::string as target
from snowflake.account_usage.access_history,
    lateral flatten(input => objects_modified) objects_modified,
    lateral flatten(input => objects_modified.value:"columns", outer => true) cols,
    lateral flatten(input => cols.value:directSources, outer => true) directSources
"""
rows = get_active_session().sql(query).collect()
st.graphviz_chart(getGraph())
