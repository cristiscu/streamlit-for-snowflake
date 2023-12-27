import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit import vega_lite_chart

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

sel = "Bank Failures by Quarter"
st.markdown(f"**{sel}**")
value_chart_tab, value_dataframe_tab, value_query_tab \
    = st.tabs(["Chart", "Raw Data", "SQL Query"])

sql = f"""
    SELECT LAST_DAY(transaction_date, 'quarter') AS date,
            COUNT(*) AS BANK_FAILURES
    FROM {DATABASE}.{SCHEMA}.financial_institution_events
    WHERE transformation_type = 'Failure'
            AND category_predecessor = 'Bank'
    AND date >= '1980-01-01'
    GROUP BY date
    ORDER BY date
    ;
"""
data = get_active_session().sql(sql).to_pandas()

with value_chart_tab:
    data["BANK_FAILURES"] = pd.to_numeric(data["BANK_FAILURES"])
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
                            "field": "BANK_FAILURES",
                            "title": "Bank Failures",
                            "type": "quantitative",
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
