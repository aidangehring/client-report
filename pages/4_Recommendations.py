import streamlit as st
from utils.config import images_path,Shoes

st.title("Recommendations")
st.write("Based on the results of this assesment my recommendations are as follows:")

with st.expander("The best choice overall:"):
    st.subheader("Nike Pegasus Plus")
    st.markdown(Shoes['Pegasus']['cost'])
    st.image('images/pegasus_plus')
    st.info('You considered the Pegasus plus to be the most comfortable, and requiring the least effort to maintain the speed of 10km/h on the treadmill according\
            to RPE. This agrees with the outcomes of the force and movement analysis, which suggests that the shoe resulted in the most mechanically efficient\
            outputs of the three shoes. However, with a considerably steeper price point than the Nike Relentless 2, the true value of the Pegasus Plus would come\
             through the ability of this shoe to keep up as you become a stronger runner and progress to longer distances.')
    
with st.expander("The budget friendly option:"):
    st.subheader("Nike Relentless 2")
    st.markdown(Shoes['Relentless']['cost'])
    st.image('images/nike_relentless_2.jpg')
    st.info('The Nike Relentless 2 was slightly behind the Pegasus Plus across every measure. The key difference that seems to lead to the edge for the\
             Pegasus shoe is the larger movement variation observed across\
            the 5 minutes in the Relentless shoe. The variation suggests that technique was likely altered due to fatigue or discomfort which makes it more\
            difficult to suggest that this shoe can keep up as you progress as a runner. With that said, at a quarter of the price of the Pegasus, this\
            shoe provides a cheaper alternative which you would be trading for performance especially as you begin to run longer distances.')
    
with st.expander("Not recommended:"):
    st.subheader('Adidas Spezial')
    st.markdown(Shoes['Spezial']['cost'])
    st.image('images/adidas_spezial')
    st.info('I highly recommend avoiding the Adidas Spezial for running, though I am sure you had intended on doing so anyways following the pain in your\
            shins after only 5 minutes of running. The discomfort, along with the high level of perceived difficulty to maintain 10 km/h in this shoe\
            makes sense when looking at the high level of evidence that mechancis were altered due to the discomfort, leading to low\
            mechancial efficiency. At a price point of double the Nike Relentless 2 there is no area where this shoe would provide a benfit that cannot\
            be matched by the others for your intended use.')

    




