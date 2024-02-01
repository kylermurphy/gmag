
# -*- coding: utf-8 -*-
"""

This module supports data from the THEMIS magnetometer array. Downloads data from THEMIS website.
Loads XYZ data and rotates into HDZ.

Directory structure is assumed
local_dir\\magnetometer\\THEMIS\\YYYY\\site\\file

local_dir is set in gmagrc

Example
-------

Produce a file list for downloading, generally easier using
themis.download is easier
fl = themis.list_files('KUUJ','2012-01-01',ndays=2)
themis.download(f_df=fl)

Download Data, generally easier using themis.load which will
loop through multiple sites.
themis.download(site='KUUJ',sdate='2012-01-01',edate='2012-01-03')

Load Data
df = themis.load(site=['KUUJ','SNKQ],sdate='2012-01-01',edate='2012-01-03')

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

    Some Arrays other then THEMIS are loaded using the THEMIS module, as
    they are downloaded from the THEMIS webiste and stored in the same 
    format as THEMIS. Please be sure to use proper acknoledgments when
    downloading data from the other Arrays.

References
----------


"""


import os
import wget
import pandas as pd
import numpy as np

import cdflib
import gmag

from gmag import utils
from urllib.parse import urljoin

local_dir = os.path.join(gmag.config_set['data_dir'], 'magnetometer', 'THEMIS')
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
     local_dir\\magnetometer\\THEMIS\\YYYY\\site\\file

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
        fnm = 'thg_l2_mag_'+site.lower()+'_'+fnm+'_v01.cdf'

        # directory location
        # THEMIS data is store in local_dir as YYYY\MM\DD\themis_file
        fdr = os.path.join(local_dir,
                           site.lower(),
                           '{0:04d}'.format(dt.year))
        if not os.path.exists(fdr):
            os.makedirs(fdr)

        # http directory
        hdr = http_dir+'thg/l2/mag/'+site.lower()+'/{0:04d}/'.format(dt.year)

        # Create a dataframe row for this site/date and append to answer
        curr_file_df = pd.DataFrame( {'date': dt, 'fname': fnm, 'dir': fdr, 'hdir': hdr}, index=[0])
        
        if f_df.empty:
            f_df = curr_file_df
        else:
            f_df = pd.concat( [ f_df, curr_file_df], ignore_index=True)

    return f_df


def download(site=None,
             sdate=None,
             ndays=1,
             edate=None,
             f_df=None,
             force=False,
             verbose=True):
    """Download THEMIS magnetometer data from the THEMIS website

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
        fn = os.path.join(row['dir'], row['fname'])
        if not os.path.exists(fn) or force:
            # if forcing download and file
            # exists remove file before
            # redownloading
            if os.path.exists(fn):
                os.remove(fn)
            try:
                wget.download(row['hdir']+row['fname'], out=row['dir'])
            except:
                print('HTTP file not found {0}'.format(row['fname']))
        elif verbose:
            print('File {0} exists use force=True to download'.format(
                row['fname']))


def load(site: str = ['KUUJ'],
         sdate='2010-01-01',
         ndays: int = 1,
         edate=None,
         dl=True,
         force=False):
    """Load THEMIS CDF files.

    Parameters
    ----------
    site : str, optional
        Site of list of sites  to load, by default ['KUUJ']
    sdate : str or datetime-like, optional
        Start date to load, by default '2010-01-01'
    ndays : int, optional
        Number of days to load, by default 1
    edate : str or datetime-like, optional
        End date to load if define defaults to this, by default None
    dl : bool, optional
        Download data before loading, by default True
    force : bool, optional
        Force download if already exists, by default False

    Returns
    -------
    Pandas DataFrame
        THEMIS magnetometer data and station metadata
    """
    if type(site) is str:
        site = [site]

    meta_df = pd.DataFrame(columns=['array', 'code', 'name', 'latitude', 'longitude', 'cgm_latitude',
       'cgm_longitude', 'declination', 'lshell', 'mlt_midnight', 'mlt_ut',
       'year','Time Resolution','Coordinates','PI','Institution'])

    stn_vals = utils.load_station_coor(param='ALL', year=pd.to_datetime(sdate).year)
    if stn_vals is None:
        stn_vals = utils.load_station_geo(param='ALL')

    # create empty data frame for data
    d_df = pd.DataFrame()
    for stn in site:
        # get list of file names
        f_df = list_files(stn.upper(), sdate, ndays=ndays, edate=edate)
        
        # station dataframe for data
        s_df = pd.DataFrame()
        if dl:
            print('Downloading Data:')
            download(f_df=f_df, force=force)

        for di, row in f_df.iterrows():
            print('Loading: '+os.path.join(row['dir'], row['fname']))

            # get file name and check
            # if it exists
            fn = os.path.join(row['dir'], row['fname'])
            if not os.path.exists(fn):
                print('File does not exist: {0}'.format(fn))
                continue

            # open cdf file and get data
            cdf_file = cdflib.CDF(fn)
            dat = cdf_file.varget('thg_mag_'+stn.lower())
            cdf_col = cdf_file.varget('thg_mag_'+stn.lower()+'_labl')
            t = pd.to_datetime(cdf_file.varget(
                'thg_mag_'+stn.lower()+'_time'), unit='s')
            #pi = cdf_file.attget('PI_name',0)['Data']
            pi = cdf_file.attget('PI_name',0).Data
            pi_i = cdf_file.attget('PI_affiliation',0).Data
            res = float(cdf_file.attget('Time_resolution',0).Data[0:-1])

            #cdf_file.close()
            # create data frame
            test_col = ['Magnetic North', 'Magnetic East', 'Vertical Down']
            lab_col = ['H','D','Z']

            columns=[(stn.upper()+'_'+l_col if c_col[0].astype(str).replace(',','-').split('-')[0].strip() == t_col \
                    else stn.upper()+'_'+c_col.strip()) \
                    for c_col,t_col,l_col in zip(cdf_col,test_col,lab_col)]
            i_df = pd.DataFrame(data=dat, columns=columns)
            i_df['t'] = t
            i_df = i_df.set_index('t')
            # append to returned data frame
            s_df = pd.concat([s_df, i_df])

        if d_df.empty:
            d_df = s_df
        else:
            d_df = d_df.join(s_df,how='outer')

        if s_df.empty:
            continue
            
        stn_dat = stn_vals[stn_vals['code'] == stn.upper()].reset_index(drop=True)
        stn_dat['Time Resolution'] = res
        stn_dat['Coordinates'] = ', '.join([str(c_col[0]).strip() for c_col in cdf_col]).strip()
        stn_dat['PI'] = pi
        stn_dat['Institution'] = pi_i

        if meta_df.empty:
            meta_df = stn_dat
        else:
            meta_df = pd.concat([meta_df,stn_dat], axis=0, sort=False, ignore_index=True)

    return d_df, meta_df
