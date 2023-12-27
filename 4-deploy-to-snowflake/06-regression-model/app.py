import os, configparser
import streamlit as st
from snowflake.snowpark import Session
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, call_udf, year, month

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

st.set_page_config(
    page_title="Financial & Economic Essentials",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")

st.title("Financial & Economic Essentials")
st.subheader("PCE over the last years")
with st.expander("What is the PCE Price Index?"):
    st.write("""
The prices you pay for goods and services change all the time – moving at different rates and even in different directions. Some prices may drop while others are going up. A price index is a way of looking beyond individual price tags to measure overall inflation (or deflation) for a group of goods and services over time.
The PCE Price Index is a measure of the prices that people living in the United States, or those buying on their behalf, pay for goods and services.The PCE price index is known for capturing inflation (or deflation) across a wide range of consumer expenses and reflecting changes in consumer behavior.
""")

# build query with DataFrame
session = getSession()
df = (session
    .table("FINANCIAL__ECONOMIC_ESSENTIALS.CYBERSYN.FINANCIAL_FRED_TIMESERIES")
    .filter(col('VARIABLE_NAME') == 'Personal Consumption Expenditures: Chain-type Price Index, Seasonally adjusted, Monthly, Index 2017=100')
    .filter(col('DATE') >= '1972-01-01')
    .filter(month(col('DATE')) == 1)
    .select(year(col('DATE')).alias('"Year"'), (col('VALUE')-100).alias('PCE'))
    .sort('"Year"', ascending=False)
    .to_pandas())
df["PCE"] = df["PCE"].round(2)

# create metrics
year_last = df.loc[0]["Year"].astype('int')
value_last = df.loc[0]["PCE"]
value_delta = value_last - df.loc[1]["PCE"]

# call UDF for model inference
df_pred = session.create_dataframe([
    [int(year_last+1)],
    [int(year_last+2)],
    [int(year_last+3)]],
    schema=["Year"])

udf_name = "financial_regression.public.predict_pce_udf"
df_pred = (df_pred
    .select(col("year"), call_udf(udf_name, col("year")).as_("pce"))
    .sort(col("year"))
    .to_pandas())
df_pred.rename(columns={"YEAR": "Year"}, inplace=True)
df_pred["PCE"] = df_pred["PCE"].round(2).astype(float) - 100

# combine actual and prediction dataframes
df_all = (df
        .set_index('Year')
        .sort_index()
        .rename(columns={"PCE": "Actual"})
    ._append(df_pred
        .set_index('Year')
        .sort_index()
        .rename(columns={"PCE": "Prediction"})))

# display metrics for global value and predictions
col1, col2, col3 = st.columns(3)
with st.container():
    with col1:
        st.metric(
            f"PCE in {str(year_last)}",
            round(value_last),
            round(value_delta),
            delta_color=("inverse"))
    with col2:
        st.metric(
            f"Predicted PCE for {str(int(df_pred.loc[0]['Year']))}",
            round(df_pred.loc[0]["PCE"]), 
            round(df_pred.loc[0]["PCE"] - value_last),
            delta_color=("inverse"))
    with col3:
        st.metric(
            f"Predicted PCE for {str(int(df_pred.loc[1]['Year']))}",
            round(df_pred.loc[1]["PCE"]),
            round(df_pred.loc[1]["PCE"] - value_last),
            delta_color=("inverse"))

st.bar_chart(data=df_all.tail(25),
    width=0, height=0, use_container_width=True)
