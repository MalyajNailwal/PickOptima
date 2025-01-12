import pandas as pd
import numpy as np
import plotly.express as px
from utils.routing.distances import (
    distance_picking,
    next_location
)
from utils.routing.routes import (
    create_picking_route
)
from utils.batch.mapping_batch import (
    orderlines_mapping,
    locations_listing
)
from utils.cluster.mapping_cluster import (
    df_mapping
)
from utils.batch.simulation_batch import (
    simulate_batch
)  # Fixed import here
from utils.cluster.simulation_cluster import(
    loop_wave,
    simulation_cluster,
    create_dataframe,
    process_methods
)
from utils.results.plot import (
    plot_simulation1,
    plot_simulation2
)
import streamlit as st

# Set page configuration with improved layout and a wider design
st.set_page_config(page_title="OptiPick Pro: Warehouse Optimization Tool",
                    initial_sidebar_state="expanded",
                    layout='wide',
                    page_icon="📦")

# Set a brown background with a bit of contrast for text
st.markdown(
    """
    <style>
    body {
        background-color: #3e2723;
        color: #fff;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        cursor: url('https://cdn.pixabay.com/photo/2017/10/25/07/14/cursor-2898276_960_720.png'), auto;
    }

    /* Header Styles */
    .stHeader {
        font-size: 2.5em;
        font-weight: bold;
        color: #ffcc80;
        text-align: center;
        padding: 10px 0;
    }

    .stSubheader {
        font-size: 1.5em;
        color: #ffcc80;
        padding: 5px 0;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #8d6e63;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1.1em;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #d7ccc8;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        transform: scale(1.05);
    }

    /* Sliders and Inputs Styling */
    .stSlider>div>div>div {
        background-color: #8d6e63;
        border-radius: 5px;
        transition: all 0.3s ease;
    }

    .stSlider>div>div>div:hover {
        background-color: #d7ccc8;
    }

    .stTextInput>div>div>input {
        background-color: #d7ccc8;
        color: #3e2723;
        font-size: 1.1em;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    .stTextInput>div>div>input:hover {
        background-color: #8d6e63;
        color: #fff;
    }

    /* Cursor Shine Effect */
    .shiny-effect:hover {
        box-shadow: 0 0 10px 3px rgba(255, 204, 128, 0.9);
        transform: scale(1.05);
        transition: all 0.3s ease;
    }

    /* Styled Headers and Subheaders */
    .stHeader, .stSubheader {
        text-transform: uppercase;
    }

    /* Add Icon Styling */
    .stMarkdown>p>span {
        font-size: 2em;
        padding-right: 10px;
    }

    /* Chart Styling */
    .plotly-graph-div {
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        background-color: #fff;
        padding: 15px;
    }

    /* General Layout Enhancements */
    .stApp {
        padding: 20px;
    }

    /* Shine effect on hover for clickable items */
    .stMarkdown p:hover {
        box-shadow: 0 0 10px 5px rgba(255, 204, 128, 0.8);
        transform: scale(1.1);
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# Set up the page
@st.cache_data(persist=False)
def load(filename, n):
    df_orderlines = pd.read_csv(IN + filename).head(n)
    return df_orderlines

# Alley Coordinates on y-axis
y_low, y_high = 5.5, 50
# Origin Location
origin_loc = [0, y_low]
# Distance Threshold (m)
distance_threshold = 35
distance_list = [1] + [i for i in range(5, 100, 5)]
IN = 'static/in/'
# Store Results by WaveID
list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = [], [], [], [], [], [], []
list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]  # Group in list
# Store Results by Simulation (Order_number)
list_ordnum , list_dstw = [], []

# Simulation 1: Order Batch
st.markdown("<h2 class='stHeader shiny-effect'>Impact of the wave size in orders (Orders/Wave) 📊</h2>", unsafe_allow_html=True)
st.subheader('''🛠️ HOW MANY ORDER LINES DO YOU WANT TO INCLUDE IN YOUR ANALYSIS?''')
col1, col2 = st.columns(2)
with col1:
    n = st.slider('SIMULATION 1 SCOPE (THOUSAND ORDERS)', 1, 200, value=5)
with col2:
    lines_number = 1000 * n 
    st.write(f"{lines_number:,} order lines")

# SIMULATION PARAMETERS
st.subheader(''' SIMULATE ORDER PICKING BY WAVE OF N ORDERS PER WAVE WITH N IN [N_MIN, N_MAX]''')
col_11 , col_22 = st.columns(2)
with col_11:
    n1 = st.slider('SIMULATION 1: N_MIN (ORDERS/WAVE)', 0, 20, value=1)
    n2 = st.slider('SIMULATION 1: N_MAX (ORDERS/WAVE)', n1 + 1, 20, value=max(n1 + 1, 10))
with col_22:
    st.write(f"[N_MIN, N_MAX] = [{n1:,}, {n2:,}]")

# START CALCULATION
start_1 = False
if st.checkbox('SIMULATION 1: START CALCULATION', key='show', value=False):
    start_1 = True

if start_1:
    df_orderlines = load('df_lines.csv', lines_number)
    df_waves, df_results = simulate_batch(n1, n2, y_low, y_high, origin_loc, lines_number, df_orderlines)
    plot_simulation1(df_results, lines_number)

# Simulation 2: Order Batch using Spatial Clustering 
st.markdown("<h2 class='stHeader shiny-effect'>Impact of the order batching method 📦</h2>", unsafe_allow_html=True)
st.subheader('''🛠️ HOW MANY ORDER LINES DO YOU WANT TO INCLUDE IN YOUR ANALYSIS?''')
col1, col2 = st.columns(2)
with col1:
    n_ = st.slider('SIMULATION 2 SCOPE (THOUSAND ORDERS)', 1, 200, value=5)
with col2:
    lines_2 = 1000 * n_ 
    st.write(f"🛠️{lines_2:,} order lines")

# START CALCULATION
start_2 = False
if st.checkbox('SIMULATION 2: START CALCULATION', key='show_2', value=False):
    start_2 = True

if start_2:
    df_orderlines = load('df_lines.csv', lines_2)
    df_reswave, df_results = simulation_cluster(y_low, y_high, df_orderlines, list_results, n1, n2, 
                                                distance_threshold)
    plot_simulation2(df_reswave, lines_2, distance_threshold)
