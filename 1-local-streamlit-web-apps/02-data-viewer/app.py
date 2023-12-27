import webbrowser
import urllib.parse
import pandas as pd

df = pd.read_csv("data/employees.csv", header=0).convert_dtypes()

edges = ""
for _, row in df.iterrows():
    if not pd.isna(row.iloc[1]):
        edges += f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'

d = f'digraph {{\n{edges}}}'
url = f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(d)}'
webbrowser.open(url)