import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit import vega_lite_chart

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

sel = "Monthly Change in Bank Branches Since Covid-19"
st.markdown(f"**{sel}**")
value_chart_tab, value_dataframe_tab, value_query_tab \
    = st.tabs(["Chart", "Raw Data", "SQL Query"])

sql = f"""
    WITH rssd_parents AS (
        SELECT id_rssd
        FROM {DATABASE}.{SCHEMA}.financial_institution_entities
    ), branch_openings_closures AS (
        SELECT 'Branch Openings' AS measure,
                DATE_TRUNC('month', start_date) AS date,
                COUNT(*) AS value
        FROM {DATABASE}.{SCHEMA}.financial_branch_entities AS open
        JOIN rssd_parents ON (rssd_parents.id_rssd = open.id_rssd_parent)
        WHERE category = 'Branch'
        GROUP BY measure, date
        UNION
        SELECT 'Branch Closures' AS measure,
                DATE_TRUNC('month', end_date) AS date,
                -COUNT(*) AS value
        FROM {DATABASE}.{SCHEMA}.financial_branch_entities AS close
        JOIN rssd_parents ON (rssd_parents.id_rssd = close.id_rssd_parent)
        WHERE category = 'Branch'
            AND end_date IS NOT NULL
        GROUP BY measure, date
    ), net_change AS (
        SELECT measure, date, value, SUM(value) OVER (PARTITION BY date) AS net_change
        FROM branch_openings_closures
    )
    SELECT measure, date, value,
            net_change AS MONTHLY_NET_CHANGE,
            SUM(net_change) OVER (PARTITION BY measure ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS CUMULATIVE_CHANGE
    FROM net_change
    WHERE date >= '2018-01-01'
    ORDER BY measure, date;
"""
data = get_active_session().sql(sql).to_pandas()

with value_chart_tab:
    data["VALUE"] = pd.to_numeric(data["VALUE"])
    data["CUMULATIVE_CHANGE"] = pd.to_numeric(data["CUMULATIVE_CHANGE"])
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
                    "axis": {
                        "format": "%y-%b",
                    },
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
                            "field": "VALUE",
                            "title": "",
                            "type": "quantitative",
                        },
                        "color": {
                            "field": "MEASURE",
                            "title": "Measure",
                            "type": "nominal",
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
                            "field": "CUMULATIVE_CHANGE",
                            "title": "Cumulative Change",
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
