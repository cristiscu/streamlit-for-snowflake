import pandas as pd

# digraph with edges only
def getEdges(df):
    edges = ""
    for _, row in df.iterrows():
        isRoot = pd.isna(row.iloc[1])
        if not isRoot:
            edges += f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'
    return f"digraph {{\n{edges}}}\n"
