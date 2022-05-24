# -*- coding: utf-8 -*-
"""

This module supports data from the CARISMA magnetometer array. Downloads data from CARISMA website.
Loads XYZ data and rotates into HDZ. Will load data downloaded from the CARISMA website.

Directory structure is assumed
local_dir\\magnetometer\\CARISMA\\YYYY\\MM\\DD\\file

local_dir is set in gmagrc

Example
-------

Load and download data from multiple stations
df = carisma.load(site=['GILL','ISLL','PINA'],sdate='2012-01-01',ndays=1)

You can download data a site at time with carisma.download, though its
easier to use carisma.load as it will loop through stations


Attributes
----------
local_dir : str
    Directory for CARISMA data. This directory will be used to download and load CARISMA files.
http_dir : str
    Web address for CARISMA data. This points to the website of CARSIMA data.


Notes
-----
    CARISMA data is downloaded in XYZ coordinates and rotated to HDZ. The rotation uses data loaded
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


local_dir = os.path.join(gmag.config_set['data_dir'],'magnetometer','CARISMA')
http_dir = gmag.config_set['ca_http']

# check if local dir exists
if not os.path.exists(local_dir):
    try:
        os.makedirs(local_dir)
    except FileNotFoundError:
        print('Local CARISMA Drive does not exist')


def list_files(site,
               sdate,
               ndays=1,
               edate=None,
               gz=True):
    """Return a Pandas DataFrame containing the date, file name, and directory
     for every file. Assume filename is generated for every day.

     Used to generate a list of files for either downloading or loading

     Directory structure is assumed
     local_dir\\magnetometer\\CARISMA\\YYYY\\MM\\DD\\file

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
    for di, dt in d_ser.iteritems():
        # filename
        fnm = '{0:04d}{1:02d}{2:02d}'.format(
            dt.year, dt.month, dt.day)
        fnm = fnm+site.upper()+'.F01'
        if gz:
            fnm = fnm + '.gz'

        # directory location
        # CARISMA data is store in local_dir as YYYY\MM\DD\carsima_file
        fdr = os.path.join(local_dir,
                           '{0:04d}'.format(dt.year),
                           '{0:02d}'.format(dt.month),
                           '{0:02d}'.format(dt.day))
        if not os.path.exists(fdr):
            os.makedirs(fdr)

        # http directory
        hdr = http_dir+'FGM/1Hz/'+'{0:04d}'.format(dt.year)+'/'
        hdr = hdr+'{0:02d}'.format(dt.month)+'/'+'{0:02d}'.format(dt.day)+'/'
                


        f_df = f_df.append(
            {'date': dt, 'fname': fnm, 'dir': fdr, 'hdir':hdr}, ignore_index=True)

    return f_df


def download(site=None,
             sdate=None,
             ndays=1,
             edate=None,
             f_df=None,
             force=False,
             verbose=True):
    """Download CARISMA magnetometer data from the CARISMA website
    
    Requires wget to download data.

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
    f_df: DataFrame 
        List of files to be loaded
    force: bool, optional
        Force download even if file exists
    verbose : bool, optional
        Outputs some additional information, by default 0
    """

    # get file names
    if f_df is None: 
        f_df = list_files(site, sdate, ndays=ndays, edate=edate)   
    # download files
    for di, row in f_df.iterrows():
        # get file name and check
        # if it exists
        # only download if force=True
        fn = os.path.join(row['dir'], row['fname'])
        if not os.path.exists(fn) or force:
            # check for online file, if it exists
            #get it
            ureq = requests.get(row['hdir']+row['fname'], timeout=5.0)
            if ureq.ok:
                print('Downloading {0}'.format(row['hdir']+row['fname']))
                open(fn,'wb').write(ureq.content)
            else:
                print('Error in request: {0}'.format(ureq.status_code))
        elif verbose:
            print('File {0} exists use force=True to download'.format(row['fname']))   
    

def load(site: str = ['GILL'],
         sdate='2010-01-01',
         ndays: int = 1,
         edate=None,
         gz=True,
         dl=True,
         force=False):
    """Loads CARISMA F01 files and F01.gz files
    
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
    force : bool, optional
        Force downloading files again, by default False
    
    Returns
    -------
    Pandas DataFrame
        Cleaned and rotated (if possible) CARISMA magnetometer data
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
            download(f_df=f_df,force=force)

        s_df = pd.DataFrame()
        for di, row in f_df.iterrows():
            print('Loading: '+os.path.join(row['dir'], row['fname']))

            # get file name and check
            # if it exists
            fn = os.path.join(row['dir'], row['fname'])
            if not os.path.exists(fn):
                print('File does not exist: {0}'.format(fn))
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
        else:
            continue
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
    """Remove bad data from CARISMA DataFrame

    This is a function so that additional utility can
    be easily added.

    Parameters
    ----------
    i_df : DataFrame
        CARISMA magnetometer data loaded with carisma.load()

    Returns
    -------
    c_df : DataFrame
        Cleaned CARISMA magnetometer data
    """
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
    """Rotate XYZ to HDZ for select sites, append
    to existing DataFrame and return

    Parameters
    ----------
    i_df : DataFrame
        CARISMA magnetometer data loaded with image.load()
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

    for stn in site:
        stn = stn.upper()
        if stn+'_X' not in c_name:
            continue

        stn_dat = utils.load_station_coor(param=stn, year=dt.year)
        # if the stn_dat can't be found don't rotate
        if stn_dat is None:
            return i_df
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

