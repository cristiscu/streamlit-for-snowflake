import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit import vega_lite_chart

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

sel = "Share of Total Commercial Bank Deposits, Small Banks (Non-Top 25)"
st.markdown(f"**{sel}**")
value_chart_tab, value_dataframe_tab, value_query_tab \
    = st.tabs(["Chart", "Raw Data", "SQL Query"])

sql = f"""
    WITH small_banks AS (
        SELECT
            date,
            value AS small_bank_deposits
        FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries AS ts
        INNER JOIN
            {DATABASE}.{SCHEMA}.financial_fred_attributes AS att
            ON (ts.variable = att.variable)
        WHERE
            att.variable_name
            = 'Deposits, Small Domestically Chartered Commercial Banks, Seasonally adjusted, Weekly, USD'
    ),

    large_banks AS (
        SELECT
            date,
            value AS large_bank_deposits
        FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries AS ts
        INNER JOIN
            {DATABASE}.{SCHEMA}.financial_fred_attributes AS att
            ON (ts.variable = att.variable)
        WHERE
            att.variable_name
            = 'Deposits, Large Domestically Chartered Commercial Banks, Seasonally adjusted, Weekly, USD'
    )

    SELECT
        small_banks.date,
        small_bank_deposits / (small_bank_deposits + large_bank_deposits) AS small_bank_pct_deposits
    FROM small_banks
    INNER JOIN large_banks ON (small_banks.date = large_banks.date)
    WHERE small_banks.date >= '2015-01-01'
    ORDER BY small_banks.date
    ;
"""
data = get_active_session().sql(sql).to_pandas()

with value_chart_tab:
    data["SMALL_BANK_PCT_DEPOSITS"] = pd.to_numeric(data["SMALL_BANK_PCT_DEPOSITS"])
    vega_lite_chart(
        data=data,
        spec={  # to customize see https://vega.github.io/vega-lite/
            "autosize": {
                "type": "fit",
                "contains": "padding",
                "resize": True,
            },
            "mark": {
                "type": "line",
                "point": False,
                "tooltip": True,
            },
            "title": None,
            "encoding": {
                "x": {
                    "field": "DATE",
                    "title": "",
                    "type": "temporal",
                    "axis": {
                        "format": "%y-%b",
                    },
                    "scale": {"type": "utc"},
                },
                "y": {
                    "field": "SMALL_BANK_PCT_DEPOSITS",
                    "title": "Share of Deposits",
                    "type": "quantitative",
                    "axis": {
                        "format": "%",
                    },
                    "scale": {
                        "zero": False,
                        "domain": [0.27, 0.35],
                    },
                },
            },
        },
        use_container_width=True,
        theme="streamlit",
    )


with value_dataframe_tab:
    st.dataframe(data, use_container_width=True)

with value_query_tab:
    st.code(sql.replace("\n        ", "\n"), "sql")

