import pandas as pd
import numpy as np
import scipy.signal as signal
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
    """Returns cooridinate information for station data located in the Stations folder.
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

    stn_dat = pd.read_csv(os.path.join(
        path, '{0:04d}_station_cgm.txt'.format(year)))

    stn_dat = stn_dat[stn_dat[col.lower()] == param.upper()
                      ].reset_index(drop=True)
    stn_dat['year'] = year

    return stn_dat
