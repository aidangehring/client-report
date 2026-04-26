import streamlit as st
from utils.config import Shoes, client_height, client_mass, treadmill_speed_kmh, athlete_info, assessment_protocol
import pandas as pd

st.title("Overview")
st.write("This is an interactive report generated to guide you through the results of your assessment interactively. Please use the table of contents\
         on the left to navigate the pages, and interact with th dropdowns as necessary \
         to guide you through the information and anlysis that leads to my recommendations, and prepare any questions you may have for our meeting." )

if "my_expander_open" not in st.session_state:
    st.session_state.my_expander_open = True

with st.expander('Athlete profile'):
    col1, col2, col3 = st.columns(3)
    col1.metric("Height", athlete_info['height'])
    col2.metric("Mass", athlete_info['mass'])
    col3.metric("Skill Level", athlete_info['skill level'])
    st.divider()
    st.markdown("**Assessment Goal**")
    st.info(athlete_info['assessment goal'])

with st.expander('The setup and protocol'):
    col_img, col_info = st.columns([1, 2])
    with col_img:
        st.image(assessment_protocol['image'], width='stretch')
    with col_info:
        st.info(assessment_protocol['description'])

with st.expander('The shoes tested'):
    for i, (shoe_name, shoe_info) in enumerate(Shoes.items()):
        col_img, col_info = st.columns([1, 2])
        with col_img:
            st.image(shoe_info['image'], width='stretch')
        with col_info:
            st.subheader(shoe_info['name'] )
            st.markdown(shoe_info['cost'])
            st.info(shoe_info['description'])
        if i < len(Shoes) - 1:
            st.divider()




