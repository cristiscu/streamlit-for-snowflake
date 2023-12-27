from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import altair as alt
import streamlit as st

st.header("Knoema: Environment Data Atlas")
st.subheader('CO2 Emissions by Countries Over Time')

with st.sidebar:
    countries = ['United States','China','Russia','India','United Kingdom','Germany','Japan','Canada']
    selected_countries = st.multiselect('Countries', countries,
        default = ['United States','China','Russia','India','United Kingdom'])

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

with st.container():
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

