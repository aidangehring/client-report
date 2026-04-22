
import streamlit as st
from utils.data_loader import load_data, get_series
from utils.config import variable_options,joints,axes, Shoes, variable_labels
import plotly.graph_objects as go
from utils.metrics import symmetry_index, peak_power_gen
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

