import webbrowser
import urllib.parse
import pandas as pd
import streamlit as st

st.title("Hierarchical Data Viewer")

df = pd.read_csv("data/employees.csv", header=0).convert_dtypes()
st.dataframe(df)

edges = ""
for _, row in df.iterrows():
    if not pd.isna(row.iloc[1]):
        edges += f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'

d = f'digraph {{\n{edges}}}'
st.graphviz_chart(d)

#url = f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(d)}'
#webbrowser.open(url)