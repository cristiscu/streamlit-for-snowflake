import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit import vega_lite_chart

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

sel = "Banking Industry Net Interest Income vs. Fed Funds Rate"
st.markdown(f"**{sel}**")
value_chart_tab, value_dataframe_tab, value_query_tab \
    = st.tabs(["Chart", "Raw Data", "SQL Query"])

sql = f"""
    WITH fed_funds AS (
        SELECT
            variable_name,
            LAST_DAY(date, 'quarter') AS end_date,
            AVG(value) AS value
        FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries
        WHERE variable_name = 'Federal Funds Effective Rate'
        GROUP BY end_date, variable_name
        ORDER BY end_date, variable_name
    ),

    interest_income AS (
        SELECT
            date,
            value
        FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries
        WHERE variable_name = 'Income and Expense: Net Interest Income, Not seasonally adjusted, Quarterly, USD'
    )

    SELECT
        fed_funds.end_date AS date,
        fed_funds.value AS FED_FUNDS_RATE,
        interest_income.value AS NET_INTEREST_INCOME
    FROM fed_funds
    LEFT JOIN interest_income ON (fed_funds.end_date = interest_income.date)
    WHERE fed_funds.end_date >= '1985-01-01'
    ORDER BY date
    ;
"""
data = get_active_session().sql(sql).to_pandas()

with value_chart_tab:
    data["FED_FUNDS_RATE"] = pd.to_numeric(data["FED_FUNDS_RATE"])
    data["NET_INTEREST_INCOME"] = pd.to_numeric(data["NET_INTEREST_INCOME"])
    vega_lite_chart(
        data=data,
        spec={  # to customize see https://vega.github.io/vega-lite/
            "autosize": {
                "type": "fit",
                "contains": "padding",
                "resize": True,
            },
            "title": None,
            "encoding": {
                "x": {
                    "field": "DATE",
                    "title": "",
                    "type": "temporal",
                    "scale": {"type": "utc"},
                },
            },
            "resolve": {"scale": {"y": "independent"}},
            "layer": [
                {
                    "mark": {
                        "type": "bar",
                        "point": False,
                        "tooltip": True,
                    },
                    "encoding": {
                        "y": {
                            "field": "NET_INTEREST_INCOME",
                            "title": "Net Interest Income",
                            "type": "quantitative",
                            "axis": {
                                "format": "$~s",
                                "labelExpr": "replace(datum.label, 'G', 'B')",
                            },
                        },
                    },
                },
                {
                    "mark": {
                        "stroke": "#FC2947",
                        "type": "line",
                        "point": False,
                        "tooltip": True,
                    },
                    "encoding": {
                        "y": {
                            "field": "FED_FUNDS_RATE",
                            "title": "Fed Funds Rate",
                            "type": "quantitative",
                            "axis": {
                                "format": ".0%",
                            },
                        },
                    },
                },
            ],
        },
        use_container_width=True,
        theme="streamlit",
    )


with value_dataframe_tab:
    st.dataframe(data, use_container_width=True)

with value_query_tab:
    st.code(sql.replace("\n        ", "\n"), "sql")
