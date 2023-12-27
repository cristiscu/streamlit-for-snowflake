import streamlit as st

st.title("Connecting to Snowflake")
st.header("Streamlit SnowflakeConnection")

conn = st.connection("snowflake")
df = conn.query("select * from employees",
    ttl=3600, show_spinner="Running query...")
st.dataframe(df)
