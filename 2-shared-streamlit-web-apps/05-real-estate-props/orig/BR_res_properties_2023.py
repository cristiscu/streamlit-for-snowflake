# Modules:
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setup for Storytelling (matplotlib):
plt.rcParams['font.family'] = 'monospace'
plt.rcParams['font.size'] = 8
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['figure.facecolor'] = '#464545' 
plt.rcParams['axes.facecolor'] = '#464545' 
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlecolor'] = 'black'
plt.rcParams['axes.titlesize'] = 9
plt.rcParams['axes.labelcolor'] = 'darkgray'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.edgecolor'] = 'darkgray'
plt.rcParams['axes.linewidth'] = 0.2
plt.rcParams['ytick.color'] = 'darkgray'
plt.rcParams['xtick.color'] = 'darkgray'
plt.rcParams['axes.titlecolor'] = '#FFFFFF'
plt.rcParams['axes.titlecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'darkgray'
plt.rcParams['axes.linewidth'] = 0.85
plt.rcParams['ytick.major.size'] = 0

# --- App (begin):
BR_real_estate_appreciation = pd.read_csv('data/BR_real_estate_appreciation_Q1_2023.csv')
BR_real_estate_appreciation['Annual_appreciation'] = round(BR_real_estate_appreciation['Annual_appreciation'], 2)*100

# Page setup:
st.set_page_config(
    page_title="Residential properties (Brazil)",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Header:
st.header('Appreciation of residential properties in Brazil')

st.sidebar.markdown(''' > **How to use this app**

1. To Select a city (**green dot**).
2. To compare for the selected city against other 50 cities (**white dots**).
3. To compare the chosen city against **national average** and the data distribution.
4. To extract insights as "An appreciation above national average & price by square meter below average = possible *opportunity*".
''')

# Widgets:
cities = sorted(list(BR_real_estate_appreciation['Location'].unique()))
city_selection = st.selectbox(
    '🌎 Select a city',
    cities
)

# City selection:
your_city = city_selection
selected_city = BR_real_estate_appreciation.query('Location == @your_city')
other_cities = BR_real_estate_appreciation.query('Location != @your_city')

# CHART 1: Annual appreciation (12 months):
chart_1, ax = plt.subplots(figsize=(3, 4.125))
# Background:
sns.stripplot(
    data= other_cities,
    y = 'Annual_appreciation',
    color = 'white',
    jitter=0.85,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)
# Highlight:
sns.stripplot(
    data= selected_city,
    y = 'Annual_appreciation',
    color = '#00FF7F',
    jitter=0.15,
    size=12,
    linewidth=1,
    edgecolor='k',
    label=f'{your_city}'
)

# Showing up position measures:
avg_annual_val = BR_real_estate_appreciation['Annual_appreciation'].median()
q1_annual_val = np.percentile(BR_real_estate_appreciation['Annual_appreciation'], 25)
q3_annual_val = np.percentile(BR_real_estate_appreciation['Annual_appreciation'], 75)

# Plotting lines (reference):
ax.axhline(y=avg_annual_val, color='#DA70D6', linestyle='--', lw=0.75)
ax.axhline(y=q1_annual_val, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3_annual_val, color='white', linestyle='--', lw=0.75)

# Adding the labels for position measures:
ax.text(1.15, q1_annual_val, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.3, avg_annual_val, 'Median', ha='center', va='center', color='#DA70D6', fontsize=8, fontweight='bold')
ax.text(1.15, q3_annual_val, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# to fill the area between the lines:
ax.fill_betweenx([q1_annual_val, q3_annual_val], -2, 1, alpha=0.2, color='gray')
# to set the x-axis limits to show the full range of the data:
ax.set_xlim(-1, 1)

# Axes and titles:
plt.xticks([])
plt.ylabel('Average appreciation (%)')
plt.title('Appreciation (%) in the past 12 months', weight='bold', loc='center', pad=15, color='gainsboro')
plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), ncol=2, framealpha=0, labelcolor='#00FF7F')
plt.tight_layout()


# CHART 2: Price (R$) by m²:
chart_2, ax = plt.subplots(figsize=(3, 3.95))
# Background:
sns.stripplot(
    data= other_cities,
    y = 'BRL_per_squared_meter',
    color = 'white',
    jitter=0.95,
    size=8,
    linewidth=1,
    edgecolor='gainsboro',
    alpha=0.7
)
# Highlight:
sns.stripplot(
    data= selected_city,
    y = 'BRL_per_squared_meter',
    color = '#00FF7F',
    jitter=0.15,
    size=12,
    linewidth=1,
    edgecolor='k',
    label=f'{your_city}'
)

# Showing up position measures:
avg_price_m2 = BR_real_estate_appreciation['BRL_per_squared_meter'].median()
q1_price_m2 = np.percentile(BR_real_estate_appreciation['BRL_per_squared_meter'], 25)
q3_price_m2 = np.percentile(BR_real_estate_appreciation['BRL_per_squared_meter'], 75)

# Plotting lines (reference):
ax.axhline(y=avg_price_m2, color='#DA70D6', linestyle='--', lw=0.75)
ax.axhline(y=q1_price_m2, color='white', linestyle='--', lw=0.75)
ax.axhline(y=q3_price_m2, color='white', linestyle='--', lw=0.75)

# Adding the labels for position measures:
ax.text(1.15, q1_price_m2, 'Q1', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
ax.text(1.35, avg_price_m2, 'Median', ha='center', va='center', color='#DA70D6', fontsize=8, fontweight='bold')
ax.text(1.15, q3_price_m2, 'Q3', ha='center', va='center', color='white', fontsize=8, fontweight='bold')

# to fill the area between the lines:
ax.fill_betweenx([q1_price_m2, q3_price_m2], -2, 1, alpha=0.2, color='gray')
# to set the x-axis limits to show the full range of the data:
ax.set_xlim(-1, 1)

# Axes and titles:
plt.xticks([])
plt.ylabel('Price (R\$)')
plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), ncol=2, framealpha=0, labelcolor='#00FF7F')
plt.title('Average price (R\$) by $m^2$', weight='bold', loc='center', pad=15, color='gainsboro')
plt.tight_layout()

# Splitting the charts into two columns:
left, right = st.columns(2)

# Columns (content):
with left:
    st.pyplot(chart_1)
with right:
    st.pyplot(chart_2)

# Informational text:
st.markdown('''
<span style="color:white;font-size:10pt"> ⚪ Each point represents a city </span>
<span style="color:#DA70D6;font-size:10pt"> ▫ <b> Average value </b></span>
<span style="color:white;font-size:10pt"> ◽ Lowest values (<b> bottom </b>)
◽ Highest values (<b> top </b>) <br>
◽ **Q1** (first quartile): where 25% of data falls under
◽ **Q3** (third quartile): where 75% of data falls under
</span>

''',unsafe_allow_html=True)

# Showing up the numerical data (as a dataframe):
st.dataframe(
    BR_real_estate_appreciation.query('Location == @your_city')[[
      'Location', 'Annual_appreciation', 
      'BRL_per_squared_meter']]
)

# Adding some reference indexes:
st.markdown(''' > **Reference indexes (inflation):**

* IPCA: **6%** (National Broad Consumer Price Index)
* IGP-M: **4%** (General Market Price Index)

> Data based on public informs that accounts residential properties for 50 Brazilian cities (first quarter of 2023).
''')

# Authorship:
st.markdown('---')
st.markdown(''' **Built by Vinícius Oviedo**  

*(further information on the sidebar - to expand it)*

[![Linkedin Badge](https://img.shields.io/badge/-Linkedin-0A66C2?&logo=Linkedin&link=https://www.linkedin.com/in/vinicius-oviedo/)](https://www.linkedin.com/in/vinicius-oviedo/)
[![GitHub Badge](https://img.shields.io/badge/-GitHub-black?&logo=Medium&link=https://github.com/OviedoVR)](https://github.com/OviedoVR)
[![Medium Badge](https://img.shields.io/badge/-Medium-green?&logo=Medium&link=https://medium.com/@vo.freelancer5)](https://medium.com/@vo.freelancer5/)
[![Website Badge](https://img.shields.io/badge/-Website-whitesmoke?&link=https://oviedovr.github.io/DataAndLaTeX/)](https://oviedovr.github.io/DataAndLaTeX/)
''')
st.markdown('---')
# --- (End of the App)