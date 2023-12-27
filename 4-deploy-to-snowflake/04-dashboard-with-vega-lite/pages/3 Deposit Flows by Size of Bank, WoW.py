import datetime
import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit import vega_lite_chart

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

sel = "Deposit Flows by Size of Bank, WoW"
st.markdown(f"**{sel}**")
value_chart_tab, value_dataframe_tab, value_query_tab \
    = st.tabs(["Chart", "Raw Data", "SQL Query"])

min_year = 1980
max_year = datetime.date.today().year
start_y, end_y = st.sidebar.select_slider(
    "Date Range:",
    options=range(min_year, max_year + 1),
    value=(min_year, max_year))
selected_series = st.sidebar.multiselect(
    label="Select Bank Type:",
    options=("Top 25 Banks", "All Other Banks"),
    default=("All Other Banks"))

if len(selected_series) == 0: bank_selection = ""
else: bank_selection = selected_series

sql = f"""
    SELECT date AS DATE,
            IFF(att.variable_name ILIKE '%Small Domestically Chartered%', 'All Other Banks', 'Top 25 Banks') AS bank_type,
            value AS DEPOSITS,
            deposits - LAG(deposits, 1) OVER (PARTITION BY bank_type ORDER BY date) AS value
    FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries AS ts
    INNER JOIN {DATABASE}.{SCHEMA}.financial_fred_attributes AS att ON (ts.variable = att.variable)
    WHERE att.variable_name IN ('Deposits, Small Domestically Chartered Commercial Banks, Seasonally adjusted, Weekly, USD',
                                'Deposits, Large Domestically Chartered Commercial Banks, Seasonally adjusted, Weekly, USD')
        AND date >= '{str(min_year) + "-01-01"}'
        AND (YEAR(date) BETWEEN '{start_y}' AND '{end_y}')
        { ("AND bank_type IN ('" + "','".join(bank_selection) + "')") if bank_selection else ""}
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
                    "scale": {"type": "utc"},
                },
                "y": {
                    "field": "VALUE",
                    "title": "Deposit Change, WoW ($)",
                    "type": "quantitative",
                    "axis": {
                        "format": "$~s",
                        "labelExpr": "replace(datum.label, 'G', 'B')",
                    },
                },
                "color": {
                    "field": "BANK_TYPE",
                    "title": "Bank Type",
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
