import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Shoe Analysis", layout="wide")

pg= st.navigation([
    st.Page("pages/1_overview.py", title="Overview"),
    st.Page("pages/2_Comfort.py", title="Comfort"),
    st.Page("pages/3_Performance.py", title="Performance"),
    st.Page("pages/4_Injury-Risk.py", title="Injury Risk"),
    st.Page("pages/5_Recommendations.py", title="Recommendations")
])
pg.run()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');        
    
    [data-testid="stImage"] img {
        width: 700px !important;
        height: 500px !important;
        object-fit: contain !important;
    }
    
    [data-testid="stImage"] {
        width: 700px !important;
    }
</style>
""", unsafe_allow_html=True)
