# Import libraries
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import sum, col
import altair as alt
import streamlit as st

# Set page config
st.set_page_config(layout="wide")

# Get current session
session = get_active_session()

@st.cache_data()
def load_data():
    # Load CO2 emissions data
    snow_df_co2 = session.table("ENVIRONMENT_DATA_ATLAS.ENVIRONMENT.EDGARED2019").filter(col('Indicator Name') == 'Fossil CO2 Emissions').filter(col('Type Name') == 'All Type').sort('"Date"').with_column_renamed('"Date"','"Year"')

    # Load forest occupied land area data
    snow_df_land = session.table("ENVIRONMENT_DATA_ATLAS.ENVIRONMENT.\"WBWDI2019Jan\"").filter(col('Series Name') == 'Forest area (% of land area)')
    snow_df_land = snow_df_land.group_by('Country Name').agg(sum('$61').alias("Total Share of Forest Land")).sort('Country Name')
    return snow_df_co2.to_pandas(), snow_df_land.to_pandas()

# Load and cache data
df_co2_overtime, df_forest_land = load_data()

def co2_emmissions():
    st.subheader('CO2 Emissions by Countries Over Time')

    countries = ['United States','China','Russia','India','United Kingdom','Germany','Japan','Canada']
    selected_countries = st.multiselect('',countries, default = ['United States','China','Russia','India','United Kingdom'])
    st.markdown("___")

    # Display an interactive chart to visualize CO2 emissions over time for the selected countries
    with st.container():
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

    threshold = st.slider(label='Forest Occupied Land By Countries', min_value=1000, max_value=2500, value=1800, step=200, label_visibility='hidden')
    st.markdown("___")

    # Display an interactive chart to visualize forest occupied land area by countries
    with st.container():
        filter = df_forest_land['Total Share of Forest Land'] > threshold
        pd_df_land_top_n = df_forest_land.where(filter)
        st.bar_chart(data=pd_df_land_top_n.set_index('Country Name'), width=850, height=400, use_container_width=True) 

# Display header
st.header("Knoema: Environment Data Atlas")

# Create sidebar and load the first page
page_names_to_funcs = {
    "CO2 Emissions": co2_emmissions,
    "Forest Occupied Land": forest_occupied_land
}
selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()