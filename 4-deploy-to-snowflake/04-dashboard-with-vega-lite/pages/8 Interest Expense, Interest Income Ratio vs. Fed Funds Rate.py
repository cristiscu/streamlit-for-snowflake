import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit import vega_lite_chart

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

sel = "Interest Expense / Interest Income Ratio vs. Fed Funds Rate"
st.markdown(f"**{sel}**")
value_chart_tab, value_dataframe_tab, value_query_tab \
    = st.tabs(["Chart", "Raw Data", "SQL Query"])

sql = f"""
    WITH int_inc AS (
        SELECT
            date,
            value AS interest_income
        FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries
        WHERE variable_name = 'Income and Expense: Total Interest Income, Not seasonally adjusted, Quarterly, USD'
    ),

    int_exp AS (
        SELECT
            date,
            value AS interest_expense
        FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries
        WHERE variable_name = 'Income and Expense: Total Interest Expense, Not seasonally adjusted, Quarterly, USD'
    )
    SELECT
        int_inc.date AS display_date,
        'Interest Exp/Interest Inc Ratio' AS display_name,
        interest_expense / interest_income AS value
    FROM int_inc
    JOIN int_exp ON (int_inc.date = int_exp.date)
    WHERE display_date >= '1985-01-01'
    UNION
    SELECT
        LAST_DAY(date, 'quarter') AS display_date,
        'Fed Funds Rate' AS display_name,
        AVG(value) AS value
    FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries
    WHERE variable_name = 'Federal Funds Effective Rate'
    AND display_date >= '1985-01-01'
    GROUP BY display_date
    ORDER BY display_date
    ;
"""
data = get_active_session().sql(sql).to_pandas()

with value_chart_tab:
    data["VALUE"] = pd.to_numeric(data["VALUE"])
    vega_lite_chart(
        data=data,
        spec={  # to customize see https://vega.github.io/vega-lite/
            "autosize": {
                "type": "fit",
                "contains": "padding",
                "resize": True,
            },
            "title": None,
            "mark": {
                "type": "line",
                "point": False,
                "tooltip": True,
            },
            "encoding": {
                "x": {
                    "field": "DISPLAY_DATE",
                    "title": "",
                    "type": "temporal",
                    "scale": {"type": "utc"},
                },
                "y": {
                    "field": "VALUE",
                    "title": "",
                    "type": "quantitative",
                    "axis": {
                        "format": "%",
                    },
                },
                "color": {
                    "title": None,
                    "field": "DISPLAY_NAME",
                    "type": "nominal",
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
