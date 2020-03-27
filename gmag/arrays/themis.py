
# -*- coding: utf-8 -*-
"""

This module supports data from the THEMIS magnetometer array. Downloads data from THEMIS website.
Loads XYZ data and rotates into HDZ.

Example
-------


Attributes
----------
local_dir : str
    Directory for IMAGE data. This directory will be used to download and load IMAGE files.
http_dir : str
    Web address for IMAGE data. This points to the website of the IMAGE data form.


Notes
-----
    THEMIS CDF files are generally in HDZ and so XYZ data is not returned.

    Acknowledgement: S. Mende and C. T. Russell for use of the GMAG data 
    and NSF for support through grant AGS-1004814.

References
----------


"""


import os
import pandas as pd
import numpy as np

import gmag

from gmag import utils
from urllib.parse import urljoin

local_dir = os.path.join(gmag.config_set['data_dir'],'magnetometer\\THEMIS\\')
http_dir = gmag.config_set['th_http']

# check if local dir exists
if not os.path.exists(local_dir):
    try:
        os.makedirs(local_dir)
    except FileNotFoundError:
        print('Local THEMIS Drive does not exist')


def list_files(site,
               sdate,
               ndays=1,
               edate=None):
    """Return a Pandas DataFrame containing the date, file name, and directory
     for every file. Assume filename is generated for every day.

     Used to generate a list of files for either downloading or loading

     Directory structure is assumed
     local_dir\\YYYY\\MM\\DD\\filename

    Parameters
    ----------
     site : str
         Magnetometer site to load file names for
     sdate : str or datetime-like
         Initial day to be loaded
     ndays : int, optional
         Number of days to be listed  (the default is 1, which will create a DataFram for a single file)
     edate : str, optional
         Last day in generated list (the default is None, which will defualt to ndays)

     Returns
     -------
     f_df : DataFrame
         Pandas dataframe with columns date (file date), fname (file name), fdir (file directory),
         hdir (http directory)
    """

    # create a panda series of dates
    if edate is not None:
        d_ser = pd.Series(pd.date_range(start=sdate, end=edate, freq='D'))
    else:
        d_ser = pd.Series(pd.date_range(
            start=sdate, periods=ndays, freq='D'))

    f_df = pd.DataFrame(columns=['date', 'fname', 'dir','hdir'])

    # create file name and directory structure
    for di, dt in d_ser.iteritems():
        # filename
        fnm = '{0:04d}{1:02d}{2:02d}'.format(
            dt.year, dt.month, dt.day)
        fnm = 'thg_l2_mag_'+site.lower()+'_'+fnm+'_v01.cdf'


        # directory location
        # THEMIS data is store in local_dir as YYYY\MM\DD\themis_file
        fdr = os.path.join(local_dir,
                           '{0:04d}'.format(dt.year),
                           '{0:02d}'.format(dt.month),
                           '{0:02d}'.format(dt.day))
        if not os.path.exists(fdr):
            os.makedirs(fdr)

        # http directory
        hdr = http_dir+'thg/l2/mag/'+site.lower()+'/{0:04d}/'.format(dt.year)

        f_df = f_df.append(
            {'date': dt, 'fname': fnm, 'dir': fdr, 'hdir':hdr}, ignore_index=True)

    return f_df


def download():
    pass


def load(site: str = ['KUUJ'],
         sdate='2010-01-01',
         ndays: int = 1,
         edate=None,
         dl=False):

    if type(site) is str:
        site = [site]

    # create empty data frame for data
    d_df = pd.DataFrame()
    for stn in site:
        # get list of file names
        f_df = list_files(stn.upper(), sdate, ndays=ndays, edate=edate)

        s_df = pd.DataFrame()
        for di, row in f_df.iterrows():
            print(os.path.join(row['dir'], row['fname']))

            # get file name and check
            # if it exists
            fn = os.path.join(row['dir'], row['fname'])
            if not os.path.exists(fn):
                print('File does not exist: {0}'.format(fn))
                if dl:
                    print('Downloading:')
                    download()
                    if not os.path.exists(fn):
                        print('File could not be downloaded')
                        continue
                else:
                    continue

            i_df = pd.read_fwf(fn, header=None, skiprows=1,
                               names=['t',
                                      stn.upper()+'_X',
                                      stn.upper()+'_Y',
                                      stn.upper()+'_Z',
                                      stn.upper()+'_flag'],
                               widths=[14, 10, 10, 10, 2],
                               compression=comp)

            try:
                i_df['t'] = pd.to_datetime(i_df['t'],
                                           format='%Y%m%d%H%M%S')
            except:
                continue
            i_df = i_df.set_index('t')

            s_df = s_df.append(i_df)

        # clean data
        if not s_df.empty:
            c_df = clean(s_df)
        # append files
        if d_df.empty:
            d_df = c_df
        else:
            d_df = d_df.join(c_df)

    # rotate data into HDZ
    if d_df.empty:
        return None

    r_df = rotate(d_df, site, sdate)

    return r_df


def clean(i_df):

    # get a list of column names
    c_name = list(i_df.columns.values)
    # find the flag column
    flag = next((s for s in c_name if 'flag' in s), None)
    zcom = next((s for s in c_name if '_Z' in s), None)
    # find bad data
    # flag is '.' for good
    # anything else is bad
    if flag:
        i_df.loc[i_df[flag] != '.', 0:3] = np.nan
    # z component should always
    # be positive
    if zcom:
        i_df.loc[i_df[zcom] < 0, 0:3] = np.nan

    return i_df


def rotate(i_df,
           site,
           date):

    dt = pd.to_datetime(date)
    # get a list of column names
    c_name = list(i_df.columns.values)

    for stn in site:
        stn = stn.upper()
        if stn+'_X' not in c_name:
            continue

        stn_dat = utils.load_station_coor(param=stn, year=dt.year)
        dec = float(stn_dat['declination'])

        h = i_df[stn+'_X'].astype(float) * np.cos(np.deg2rad(dec)) + \
            i_df[stn+'_Y'].astype(float) * np.sin(np.deg2rad(dec))
        d = i_df[stn+'_Y'].astype(float) * np.cos(np.deg2rad(dec)) - \
            i_df[stn+'_X'].astype(float) * np.sin(np.deg2rad(dec))

        i_df[stn+'_H'] = h
        i_df[stn+'_D'] = d

        # fill in station cooridinat info
        # this would be better as metadata
        # but not possible in pandas
        i_df[stn+'_declination'] = float(stn_dat['declination'])
        i_df[stn+'_cgmlat'] = float(stn_dat['cgm_latitude'])
        i_df[stn+'_cgmlon'] = float(stn_dat['cgm_longitude'])
        i_df[stn+'_lshell'] = float(stn_dat['lshell'])
        i_df[stn+'_mlt'] = float(stn_dat['mlt_midnight'])

    return i_df

