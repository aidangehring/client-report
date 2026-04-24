import os
import streamlit as st
from utils.data_loader import load_data, get_series, load_events
from utils.config import variable_options, variable_config, Shoes, sagittal_info
import plotly.graph_objects as go
from utils.metrics import peak_power_gen, step_lengths, cadence
import pandas as pd
st.title("Performance")
st.write("This page will analyse the performance of the 3 shoes based on kinetic and kinematic data collected during the testing sessions.\
         Because running, especially on a treadmill as was completed in this protocol, is predominantly involving forward progression this report\
         will mainly be focused on dorsiflexion/plantarflexion of the ankle and flexion/extension of the hip and knee joints.\
         Visuals and explanations for all of these movements can be explored using the appropriate buttons below.")
for movement in sagittal_info:
    with st.expander(f'What is {movement}?', expanded=False):
        st.image(sagittal_info[movement]['image'])
        st.markdown(sagittal_info[movement]['information'])
st.write("Analysis involves the examination of joint angles, moments, powers and vertical ground reaction force. To keep the information more concise, relevant\
         information for recommendations was isolated for self exploration, and can be navigated by selecting the variable and joint desired, which will update\
         the plot below. As the input changes, relevant information will also be updated.")
with st.expander ("Information for analysing the plots", expanded=False):
    st.markdown("All curves have been normalized, meaning that each time point on the x axis represents a % of the running stride, where a stride starts with one sides heel\
        contacting the ground, and ends with that same heel contacting the ground on the next step. Another thing to know when examining these curves is\
        that the solid line represents magnitude, or the average value for the correspnding shoe across the entire session. The faint shaded line represents a statistic\
        called standard deviation which represents how spread the data is. A wider range of this shaded region suggests a higher amount of variability\
        in technique across the run. ")

data= load_data()



variable_key= st.radio("Variable", list(variable_options.keys()), format_func= lambda k: variable_options[k], horizontal=True)

cfg = variable_config[variable_key]
axis = cfg['axis']
y_label = cfg['label']

joint = st.radio("Side" if variable_key == 'grf' else "Joint", cfg['joints'], horizontal=True)



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
if 'Ankle' in joint:
    movement_title = 'Dorsiflexion/Plantarflexion'
elif 'Knee' in joint:
    movement_title = 'Knee Flexion'
elif 'Hip' in joint:
    movement_title = 'Hip flexion'
else:
    movement_title = joint

if variable_key == 'powers':
    sign_note = 'Generation is positive, absorption is negative'
elif variable_key == 'grf':
    sign_note = None
elif 'Ankle' in joint:
    sign_note = 'Dorsiflexion is positive, plantarflexion is negative'
else:
    sign_note = 'Flexion is positive'

title_text = f'{movement_title} {variable_key.capitalize()}'
if sign_note:
    title_text += f'<br><sup>{sign_note}</sup>'
fig.update_layout(title=title_text)
fig.update_layout(
    xaxis=dict(
        title='% Gait Cycle',
        zeroline=False,
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        title=y_label,
        zeroline=True,
        zerolinecolor='#333',
        zerolinewidth=1,
        tickfont=dict(size=11),
        rangemode='tozero' if cfg['clip_zero'] else 'normal',
    ),
    legend=dict(
        borderwidth=1,
    ),
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

if variable_key== 'angles':
    st.markdown("There are two considerations when navigating these angle plots. The first is the ranges of the average joint angles across the shoes.\
                If this range is decreased, it is likely that the body subconciously employed a range of motion limitationa as a protection mechanism. This\
                is typically seen when the shoe is uncomfortable/causing pain, or fatigue is setting in. The second consideration is the variablity of the\
                joint angles across the trials, represented by the shaded region. If this shaded region becomes wider, it is likely that over the course of the session\
                technique was altered in some way for the same reasons listed that may change the magnitude of the curves. With this in mind, analysis of the shoes\
                can be made individually.")
    with st.expander("Spezial analysis"):
        st.image('images/adidas_spezial')
        st.markdown("The spezial showed a lower range of joint angles, and a wider spread of data than the other two shoes across the board. When this is\
                    considered in tandem with the reported discomfort of these shoes while running, it is highly likely that technique alterations were made in\
                    attempt to limit discomfort, which would reduce mechanical efficiency. This shoe would not be recommended for running performance.")
    with st.expander("Relentless Analysis"):
        st.image('images/nike_relentless_2.jpg')
        st.markdown("The Nike Relentless 2 showed similar joint angle values to the Pegasus Plus across the board, however this shoe showed a considerably greater\
                    variability in joint angles, particularily in the joints of the left side. Compared to the Spezial, however, the Relentless 2 showed a wider\
                    range of joint angles and a decreased spread of data suggesting that less technique alteration took place across the session,\
                    which makes sense with the larger comfort score, and greater mechancial efficiency resulted.")
    with st.expander("Pegasus Analysis"):
        st.image('images/pegasus_plus')
        st.markdown("The Nike Pegasus Plus showed a wide range of joint angles across all joints, generally in agreement with the Nike Relentless 2,\
                    however the Pegasus Plus displayed a very low spread of joint angle data, suggesting that the running movement was very repeatable across\
                    the entire session with this shoe, most likely in relation to the high level of comfort reported when running in this shoe.\
                     A normal range or joint angles and a low variation of these joint angles suggests that the pegasus plus resulted in a high level of\
                    mechancial efficiency, and this shoe can be recommended based on the joint angle data collected.")

events = load_events()


rows = []
for shoe_key, shoe_info in Shoes.items():
    events_df = events.get(shoe_key)
    if events_df is None:
        continue
    df = step_lengths(events_df)
    left = df[df['foot'] == 'L']
    right = df[df['foot'] == 'R']
    rows.append({
        'Shoe': shoe_info['name'],
        'Left step length (m)': round(left['step_length_m'].mean(), 3),
        'Right step length (m)': round(right['step_length_m'].mean(), 3),
        'Cadence (spm)': cadence(events_df),
    })
if rows:
    st.dataframe(pd.DataFrame(rows).set_index('Shoe'), width='content')



