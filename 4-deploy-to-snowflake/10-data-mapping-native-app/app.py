import streamlit as st
from snowflake.snowpark.context import get_active_session

st.header("IP to Location")

# get current data
query = "SELECT * FROM REFERENCE('tabletouse')"
df = get_active_session().sql(query).to_pandas()
st.dataframe(df)

# map columns
st.sidebar.header('Map Columns')
column_names = df.columns.values.tolist()
col_ip = st.sidebar.selectbox('IP column', column_names, index=0)
col_result = st.sidebar.selectbox('Result column', column_names, index=1)
        
# update data
def update_table():
    query = f"CALL app.enrich_ip_data('{col_ip}', '{col_result}')"
    get_active_session().sql(query).collect()

st.button('Update Data', on_click=update_table)
