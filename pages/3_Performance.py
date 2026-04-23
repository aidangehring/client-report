
import streamlit as st
from utils.data_loader import load_data, get_series
from utils.config import variable_options,joints,axes, Shoes, variable_labels
import plotly.graph_objects as go
from utils.metrics import peak_power_gen
st.title("Performance")
st.write("This page will analyse the performance of the 3 shoes based on\
         kinetic and kinematic data collected during the testing sessions.")

data= load_data()


variable_key= st.radio("Variable", list(variable_options.keys()), format_func= lambda k: variable_options[k], horizontal=True)

ctrl1, ctrl2, ctrl3= st.columns (3)

with ctrl1:
    if variable_key =='grf':
        side =st.radio ("Side", ['Left', 'Right'])
        joint=side
    else:
        joint= st.selectbox("Joint", joints)
with ctrl2:
    axis= st.radio ("Axis", axes, horizontal=True)

y_label= variable_labels[variable_key]



fig=go.Figure()

for shoe_key, shoe_info in Shoes.items():
    mean= get_series(data, variable_key, shoe_key, joint, axis, stat='Mean')
    sd= get_series(data,variable_key, shoe_key, joint, axis, stat='Std Dev')
    if mean is None:
        continue
    x= list(mean.index)
    color= shoe_info['color']

    if sd is not None: 
        fig.add_trace (go.Scatter(
            x=x + x[::-1],
            y=list(mean+sd) + list((mean-sd).iloc[::-1]),
            fill='toself',
            fillcolor=color,
            opacity= 0.12,
            line=dict(width=0),
            showlegend= False,
            hoverinfo= 'skip',
        ))
    fig.add_trace(go.Scatter(
        x=x,
        y=mean,
        name=shoe_info['name'],
        line=dict(color=color, width=2.5),
        hovertemplate= f"<b>{shoe_info['name']}</b><br>%{{x}}% GC<br>%{{y:.2f}}<extra></extra>"
    ))

fig.update_layout(
    xaxis=dict(
        title='% Gait Cycle',
        zeroline=False,
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        title= y_label,
        zeroline=True,
        zerolinecolor= '#333',
        zerolinewidth=1,
        tickfont=dict(size=11),
    ),
    legend=dict(
        borderwidth=1,
    )
)

if variable_key== 'angles' and axis=='X':
    st.markdown("The two main things to take note of in these angle plots are the solid the dark lines, which represents the average joint angle\
                across all the strides taken during the run, but also the width of the shaded regions which represents the variation of the joint angles\
                observed over the course of the 5 minute run. A larger range of average joint angle over a stride suggests that the body is allowing\
                itself to progress through a full range of motion with no adaptations required. As this range decreases, the body is typically limiting\
                the range of motion to compensate for some reason such as uncomfortability or fatigue. Additionally, a larger shaded area suggests that\
                over the course of the run the athlete changed their joint angles either from stride to stride, or from capture period to capture period.\
                This once again suggests that patterns changed from the typical optimal pattern to an alternative pattern to accomodate a reason\
                to change such as pain or fatigue.")

if variable_key== 'angles' and axis=='Y':
    st.markdown("")

if variable_key=='powers':
    with st.expander("Advanced Metrics", expanded=False):
        if 'Left' in joint and 'powers' in variable_key:
            pow_cols=st.columns(3)
            for col, (shoe_key,shoe_info) in zip(pow_cols,Shoes.items()):
                left_p= get_series(data,variable_key,shoe_key,joint,axis)
                pow=peak_power_gen(left_p)
                with col: 
                    st.markdown(f"**{shoe_info['name']}**")
                    st.metric("Peak power output", f"{pow:.1f}W" if pow is not None else "N/A")
        if 'Right' in joint and 'powers' in variable_key:
            pow_cols=st.columns(3)
            for col, (shoe_key,shoe_info) in zip(pow_cols,Shoes.items()):
                right_p= get_series(data,variable_key,shoe_key,joint,axis)
                pow=peak_power_gen(right_p)
                with col: 
                    st.markdown(f"**{shoe_info['name']}**")
                    st.metric("Peak power output", f"{pow:.1f}W" if pow is not None else "N/A")



                                

st.plotly_chart(fig, width='stretch')

