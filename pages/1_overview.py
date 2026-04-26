import streamlit as st
from utils.config import Shoes,client_weight,client_mass,treadmill_speed_kmh
import pandas as pd

st.title("Overview")
st.write("This report was generated to compare 3 different shoes\
         in order to provide recommendations for which shoe is best for the client. The 3 shoes were tested in a biomechanics lab,\
          where kinetic and kinematic data was collected during testing sessions. The client's perception of comfort for each shoe was also recorded.\
         The following pages will provide an analysis of the data collected during the testing sessions, and provide recommendations for the\
          client based on the findings.")
st.write("The 3 shoes tested were:")

for shoe_name, shoe_info in Shoes.items():
    st.subheader(shoe_info['name'])
    st.write(shoe_info['description'])
    st.image(shoe_info['image'])

rows=[]

rows.append({
    'Treadmill Speed': (treadmill_speed_kmh),
    'Client Weight': (client_mass),
    'Client Height': (client_mass)
})
if rows:
    st.dataframe(pd.DataFrame(rows), width='content')


