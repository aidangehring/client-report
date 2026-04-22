#%%
import streamlit as st
import pandas as pd
from utils.config import assets_path,client_weight


from utils.data_loader import load_data, get_series
import numpy as np


#%%
data= load_data()
# %%
def impulse(series): 
    if series is None:
        return None
    series_newtons=series/100*client_weight
    return np.trapezoid(series_newtons)



def work(series):
    if series is None: 
        return None
    return np.trapezoid(series)

def peak_power_gen(series):
    if series is None: 
        return None
    return series.max()

def loading_rate(series, stance_end=40):

    if series is None or not isinstance(series, pd.Series):
        return None
    
    early_stance=series.iloc[:20]
    rate=(early_stance.max()-early_stance.iloc[0])/20
    
    return round(rate, 4)

def symmetry_index(left_series, right_series):
    if left_series is None or right_series is None:
        return None
    left_peak= left_series.max()
    right_peak= right_series.max()
    if (left_peak-right_peak) == 0:
        return None
    si=abs(left_peak-right_peak)/((left_peak+right_peak)/2)*100
    return round (si,2)

    