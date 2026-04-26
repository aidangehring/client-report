import streamlit as st
import pandas as pd
from utils.config import Shoes

st.title("Comfort")


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
          and red indicating low comfort of 3 or lower. The dropdowns below outline shoes which noted to be etither comfortable or uncomforatble to run in\
         as well as a summarized comment you made regarding the comfortablity after running in the shoe.")


with st.expander("Which shoes were uncomfortable to run in?"):
    st.write("The following shoes are not recommended based on discomfort:")
    for shoe in low_comfort.values():
        st.subheader(shoe['name'])
        st.image(shoe['image'])
        st.write('Comment from testing:' + shoe['comfort comments'])

with st.expander("Which shoes were comfortable to run in?"):
    st.write("The following shoes are recommended based on comfort:")
    for shoe in high_running_comfort.values():
        st.subheader(shoe['name'])
        st.image(shoe['image'])
        st.write('Comment from testing:' + shoe['comfort comments'])

