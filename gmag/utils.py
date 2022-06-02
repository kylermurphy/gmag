# -*- coding: utf-8 -*-
"""
Simple set of utilites for reading in array locations

"""

import pandas as pd
import numpy as np
import os

import gmag


try:
    import igrf12
except ImportError:
    igrf12 = None
try:
    import aacgmv2
except ImportError:
    aacgmv2 = None


# TODO add code to generate stn text files by year

def l_dipole(cgm_lat):

    return 1. / (np.cos(np.deg2rad(cgm_lat))**2.)


def load_station_coor(
        param: str = 'GILL',
        year: int = 2000,
        col: str = 'code',
        path=False):
    """
    Returns cooridinate information for station data located in the Stations folder.
        Values returned are geographic and geomagnetic latitude and longitude, declination,
        l-shell (dipole), mlt of magnetic midnight (UT), mlt at 0 UT, and year.

    Parameters
    ----------
    param : str, optional
        [description], by default 'GILL'
    year : int, optional
        [description], by default 2000
    col : str, optional
        [description], by default 'code'
    path : str, optional
        [description], by default Stations directory of main folder'
    """
    if not path:
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'Stations')

    # station yearly file
    fn = os.path.join(path, '{0:04d}_station_cgm.txt'.format(year))

    if not os.path.exists(fn):
        return None
    
    # read in station data
    stn_dat = pd.read_csv(fn)

    if param.upper() != 'ALL' and param != '*':
        stn_dat = stn_dat[stn_dat[col.lower()] == param.upper()
                        ].reset_index(drop=True)

    
    stn_dat['year'] = year

    return stn_dat

def load_station_geo(
        param: str = 'GILL',
        col: str = 'code',
        path=False):

    """
    Returns geographic cooridinate information for station data located in the Stations folder

    Parameters
    ----------
    param : str, optional
        [description], by default 'GILL'
    year : int, optional
        [description], by default 'code'
    path : str, optional
        [description], by default Stations directory of main folder'
    """

    if not path:
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'Stations')

    # station file
    fn = os.path.join(path, 'station_list.csv')

    if not os.path.exists(fn):
        return None

    # read in station data
    stn_dat = pd.read_csv(fn, header=None, skiprows=1, 
                     names = ['array','code','name','latitude','longitude'])

    if param.upper() != 'ALL' and param != '*':
        stn_dat = stn_dat[stn_dat[col.lower()] == param.upper()
                        ].reset_index(drop=True)

    return stn_dat