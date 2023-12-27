import os, configparser
import streamlit as st
from snowflake.snowpark import Session

# customize with your own local connection parameters
@st.cache_resource(show_spinner="Connecting to Snowflake...")
def getSession():
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.expanduser('~'), ".snowsql/config"))
    section = "connections.demo_conn"
    pars = {
        "account": parser.get(section, "accountname"),
        "user": parser.get(section, "username"),
        "password": os.environ['SNOWSQL_PWD']
    }
    return Session.builder.configs(pars).create()

@st.cache_data(show_spinner="Getting all database names...")
def getDatabases():
    query = "show databases"
    rows = getSession().sql(query).collect()
    if rows is None: st.stop()
    return [str(row["name"]) for row in rows]

@st.cache_data(show_spinner="Getting database schema names...")
def getSchemas(database):
    query = f'show schemas in database "{database}"'
    rows = getSession().sql(query).collect()
    if rows is None: st.stop()
    return [str(row["name"]) for row in rows]

# select a database and schema
def getDatabaseAndSchema():
    databases = getDatabases()
    database = st.sidebar.selectbox('Database', databases, index=None)
    if database is None: return None, None

    schemas = getSchemas(database)
    sel = None if "PUBLIC" not in schemas else schemas.index("PUBLIC")
    schema = st.sidebar.selectbox('Schema', schemas, index=sel)
    return database, schema
