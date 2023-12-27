import streamlit as st
from snowflake.snowpark.context import get_active_session

def getGraph():
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

    return ('digraph {\n'
        + '\tgraph [rankdir="LR"]\n'
        + '\tnode [shape="rect"]\n\n'
        + f'{nodes}\n'
        + f'{edges}'
        + '}')


st.set_page_config("Object Dependencies", layout="wide")
st.title("Hierarchical Metadata Viewer")
st.header("Object Dependencies")

query = "select * from snowflake.account_usage.object_dependencies"
rows = get_active_session().sql(query).collect()
st.graphviz_chart(getGraph())
