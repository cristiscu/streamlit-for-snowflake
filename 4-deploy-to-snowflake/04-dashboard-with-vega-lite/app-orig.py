import datetime
import pandas as pd
from snowflake.snowpark.context import get_active_session
import streamlit as st
from streamlit import (
    code,
    dataframe,
    markdown,
    multiselect,
    select_slider,
    tabs,
    vega_lite_chart,
)

st.set_page_config(layout="wide")
st.title("Cybersyn: Financial Package Preview")

# Database and schema to be used in sql queries
# in this case it should be database with mounted Cybersyn Financial Package listing
DATABASE = "FINANCIAL__ECONOMIC_ESSENTIALS"
SCHEMA = "CYBERSYN"

# Get the current credentials
session = get_active_session()

# This should be replaced with "from sqlparse import format as format_sql"
# but unfortunately sqlparse is not available as a library to Streamlit in Snowflake at the moment
def format_sql(sql):
    # Remove padded space so that it looks good in code and in the ui element
    return sql.replace("\n        ", "\n")


def deposits_by_size_of_bank_chart():
    # IMPORTANT: using f-strings to assemble sql queries is not safe and should only be used internally
    #            when you build external facing applications please sanitize sql to prevent sql injections
    #            https://xkcd.com/327/
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

    deposits_by_bank_size = session.sql(sql).to_pandas()

    markdown("**Deposits By Size of Bank**")
    value_chart_tab, value_dataframe_tab, value_query_tab = tabs(
        [
            "Chart",
            "Raw Data",
            "SQL Query",
        ],
    )

    with value_chart_tab:
        deposits_by_bank_size["DEPOSITS"] = pd.to_numeric(
            deposits_by_bank_size["DEPOSITS"],
        )
        vega_lite_chart(
            data=deposits_by_bank_size,
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
            theme="streamlit",
        )

    with value_dataframe_tab:
        dataframe(deposits_by_bank_size, use_container_width=True)

    with value_query_tab:
        code(
            format_sql(sql),
            "sql",
        )


def commercial_bank_deposits_chart():
    # IMPORTANT: using f-strings to assemble sql queries is not safe and should only be used internally
    #            when you build external facing applications please sanitize sql to prevent sql injections
    #            https://xkcd.com/327/
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

    data = session.sql(sql).to_pandas()

    markdown("**Share of Total Commercial Bank Deposits, Small Banks (Non-Top 25)**")
    value_chart_tab, value_dataframe_tab, value_query_tab = tabs(
        [
            "Chart",
            "Raw Data",
            "SQL Query",
        ],
    )

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
        dataframe(data, use_container_width=True)

    with value_query_tab:
        code(
            format_sql(sql),
            "sql",
        )


def deposits_flows_chart():
    min_year = 1980
    max_year = datetime.date.today().year
    start_y, end_y = select_slider(
        "Date Range:",
        options=range(min_year, max_year + 1),
        value=(min_year, max_year),
    )
    selected_series = multiselect(
        label="Select Bank Type:",
        options=("Top 25 Banks", "All Other Banks"),
        default=("All Other Banks"),
    )

    if len(selected_series) == 0:
        bank_selection = ""
    else:
        bank_selection = selected_series

    # IMPORTANT: using f-strings to assemble sql queries is not safe and should only be used internally
    #            when you build external facing applications please sanitize sql to prevent sql injections
    #            https://xkcd.com/327/
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

    deposits_by_bank_size = session.sql(sql).to_pandas()

    markdown("**Deposit Flows by Size of Bank, WoW**")
    value_chart_tab2, value_dataframe_tab2, value_query_tab2 = tabs(
        [
            "Chart",
            "Raw Data",
            "SQL Query",
        ],
    )

    with value_chart_tab2:
        deposits_by_bank_size["VALUE"] = pd.to_numeric(deposits_by_bank_size["VALUE"])
        vega_lite_chart(
            data=deposits_by_bank_size,
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

    with value_dataframe_tab2:
        dataframe(deposits_by_bank_size, use_container_width=True)

    with value_query_tab2:
        code(format_sql(sql), "sql")


def monthly_change_in_bank_branches_chart():
    # IMPORTANT: using f-strings to assemble sql queries is not safe and should only be used internally
    #            when you build external facing applications please sanitize sql to prevent sql injections
    #            https://xkcd.com/327/
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

    data = session.sql(sql).to_pandas()

    markdown("**Monthly Change in Bank Branches Since Covid-19**")
    value_chart_tab, value_dataframe_tab, value_query_tab = tabs(
        [
            "Chart",
            "Raw Data",
            "SQL Query",
        ],
    )

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
        dataframe(data, use_container_width=True)

    with value_query_tab:
        code(
            format_sql(sql),
            "sql",
        )


def banks_with_lowest_insured_deposits_chart():
    # IMPORTANT: using f-strings to assemble sql queries is not safe and should only be used internally
    #            when you build external facing applications please sanitize sql to prevent sql injections
    #            https://xkcd.com/327/
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

    data = session.sql(sql).to_pandas()

    markdown("**As of Dec '23: Banks w/ $10B Assets with Lowest FDIC Insured Deposits**")
    value_chart_tab, value_dataframe_tab, value_query_tab = tabs(
        [
            "Chart",
            "Raw Data",
            "SQL Query",
        ],
    )

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
        dataframe(data, use_container_width=True)

    with value_query_tab:
        code(
            format_sql(sql),
            "sql",
        )


def bank_failures_chart():
    # IMPORTANT: using f-strings to assemble sql queries is not safe and should only be used internally
    #            when you build external facing applications please sanitize sql to prevent sql injections
    #            https://xkcd.com/327/
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

    data = session.sql(sql).to_pandas()

    markdown("**Bank Failures by Quarter**")
    value_chart_tab, value_dataframe_tab, value_query_tab = tabs(
        [
            "Chart",
            "Raw Data",
            "SQL Query",
        ],
    )

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
        dataframe(data, use_container_width=True)

    with value_query_tab:
        code(
            format_sql(sql),
            "sql",
        )


def net_interest_income_vs_fed_funds_rate_chart():
    # IMPORTANT: using f-strings to assemble sql queries is not safe and should only be used internally
    #            when you build external facing applications please sanitize sql to prevent sql injections
    #            https://xkcd.com/327/
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

    data = session.sql(sql).to_pandas()

    markdown("**Banking Industry Net Interest Income vs. Fed Funds Rate**")
    value_chart_tab, value_dataframe_tab, value_query_tab = tabs(
        [
            "Chart",
            "Raw Data",
            "SQL Query",
        ],
    )

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
        dataframe(data, use_container_width=True)

    with value_query_tab:
        code(
            format_sql(sql),
            "sql",
        )


def interest_expense_over_interest_income_ratio_vs_fed_funds_rate_chart():
    # IMPORTANT: using f-strings to assemble sql queries is not safe and should only be used internally
    #            when you build external facing applications please sanitize sql to prevent sql injections
    #            https://xkcd.com/327/
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

    data = session.sql(sql).to_pandas()

    markdown("**Interest Expense / Interest Income Ratio vs. Fed Funds Rate**")
    value_chart_tab, value_dataframe_tab, value_query_tab = tabs(
        [
            "Chart",
            "Raw Data",
            "SQL Query",
        ],
    )

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
        dataframe(data, use_container_width=True)

    with value_query_tab:
        code(
            format_sql(sql),
            "sql",
        )


deposits_by_size_of_bank_chart()
commercial_bank_deposits_chart()
markdown("---")
deposits_flows_chart()
monthly_change_in_bank_branches_chart()
banks_with_lowest_insured_deposits_chart()
bank_failures_chart()
net_interest_income_vs_fed_funds_rate_chart()
interest_expense_over_interest_income_ratio_vs_fed_funds_rate_chart()