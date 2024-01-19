# -*- coding: utf-8 -*-
"""

This module supports data from the CANOPUS (now CARISMA) magnetometer array.

Directory structure is assumed
local_dir\\magnetometer\\CANOPUS\\YYYY\\MM\\SITE\\file

local_dir is set in gmagrc

Example
-------

Load data from multiple stations
df = canopus.load(site=['GILL','ISLL','PINA'],sdate='2012-01-01',ndays=1)

Attributes
----------
local_dir : str
    Directory for CANOPUS data. This directory will be used to download and load CANOPUS files.

Notes
-----
    CANOPUS data is downloaded in XYZ coordinates and rotated to HDZ. The rotation uses data loaded
    from the text files in the Stations directory and the function gmag.load_station_coor().

    Acknowledgement: I.R. Mann, D.K. Milling and the rest of the CARISMA team for use of GMAG data.
    CARISMA is operated by the University of Alberta, funded by the Canadian Space Agency.

References
----------
.. [1] Mann, I. R., Milling, D. K., Rae, I. J., Ozeke, L. G., Kale, A., Kale, Z. C., … Singer, H. J. (2008).
   The Upgraded CARISMA Magnetometer Array in the THEMIS Era. Space Science Reviews, 141(1–4), 413–451.
   https://doi.org/10.1007/s11214-008-9457-6

"""

import os
import requests
import pandas as pd
import numpy as np

import gmag

from gmag import utils


local_dir = os.path.join(
    gmag.config_set['data_dir'], 'magnetometer', 'CANOPUS')
http_dir = False
pi = 'Ian Mann'
pi_i = 'University of Alberta'

# check if local dir exists
if not os.path.exists(local_dir):
    try:
        os.makedirs(local_dir)
    except FileNotFoundError:
        print('Local CANOPUS Drive does not exist')


def list_files(site,
               sdate,
               ndays=1,
               edate=None,
               gz=True):
    """Return a Pandas DataFrame containing the date, file name, and directory
     for every file. Assume filename is generated for every day.

     Used to generate a list of files for either downloading or loading

     Directory structure is assumed
     local_dir\\magnetometer\\CANOPUS\\YYYY\\MM\\SITE\\file

    Parameters
    ----------
     site : str
         Magnetometer site to load file names for
     sdate : str or datetime-like
         Initial day to be loaded
     ndays : int, optional
         Number of days to be listed  (the default is 1, which will create a DataFram for a single file)
     edate : str or datetime-like, optional
         Last day in generated list (the default is None, which will defualt to ndays)
     gz : bool, optional
         Create gzipped filenames(the default is True)

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

    f_df = pd.DataFrame(columns=['date', 'fname', 'dir', 'hdir'])

    # create file name and directory structure
    for di, dt in d_ser.items():
        # filename
        fnm = '{0:04d}{1:02d}{2:02d}'.format(
            dt.year, dt.month, dt.day)
        fnm = fnm+site.upper()+'.MAG'
        if gz:
            fnm = fnm + '.gz'

        # directory location
        # CANOPUS data is store in local_dir as YYYY\MM\SITE\canopus_file
        fdr = os.path.join(local_dir,
                           '{0:04d}'.format(dt.year),
                           '{0:02d}'.format(dt.month),
                           '{0}'.format(site.upper()))
        if not os.path.exists(fdr):
            os.makedirs(fdr)

        # http directory
        # currently no way to download data
        if http_dir:
            hdr = http_dir+'FGM/1Hz/'+'{0:04d}'.format(dt.year)+'/'
            hdr = hdr+'{0:02d}'.format(dt.month) + \
                '/'+'{0:02d}'.format(dt.day)+'/'
        else:
            hdr = False

        # Create a dataframe row for this site/date and append to answer
        curr_file_df = pd.DataFrame( {'date': dt, 'fname': fnm, 'dir': fdr, 'hdir': hdr}, index = [0])
        f_df = pd.concat( [ f_df, curr_file_df], ignore_index=True)

    # CANOPUS only goes to 2005-04-01
    # after this the data transitions to
    # CARISMA data
    # remove rows past this
    f_df = f_df[f_df['date'] < pd.to_datetime('2005-04-01')]

    return f_df


def download(site=None,
             sdate=None,
             ndays=1,
             edate=None,
             f_df=None,
             force=False,
             verbose=True):
    """
    No http dir to download files yet
    """


def load(site: str = ['GILL'],
         sdate='1998-01-01',
         ndays: int = 1,
         edate=None,
         gz=True,
         dl=True,
         drop_flag=True,
         force=False):
    """Loads CANOPUS MAG files and MAG.gz files

    Parameters
    ----------
    site : str, optional
        Site or list of sites to load, by default ['GILL']
    sdate : str, optional
        Start day to load, by default '2010-01-01'
    ndays : int, optional
        Number of days to load, by default 1
    edate : str or datetime-like, optional
        End day to load, by default None
    gz : bool, optional
        Load gzip files, by default True
    dl : bool, optional
        Download files if they don't exist, by default True
    drop_flag : bool, optional
        Drop flag columns before returning DataFrame
    force : bool, optional
        Force downloading files again, by default False

    Returns
    -------
    Pandas DataFrame
        Cleaned and rotated (if possible) CANOPUS magnetometer data and metadata
    """

    if type(site) is str:
        site = [site]
    if gz:
        comp = 'gzip'
    else:
        comp = 'infer'

    # create empty data frame for data
    d_df = pd.DataFrame()
    for stn in site:
        # get list of file names
        f_df = list_files(stn.upper(), sdate, ndays=ndays, edate=edate, gz=gz)

        if dl:
            print('Downloading Data:')
            download(f_df=f_df, force=force)

        # data frame to store site data
        s_df = pd.DataFrame()
        for di, row in f_df.iterrows():
            print('Loading: '+os.path.join(row['dir'], row['fname']))

            # get file name and check
            # if it exists
            fn = os.path.join(row['dir'], row['fname'])
            if not os.path.exists(fn):
                print('File does not exist: {0}'.format(fn))
                continue

            i_df = pd.read_fwf(fn, header=None, skiprows=40,
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
            s_df = pd.concat([s_df, i_df])

        # clean data
        if not s_df.empty:
            c_df = clean(s_df)
        else:
            continue
        # append files
        if d_df.empty:
            d_df = c_df
        else:
            d_df = d_df.join(c_df,how='outer')

    # rotate data into HDZ
    if d_df.empty:
        return None

    r_df, meta_df = rotate(d_df, site, sdate)

    #get the nominal resolution of the dataframe
    res = (pd.Series(r_df.index[1:]) -
               pd.Series(r_df.index[:-1])).value_counts()
    res = res.index[0].total_seconds()

    #add PI to metadata
    meta_df['Time Resolution'] = res 
    meta_df['Coordinates'] = 'Geographic North - X, Eas - Y, Vertical Down - Z, Geomagnetic North - H, East- D, Vertical Down - Z'
    meta_df['PI'] = pi
    meta_df['Institution'] = pi_i

    #drop flag column
    if drop_flag: 
        r_df = r_df[r_df.columns.drop(list(r_df.filter(regex='flag')))]

    return r_df, meta_df


def clean(i_df):
    """Remove bad data from CANOPUS DataFrame

    This is a function so that additional utility can
    be easily added.

    Parameters
    ----------
    i_df : DataFrame
        CANOPUS magnetometer data loaded with CANOPUS.load()

    Returns
    -------
    c_df : DataFrame
        Cleaned CANOPUS magnetometer data
    """
    # get a list of column names
    c_name = list(i_df.columns.values)
    # find the flag column
    flag = next((s for s in c_name if 'flag' in s), None)
    xcom = next((s for s in c_name if '_X' in s), None)
    ycom = next((s for s in c_name if '_Y' in s), None)
    zcom = next((s for s in c_name if '_Z' in s), None)

    # find bad data
    # flag is '.' for good
    # anything else is bad
    if flag:
        i_df.iloc[i_df[flag] != '.', 0:3] = np.nan
    # z component should always
    # be positive and less then 99999.992
    if zcom:
        i_df.iloc[i_df[zcom] < 0, 0:3] = np.nan
        i_df.iloc[i_df[zcom] > 99999, 0:3] = np.nan
    # x and yshould always be less then
    # 99999.992
    if xcom:
        i_df.iloc[i_df[xcom] > 99999, 0:3] = np.nan
    if ycom:
        i_df.iloc[i_df[ycom] > 99999, 0:3] = np.nan

    return i_df


def rotate(i_df,
           site,
           date):
    """Rotate XYZ to HDZ for select sites, append
    to existing DataFrame and return

    Parameters
    ----------
    i_df : DataFrame
        CANOPUS magnetometer data loaded with image.load()
    site : site to rotate
        List of sites to rotate
    date : str or datetime-like
        Date to load declination for

    Returns
    -------
    i_df : DataFrame
        DataFrame with HD magnetic field coordinates
        and station cgm coordinates, lshell and 
        declination
    """
    dt = pd.to_datetime(date)
    # get a list of column names
    c_name = list(i_df.columns.values)

    #create dataframe for metadata
    meta = pd.DataFrame(columns=['array', 'code', 'name', 'latitude', 'longitude', 'cgm_latitude',
       'cgm_longitude', 'declination', 'lshell', 'mlt_midnight', 'mlt_ut',
       'year'])

    #get station data for CARISMA array
    stn_cgm = utils.load_station_coor(param='CARISMA',col='array', year=dt.year)   
    # if the stn_dat can't be found don't rotate
    # but still return meta data
    if stn_cgm is None:
        geo_stn = utils.load_station_geo(param='CARISMA',col='array')
        for stn in site:
            stn_dat = geo_stn[geo_stn['code'] == stn.upper()].reset_index(drop=True)
            meta = pd.concat([meta,stn_dat], axis=0, sort=False, ignore_index=True)

        return i_df, meta   

    for stn in site:
        stn = stn.upper()
        if stn+'_X' not in c_name:
            continue

        stn_dat = stn_cgm[stn_cgm['code'] == stn].reset_index(drop=True)
        dec = float(stn_dat['declination'])

        h = i_df[stn+'_X'].astype(float) * np.cos(np.deg2rad(dec)) + \
            i_df[stn+'_Y'].astype(float) * np.sin(np.deg2rad(dec))
        d = i_df[stn+'_Y'].astype(float) * np.cos(np.deg2rad(dec)) - \
            i_df[stn+'_X'].astype(float) * np.sin(np.deg2rad(dec))

        i_df[stn+'_H'] = h
        i_df[stn+'_D'] = d

        # add meta data to data frame
        meta = pd.concat([meta,stn_dat], axis=0, sort=False, ignore_index=True)

    return i_df, meta
