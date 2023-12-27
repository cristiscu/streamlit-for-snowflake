from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import sum, col
import streamlit as st

st.header("Knoema: Environment Data Atlas")
st.subheader('Forest Occupied Land Area by Countries')

with st.sidebar:
    threshold = st.slider(label='Threshold',
        min_value=1000, max_value=2500, value=1800, step=200)

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

with st.container():
    df_forest_land = load_forest_occupied_land()
    filter = df_forest_land['Total Share of Forest Land'] > threshold
    pd_df_land_top_n = df_forest_land.where(filter)
    st.bar_chart(
        data=pd_df_land_top_n.set_index('Country Name'),
        width=850, height=400,
        use_container_width=True) 
