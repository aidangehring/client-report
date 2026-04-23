#%%
import pandas as pd
import os
from utils.config import assets_path
import streamlit as st

@st.cache_data
def load_data():
    data={
        'angles': {},
        'moments':{},
        'powers':{},
        'grf': {},
    } 
    for data_type in data.keys():    
        for file in os.listdir(assets_path):
            if file.endswith('.csv') and file.startswith(f'{data_type}_'):
                shoe_name= file.replace(f'{data_type}_', '').replace('.csv', '')
                filepath= os.path.join(assets_path, file)
                try:
                    df= pd.read_csv(filepath,header=[0,1,4])
                    df=df.drop(columns=[col for col in df.columns if 'Unnamed' in str(col[0])])
                    df.columns= pd.MultiIndex.from_tuples(df.columns, names= ['Stat','Metric', 'Axis'])
                    df.index =range(101)
                    data[data_type][shoe_name]= df
                except Exception as e:
                    st.write(f"Failed to load {file}: {e}")
    return data

def get_series(data, data_type, shoe, joint, axis, stat='Mean'):
    df= data[data_type].get(shoe)
    if df is None: 
        return None
    label_map= {
        'angles': 'Angles',
        'moments': 'Moment',
        'powers': 'Power',
        'grf': 'GRF'
    }
    metric_label= f'{joint} {label_map[data_type]}'

    try: 
        return df[(stat, metric_label, axis)]
    except KeyError:
        st.write(f"Data not found for {shoe} - {joint} {data_type} {axis}")
        return None

def load_events():
    events = {}
    for file in os.listdir(assets_path):
        if file.endswith('.txt') and file.startswith('events_'):
            shoe_name = file.replace('events_', '').replace('.txt', '')
            filepath = os.path.join(assets_path, file)
            try:
                # Row 0: file paths, row 1: event types (header), row 2: EVENT_LABEL, row 3: ORIGINAL, row 4: ITEM zeros
                df = pd.read_csv(filepath, sep='\t', skiprows=[0, 2, 3, 4], header=0, index_col=0)
                df.columns = [
                    f'trial{i // 4 + 1}_{col.split(".")[0]}'
                    for i, col in enumerate(df.columns)
                ]
                events[shoe_name] = df
            except Exception as e:
                st.write(f"Failed to load {file}: {e}")
    return events



                

# %%

# %%
