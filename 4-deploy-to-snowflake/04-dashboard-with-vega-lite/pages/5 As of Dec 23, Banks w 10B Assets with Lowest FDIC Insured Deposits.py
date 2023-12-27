import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session
from streamlit import vega_lite_chart

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

sel = "As of Dec '23: Banks w/ $10B Assets with Lowest FDIC Insured Deposits"
st.markdown(f"**{sel}**")
value_chart_tab, value_dataframe_tab, value_query_tab \
    = st.tabs(["Chart", "Raw Data", "SQL Query"])

sql = f"""
        WITH big_banks AS (
            SELECT id_rssd
            FROM {DATABASE}.{SCHEMA}.financial_institution_timeseries
            WHERE VARIABLE = 'ASSET'
                AND date = '2022-12-31'
                AND value > 1E10
        )
        SELECT name,
                value AS pct_insured,
                IFF(is_active, 'Active', 'Failed') AS BANK_STATUS
        FROM {DATABASE}.{SCHEMA}.financial_institution_timeseries AS ts
        JOIN {DATABASE}.{SCHEMA}.financial_institution_attributes AS att ON (ts.variable = att.variable)
        JOIN {DATABASE}.{SCHEMA}.financial_institution_entities AS ent ON (ts.id_rssd = ent.id_rssd)
        JOIN big_banks ON (big_banks.id_rssd = ts.id_rssd)
        AND ts.date = '2022-12-31'
        AND att.variable_name = '% Insured (Estimated)'
        AND att.frequency = 'Quarterly'
        ORDER BY pct_insured ASC
        LIMIT 15;
"""
data = get_active_session().sql(sql).to_pandas()

with value_chart_tab:
    data["PCT_INSURED"] = pd.to_numeric(data["PCT_INSURED"])
    vega_lite_chart(
        data=data,
        spec={  # to customize see https://vega.github.io/vega-lite/
            "autosize": {
                "type": "fit",
                "contains": "padding",
                "resize": True,
            },
            "mark": {
                "type": "bar",
                "point": False,
                "tooltip": True,
            },
            "title": None,
            "encoding": {
                "x": {
                    "field": "NAME",
                    "title": "",
                    "type": "nominal",
                    "sort": "y",
                    "axis": {"labelLimit": 0},
                },
                "y": {
                    "field": "PCT_INSURED",
                    "title": "Percent Insured",
                    "type": "quantitative",
                    "axis": {
                        "format": ".0%",
                    },
                },
                "color": {
                    "field": "BANK_STATUS",
                    "title": "Bank Type",
                    "type": "nominal",
                },
            },
            "height": 500,
        },
        use_container_width=True,
        theme="streamlit",
    )


with value_dataframe_tab:
    st.dataframe(data, use_container_width=True)

with value_query_tab:
    st.code(sql.replace("\n        ", "\n"), "sql")
