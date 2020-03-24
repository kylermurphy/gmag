import heliopy.data.omni as omni
import numpy as np
import pandas as pd


def load(sdate,
         edate,
         var=['Bx GSE, GSM',
              'By GSM',
              'Bz GSM',
              'Proton Density',
              'Plasma Flow Speed',
              'Flow Pressure',
              'Kp',
              'DST Index',
              'AE Index',
              'f10.7 index']):

    sdate = pd.to_datetime(sdate)
    edate = pd.to_datetime(edate)

    o_dat = omni.low(sdate, edate)

    if var is not None:
        o_dat = o_dat.data[var]
    else:
        o_dat = o_dat.data

    c_df = clean(o_dat.copy())
    c_df.columns = c_df.columns.str.replace(',', '')
    c_df.columns = c_df.columns.str.replace('.', '')
    c_df.columns = c_df.columns.str.replace(' ', '_')

    return c_df


def clean(i_df):

    # dictionary of data columns
    # and value to replace
    o_d = {
        'Bx GSE, GSM': 999.9,
        'By GSM': 999.9,
        'Bz GSM': 999.9,
        'Proton Density': 999.9,
        'Plasma Flow Speed': 9999.,
        'Flow Pressure': 99.99,
        'Kp': 99,
        'DST Index': 99999,
        'AE Index': 9999
    }

    for k, kval in o_d.items():
        i_df.loc[i_df[k] >= kval, k] = np.nan

    return i_df
