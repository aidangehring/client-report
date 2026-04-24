import streamlit as st
# from utils.data_loader import load_data, get_series
# from utils.config import variable_options,axes, Shoes, variable_labels
# import plotly.graph_objects as go
# from utils.metrics import max_symmetry_index, impulse,loading_rate, min_symmetry_index

st.title("Injury Risk")
st.write ("This page will analyse kinetic and kinematic data collected\
          during the test, and point out any potential injury risks\
          associated with the 3 shoes. Examples could be rate of loading.")

# data= load_data()


# variable_key= st.radio("Variable", list(variable_options.keys()), format_func= lambda k: variable_options[k], horizontal=True)

# ctrl1, ctrl2, ctrl3= st.columns (3)

# with ctrl1:
#     if variable_key =='grf':
#         side =st.radio ("Side", ['Left', 'Right'])
#         joint=side
#     else:
#         joint= st.selectbox("Joint", joints)
# with ctrl2:
#     axis= st.radio ("Axis", axes, horizontal=True)

# y_label= variable_labels[variable_key]



# fig=go.Figure()

# for shoe_key, shoe_info in Shoes.items():
#     mean= get_series(data, variable_key, shoe_key, joint, axis, stat='Mean')
#     sd= get_series(data,variable_key, shoe_key, joint, axis, stat='Std Dev')
#     if mean is None:
#         continue
#     x= list(mean.index)
#     color= shoe_info['color']

#     if sd is not None: 
#         fig.add_trace (go.Scatter(
#             x=x + x[::-1],
#             y=list(mean+sd) + list((mean-sd).iloc[::-1]),
#             fill='toself',
#             fillcolor=color,
#             opacity= 0.12,
#             line=dict(width=0),
#             showlegend= False,
#             hoverinfo= 'skip',
#         ))

#     fig.add_trace(go.Scatter(
#         x=x,
#         y=mean,
#         name=shoe_info['name'],
#         line=dict(color=color, width=2.5),
#         hovertemplate= f"<b>{shoe_info['name']}</b><br>%{{x}}% GC<br>%{{y:.2f}}<extra></extra>"
#     ))

# fig.update_layout(
#     xaxis=dict(
#         title='% Gait Cycle',
#         zeroline=False,
#         tickfont=dict(size=11),
#     ),
#     yaxis=dict(
#         title= y_label,
#         zeroline=True,
#         zerolinecolor= '#333',
#         zerolinewidth=1,
#         tickfont=dict(size=11),
#     ),
#     legend=dict(
#         borderwidth=1,
#     )
# )

# if variable_key=='angles':
#     with st.expander("Max Angle Symmetry", expanded=False):
#         if 'Left' in joint and 'angles' in variable_key:
#             right_joint=joint.replace('Left', 'Right')
#             sym_cols=st.columns(3)
#             for col, (shoe_key,shoe_info) in zip(sym_cols,Shoes.items()):
#                 left_s= get_series(data,variable_key,shoe_key,joint,axis)
#                 right_s= get_series(data,variable_key,shoe_key, right_joint,axis)
#                 si=max_symmetry_index(left_s,right_s)
#                 with col: 
#                     st.markdown(f"**{shoe_info['name']}**")
#                     st.metric("Symmetry of sides", f"{si:.1f}%" if si is not None else "N/A")
#         if 'Right' in joint and 'angles' in variable_key:
#             left_joint= joint.replace('Right', 'Left')
#             sym_cols=st.columns(3)
#             for col, (shoe_key,shoe_info) in zip(sym_cols,Shoes.items()):
#                 right_s= get_series(data,variable_key,shoe_key,joint,axis)
#                 left_s=get_series(data,variable_key,shoe_key,left_joint,axis)
#                 si=max_symmetry_index(right_s,left_s)
#                 with col: 
#                     st.markdown(f"**{shoe_info['name']}**")
#                     st.metric("Symmetry of sides", f"{si:.1f}%" if si is not None else "N/A")
#     with st.expander("Minimum Angle Symmetry", expanded=False):
#         if 'Left' in joint and 'angles' in variable_key:
#             right_joint=joint.replace('Left', 'Right')
#             sym_cols=st.columns(3)
#             for col, (shoe_key,shoe_info) in zip(sym_cols,Shoes.items()):
#                 left_s= get_series(data,variable_key,shoe_key,joint,axis)
#                 right_s= get_series(data,variable_key,shoe_key, right_joint,axis)
#                 si=min_symmetry_index(left_s,right_s)
#                 with col: 
#                     st.markdown(f"**{shoe_info['name']}**")
#                     st.metric("Symmetry of sides", f"{si:.1f}%" if si is not None else "N/A")
#         if 'Right' in joint and 'angles' in variable_key:
#             left_joint= joint.replace('Right', 'Left')
#             sym_cols=st.columns(3)
#             for col, (shoe_key,shoe_info) in zip(sym_cols,Shoes.items()):
#                 right_s= get_series(data,variable_key,shoe_key,joint,axis)
#                 left_s=get_series(data,variable_key,shoe_key,left_joint,axis)
#                 si=min_symmetry_index(right_s,left_s)
#                 with col: 
#                     st.markdown(f"**{shoe_info['name']}**")
#                     st.metric("Symmetry of sides", f"{si:.1f}%" if si is not None else "N/A")

# if variable_key== 'grf':
#     with st.expander("Impulse", expanded=False):
#         if 'Left' in joint and 'grf' in variable_key:
#             imp_cols= st.columns(3)
#             for col, (shoe_key,shoe_info) in zip(imp_cols, Shoes.items()):
#                 left_i=get_series(data,variable_key,shoe_key,joint,axis)
#                 imp= impulse(left_i)
#                 with col:
#                     st.markdown(f"**{shoe_info['name']}**")
#                     st.metric("Impulse over one stride", f"{imp:.1f}J" if imp is not None else "N/A")
#     with st.expander("Loading Rate", expanded=False):
#         lr_cols = st.columns(3)
#         for col, (shoe_key, shoe_info) in zip(lr_cols, Shoes.items()):
#             grf_series = get_series(data, 'grf', shoe_key, joint, axis, stat='Mean')
#             lr = loading_rate(grf_series)
#             with col:
#                 st.markdown(f"**{shoe_info['name']}**")
#                 st.metric("Loading Rate", f"{lr:.2f}" if lr is not None else "N/A")





# st.plotly_chart(fig, width='stretch')