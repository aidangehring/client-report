import os
import streamlit as st
from utils.data_loader import load_data, get_series, load_events
from utils.config import variable_options, variable_config, Shoes, sagittal_info, images_path
import plotly.graph_objects as go
from utils.metrics import peak_power_gen, step_lengths, cadence
import pandas as pd
st.title("Analysis")
st.write("This page will analyse the performance of the 3 shoes based on kinetic and kinematic data collected during the testing sessions.\
         Because running, especially on a treadmill as was completed in this protocol, is predominantly involving forward progression this report\
         will mainly be focused on dorsiflexion/plantarflexion of the ankle and flexion/extension of the hip and knee joints. \
         Detailed explanations for all of these movements can be explored using the appropriate buttons below.")
with st.expander("For full transparency, raw data not included in this report has been prepped for visualisation as well, and can be viewed here."):
    st.markdown("[View full dataset](https://7115-footwear-repository-p99ez7xmgdwyfiq3psbpsk.streamlit.app/)")
    
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
elif 'Ankle' in joint and variable_key == 'moments':
    sign_note = 'Plantarflexion is positive, dorsiflexion is negative'
elif 'Ankle' in joint:
    sign_note = 'Dorsiflexion is positive, plantarflexion is negative'
else:
    sign_note = 'Flexion is positive'

title_text = f'{movement_title} {variable_options[variable_key]}'
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








events = load_events()
rows = []
for shoe_key, shoe_info in Shoes.items():
    events_df = events.get(shoe_key)
    if events_df is None:
        continue
    df = step_lengths(events_df)
    left_steps = df[df['foot'] == 'L']
    right_steps = df[df['foot'] == 'R']
    rows.append({
        'Shoe': shoe_info['name'],
        'Left step length (m)': round(left_steps['step_length_m'].mean(), 3),
        'Right step length (m)': round(right_steps['step_length_m'].mean(), 3),
        'Cadence (spm)': cadence(events_df),
        'Rating of perceived exertion (RPE)': shoe_info['RPE']
    })

st.plotly_chart(fig, width='stretch')
#* Angles
if variable_key == 'angles':
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
#* Moments
if variable_key == 'moments':
    st.markdown('Moments are a complex representation of how much force is required to either stablize or rotate a joint. Through a process called inverse\
                dynamics, forces measured at the force plate are resolved to determine how much force is required at each joint depending on the angle of that joint,\
                for that joint to remain stable. If greater moments are felt in the joints, especially those higher up the body like the knees and hips, than less force is\
                being dissipated by the shoes, and the muscles are required to produce more force may lead to overuse injury over time. Moments can increase\
                or decrease either by increased/decreased force requirments, or changes in joint angle.')
    with st.expander('Spezial analysis'):
        st.image('images/adidas_spezial')
        st.markdown('The Spezial displayed the lowest joint moments of the three shoes at both the ankle and the knee. When the low angles and low comfort\
                    observed are taken into account, the low moments observed are likely an adaptation made to reduce the moments about the joints due to\
                     discomfort, rather than mechanical efficiency and should not necessarilly be considered positive.')
    with st.expander('Relentless analysis'):
        st.image('images/nike_relentless_2.jpg')
        st.markdown('The Relentless 2 displayed the greatest joint moments across the 3 shoes. When comapring this to the results of the Pegasus Plus, across\
                    similar joint angles this suggests that there was a greater force requirment from the muscles to stabilize the joints compared to the\
                    Pegasus shoe, which may lead to a higher risk of oversue injury over time.')
    with st.expander('Pegasus analysis'):
        st.image('images/pegasus_plus')
        st.markdown('The Pegasus Plus displayed joint moments between the Spezial and the Relentless 2 across all joints. Because the lower joint moments\
                    observed with the spezial is not necessarilly considered to be a positive, the lower magnitude of joint moments in the Pegasus shoes compared\
                    to the Relentless 2 suggests that the Pegasus shoe is recommended based on joint moment outputs.')
#* Powers
if variable_key == 'powers':
    st.markdown('The power plots represent whether the ankle is generating power for propulsion or absorbing energy during landing. A higher power absorption\
                 is represented by a larger negative value in the power curve, and means that the muscles are working harder to absorb the load of the impact.\
                Conversely, as power generation increases the muscles are working harder to generate propulsive forces.')
    with st.expander('Spezial analysis'):
        st.image('images/adidas_spezial')
        st.markdown('The Spezial showed the lowest power generation and absorption of the three shoes. A key comparison here is with step length:\
                     if a shoe were highly efficient, lower power output could still maintain step length because the shoe would be contributing to\
                     propulsion. However, with the Spezial, both power output and step length were reduced together. This suggests the lower power was\
                     not a sign of efficiency, but rather that the runner was subconsciously reducing effort to manage discomfort which would also\
                     explain the shorter steps.')
    with st.expander('Relentless analysis'):
        st.image('images/nike_relentless_2.jpg')
        st.markdown('The Nike Relentless 2 showed the greatest power generation and absorption of the three shoes. Despite this, when compared\
                     to the Pegasus Plus, the Relentless produced a similar or slightly shorter step length. This means the runner was using considerably\
                     more energy to cover roughly the same distance per step, which is a sign of lower mechanical efficiency. Based on the power and step\
                     length data, the Relentless 2 is the least efficient of the two performance shoes.')
    with st.expander('Pegasus analysis'):
        st.image('images/pegasus_plus')
        st.markdown('The Nike Pegasus Plus showed a power generation and absorption which was greater than the Adidas Spezial, but less than the\
                    Nike Relentless 2. Because the Pegasus displayed a step length greater than the Spezial, the decreased magnitude of the power curve in the\
                    Spezial should not be considered advantageous over the Pegasus shoe. Compared to the Relentless 2, the pegasus showed similar or greater step\
                    length at a lower power requirement, suggesting this shoe provides superior efficicency and is recommended based on the power outputs.')
#* GRF
if variable_key == 'grf':
    st.markdown('GRF, or ground reaction force, represents the force being applied to the ground by the runner. A higher ground reaction force means that\
                the runner is pushing into the ground with more force. A larger ground reaction force may mean that the runner is producing more force\
                during their stride, but if this force is not dispersed in an efficient way, it may increase the force required at the joints to \
                maintain stability.')
    with st.expander('Spezial analysis'):
        st.image('images/adidas_spezial')
        st.markdown('The Adidas Spezial displayed the lowest ground reaction force of the 3 shoes. When considered in context with all other variables for this\
                    shoe, it appears that the reduced ground reaction force is a result of altered mechancis to limit the strain placed on the joints due to\
                    the level of discomfort during the run in this shoe. Additionally, the large width of the shaded band for this shoe suggests that there was\
                    a large variation in how the ground was contacted, further suggesting that technique was modified over the course of the trial.')
    with st.expander('Relentless analysis'):
        st.image('images/nike_relentless_2.jpg')
        st.markdown('The Relentless 2 produced ground reaction forces similar to the Pegasus Plus, meaning both shoes generated roughly the same amount\
                     of force into the ground during running. However, the Relentless consistently required higher joint moments across all joints to\
                     achieve this. In other words, the muscles had to work harder to resolve the same forces which is a sign of lower mechanical efficiency\
                     compared to the Pegasus Plus.')
    with st.expander('Pegasus analysis'):
        st.image('images/pegasus_plus')
        st.markdown('The Pegasus Plus displayed a ground reaction force greater than the Adidas Spezial, and similar to the Nike Reletnless 2. Becasue the\
                    Spezial appears to display dcreased GRF due to altered technique, direct comparisons between the Pegasus and the Relentless are\
                    warranted. The main comparison to be drawn is the relation of the simialr GRF outputs to the joint moment curves for these shoes.\
                    The Pegasus Plus displayed consitently lower joint moments compared to the Relentless despite the similar GRF outputs, suggesting that the\
                    Pegasus Plus offers a superior mechncial efficiency, and is therefore recommended based on the results of the GRF curves.')

st.subheader("Metrics")
if rows:
    def color_metrics(row):
        def color(val):
            if 'step length' in row.name.lower():
                if val <= 0.95:
                    return 'background-color: #c0392b; color: white'
                elif val <= 0.98:
                    return 'background-color: #d4a017; color: white'
                else:
                    return 'background-color: #27ae60; color: white'
            elif 'cadence' in row.name.lower():
                if val >= 171:
                    return 'background-color: #c0392b; color: white'
                elif val >= 170:
                    return 'background-color: #d4a017; color: white'
                else:
                    return 'background-color: #27ae60; color: white'
            elif 'rpe' in row.name.lower():
                if val >= 7:
                    return 'background-color: #c0392b; color: white'
                elif val == 6:
                    return 'background-color: #d4a017; color: white'
                else:
                    return 'background-color: #27ae60; color: white'
            return ''
        return [color(v) for v in row]

    df_metrics = pd.DataFrame(rows).set_index('Shoe').T
    styled = (df_metrics.style
        .apply(color_metrics, axis=1)
        .format('{:.3f}', subset=pd.IndexSlice[['Left step length (m)', 'Right step length (m)'], :])
        .format('{:.1f}', subset=pd.IndexSlice[['Cadence (spm)'], :])
        .format('{:.0f}', subset=pd.IndexSlice[['Rating of perceived exertion (RPE)'], :])
    )
    st.dataframe(styled, use_container_width=True)
with st.expander("RPE scale"):
    st.image('images/borg_scale.avif')
st.markdown('The metrics table outlines some color coordinated key values, where green is the best outcomes of the shoes, red the least optimal, and \
            yellow in between these values. These ratings are used to help analyse the ouputs of the force and movement data. ')



