import os, configparser, urllib.parse
import streamlit as st
from snowflake.snowpark import Session

st.set_page_config(layout="wide")
st.title("Hierarchical Metadata Viewer")

# customize with your own local connection parameters
parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
section = "connections.demo_conn"
pars = {
    "account": parser.get(section, "accountname"),
    "user": parser.get(section, "username"),
    "password": os.environ['SNOWSQL_PWD']
}
session = Session.builder.configs(pars).create()

sel = st.sidebar.selectbox("Make a choice:", ["Object Dependencies", "Data Lineage"])
if sel == "Object Dependencies":
    st.header(sel)
    query = "select * from snowflake.account_usage.object_dependencies"
    rows = session.sql(query).collect()

    ids, nodes, edges = set(), "", ""
    for row in rows:
        # referenced object
        nameTo = f"{str(row[0])}.{str(row[1])}.{str(row[2])}".replace('"', '\\"')
        idTo = int(row[3]) if row[3] is not None else 0
        typeTo = str(row[4])
        if idTo not in ids:
            ids.add(idTo)
            nodes += f'\tn{idTo} [label="{nameTo}\\n({typeTo})"];\n'

        # referencing object
        nameFrom = f"{str(row[5])}.{str(row[6])}.{str(row[7])}".replace('"', '\\"')
        idFrom = int(row[8]) if row[8] is not None else 0
        typeFrom = str(row[9])
        if idFrom not in ids:
            ids.add(idFrom)
            nodes += f'\tn{idFrom} [label="{nameFrom}\\n({typeFrom})"];\n'

        # add edge
        edges += f'\tn{idFrom} -> n{idTo} '

        byType = str(row[10])
        if byType == "BY_ID": edges += '[style="dotted"];\n'
        elif byType == "BY_NAME": edges += '[style="dashed"];\n'
        else: edges += '[style="solid"];\n'

    graph = ('digraph {\n'
        + '\tgraph [rankdir="LR"]\n'
        + '\tnode [shape="rect"]\n\n'
        + f'{nodes}\n'
        + f'{edges}'
        + '}')

    # show graph
    st.link_button("Visualize Online",
        f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(graph)}')
    st.graphviz_chart(graph)

elif sel == "Data Lineage":
    st.header(sel)
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
    rows = session.sql(query).collect()

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
    st.link_button("Visualize Online",
        f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(graph)}')
    st.graphviz_chart(graph)
