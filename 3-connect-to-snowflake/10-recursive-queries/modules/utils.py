import os, configparser
import pandas as pd
from snowflake.snowpark import Session
import streamlit as st

def getFullPath(filename):
    crtdir = os.path.dirname(__file__)
    pardir = os.path.abspath(os.path.join(crtdir, os.pardir))
    return f"{pardir}/{filename}"

# customize with your own Snowflake connection parameters
@st.cache_resource(show_spinner="Connecting to Snowflake...", max_entries=10)
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

@st.cache_data(show_spinner="Running a Snowflake query...")
def getDataFrame(_session, query):
    rows = _session.sql(query).collect()
    return pd.DataFrame(rows).convert_dtypes()

@st.cache_data(show_spinner="Loading the CSV file...")
def loadFile(filename):
    return pd.read_csv(filename).convert_dtypes()
