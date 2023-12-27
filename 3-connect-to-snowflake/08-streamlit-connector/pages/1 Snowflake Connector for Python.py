import os
import snowflake.connector
import streamlit as st

st.title("Connecting to Snowflake")
st.header("Snowflake Connector for Python")

@st.cache_resource(max_entries=10)
def getConnection(connection_name="snowflake"):
    section = st.secrets[f"connections_{connection_name}"]
    return snowflake.connector.connect(
        account=section["account"],
        user=section["user"],
        password=os.environ["SNOWSQL_PWD"],
        database=section["database"],
        schema=section["schema"],
        role=section["role"],
        warehouse=section["warehouse"]
    )

@st.cache_data(ttl=3600, show_spinner="Running query...")
def runQuery(_conn, query):
    cur = _conn.cursor()
    cur.execute(query)
    return cur.fetch_pandas_all()


conn = getConnection()
df = runQuery(conn, "select * from employees")
st.dataframe(df)
