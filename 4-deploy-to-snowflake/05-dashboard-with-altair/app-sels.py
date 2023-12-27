import os, configparser
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
from snowflake.snowpark.functions import sum, col
import altair as alt
import streamlit as st

st.set_page_config(layout="wide")
st.header("Knoema: Environment Data Atlas")

def co2_emmissions():
    st.subheader('CO2 Emissions by Countries Over Time')
    countries = ['United States','China','Russia','India','United Kingdom','Germany','Japan','Canada']
    selected_countries = st.sidebar.multiselect('', countries,
        default = ['United States','China','Russia','India','United Kingdom'])

    with st.container():
        @st.cache_data()
        def load_co2_emmissions():
            # SELECT *, "Date" as "Year"
            # FROM ENVIRONMENT_DATA_ATLAS.ENVIRONMENT.EDGARED2019
            # WHERE "Indicator Name" = 'Fossil CO2 Emissions'
            # AND "Type Name" = 'All Type'
            # ORDER BY "Date";
            return (get_active_session()
                .table("ENVIRONMENT_DATA_ATLAS.ENVIRONMENT.EDGARED2019")
                .filter(col('Indicator Name') == 'Fossil CO2 Emissions')
                .filter(col('Type Name') == 'All Type')
                .sort('"Date"')
                .with_column_renamed('"Date"','"Year"')
                .to_pandas())
        df_co2_overtime = load_co2_emmissions()

        countries_list = countries if len(selected_countries) == 0 else selected_countries
        df_co2_overtime_filtered = df_co2_overtime[df_co2_overtime['Location Name'].isin(countries_list)]
        line_chart = alt.Chart(df_co2_overtime_filtered).mark_line(
            color="lightblue",
            line=True,
            point=alt.OverlayMarkDef(color="red")
        ).encode(
            x='Year',
            y='Value',
            color='Location Name',
            tooltip=['Location Name','Year','Value']
        )
        st.altair_chart(line_chart, use_container_width=True)

def forest_occupied_land():
    st.subheader('Forest Occupied Land Area by Countries')
    threshold = st.sidebar.slider(
        label='Forest Occupied Land By Countries',
        min_value=1000, max_value=2500, value=1800, step=200,
        label_visibility='hidden')

    with st.container():
        @st.cache_data()
        def load_forest_occupied_land():
            # SELECT SUM($61) AS "Total Share of Forest Land"
            # FROM ENVIRONMENT_DATA_ATLAS.ENVIRONMENT."WBWDI2019Jan"
            # WHERE "Series Name" = 'Forest area (% of land area)'
            # GROUP BY "Country Name"
            # ORDER BY "Country Name";
            return (get_active_session()
                .table("ENVIRONMENT_DATA_ATLAS.ENVIRONMENT.\"WBWDI2019Jan\"")
                .filter(col('Series Name') == 'Forest area (% of land area)')
                .group_by('Country Name')
                .agg(sum('$61').alias("Total Share of Forest Land"))
                .sort('Country Name')
                .to_pandas())
        df_forest_land = load_forest_occupied_land()

        filter = df_forest_land['Total Share of Forest Land'] > threshold
        pd_df_land_top_n = df_forest_land.where(filter)
        st.bar_chart(
            data=pd_df_land_top_n.set_index('Country Name'),
            width=850, height=400,
            use_container_width=True) 

page_names_to_funcs = {
    "CO2 Emissions": co2_emmissions,
    "Forest Occupied Land": forest_occupied_land }
selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()