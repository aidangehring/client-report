import streamlit as st
import pandas as pd
from utils.config import Shoes

st.title("Comfort")
st.write("This is the page where the client's perception of comfort for the 3\
        shoes will be analysed.")

df= pd.DataFrame([{
    'Shoe': shoe['name'],
    'Standing Comfort': shoe['standing_comfort'],
    'Running Comfort': shoe['running_comfort']
} for shoe in Shoes.values()
]).set_index('Shoe')

def colour_rating(val):
    if val >= 7:
        return 'background-color: green'
    elif val >= 5:
        return 'background-color: yellow'
    else:
        return 'background-color: red'
    
high_comfort={}
moderate_comfort={}
low_comfort={}
high_standing_comfort={}
high_running_comfort={}

for shoe in Shoes.values():
    if shoe['standing_comfort'] >= 7 and shoe['running_comfort'] >= 7:
        high_comfort[shoe['name']] = shoe
    elif shoe['standing_comfort'] >= 5 and shoe['running_comfort'] >= 5:
        moderate_comfort[shoe['name']] = shoe
    else:
        low_comfort[shoe['name']] = shoe

for shoe in Shoes.values():
    if shoe['standing_comfort'] >= 7:
        high_standing_comfort[shoe['name']] = shoe
    if shoe['running_comfort'] >= 7:
        high_running_comfort[shoe['name']] = shoe
st.dataframe(df.style.map(colour_rating, subset=['Standing Comfort', 'Running Comfort']))

st.write("The table above shows the comfort ratings rated out of 10 for each shoe during standing and running.\
          The cells are colour coded based on the rating, with green indicating high comfort of 7 or above, yellow indicating moderate comfort,\
          and red indicating low comfort of 3 or lower.")

if st.button("Show me the shoes with high comfort ratings (7 or above for both standing and running)"):
    st.write("The following shoes were recommended for high comfort (7 or above for both standing and running):")
    for shoe in high_comfort.values():
        st.subheader(shoe['name'])
        st.image(shoe['image'])
        st.write('Comment from testing:' + shoe['comfort comments'])

if st.button ("Running is important to me. Which shoes were uncomfortable to run in? (3 or below)"):
    st.write("The following shoes were recommended for low running comfort (3 or below):")
    for shoe in low_comfort.values():
        st.subheader(shoe['name'])
        st.image(shoe['image'])
        st.write('Comment from testing:' + shoe['comfort comments'])

if st.button("I want to maximise comfort during standing, show me the shoes with high standing comfort ratings (7 or above for standing)"):
    st.write("The following shoes were recommended for high standing comfort (7 or above for standing):")
    for shoe in high_standing_comfort.values():
        st.subheader(shoe['name'])
        st.image(shoe['image'])
        st.write('Comment from testing:' + shoe['comfort comments'])

if st.button("I want to maximise comfort during running, show me the shoes with high running comfort ratings (7 or above for running)"):
    st.write("The following shoes were recommended for high running comfort (7 or above for running):")
    for shoe in high_running_comfort.values():
        st.subheader(shoe['name'])
        st.image(shoe['image'])
        st.write('Comment from testing:' + shoe['comfort comments'])
