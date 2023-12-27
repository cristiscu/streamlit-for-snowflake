import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit import vega_lite_chart

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

sel = "Deposits By Size of Bank"
st.markdown(f"**{sel}**")
value_chart_tab, value_dataframe_tab, value_query_tab \
    = st.tabs(["Chart", "Raw Data", "SQL Query"])

sql = f"""
    SELECT
        date AS DATE,
        IFF(att.variable_name ILIKE '%Small Domestically Chartered%', 'All Other Banks', ' Top 25 Banks') AS BANK_TYPE,
        value AS DEPOSITS
    FROM {DATABASE}.{SCHEMA}.financial_fred_timeseries AS ts
    INNER JOIN
        {DATABASE}.{SCHEMA}.financial_fred_attributes AS att
        ON (ts.variable = att.variable)
    WHERE
        att.variable_group IN ('Deposits, Large Domestically Chartered Commercial Banks',
                                'Deposits, Small Domestically Chartered Commercial Banks')
        AND att.seasonally_adjusted = TRUE
        AND date >= '1999-01-01'
        ORDER BY BANK_TYPE, DATE
    ;
"""
data = get_active_session().sql(sql).to_pandas()

with value_chart_tab:
    data["DEPOSITS"] = pd.to_numeric(data["DEPOSITS"],)
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
                    "field": "DEPOSITS",
                    "title": "Deposits",
                    "type": "quantitative",
                    "axis": {
                        "format": "$~s",
                        "labelExpr": "replace(datum.label, 'G', 'B')",  # replace G(iga) with B(illion)
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
        theme="streamlit")

with value_dataframe_tab:
    st.dataframe(data, use_container_width=True)

with value_query_tab:
    st.code(sql.replace("\n        ", "\n"), "sql")
