
# -*- coding: utf-8 -*-
"""

This module supports data from the IMAGE magnetometer array. Downloads data from IMAGE website.
Loads XYZ data and rotates into HDZ. Will load data downloaded from IMAGE website
as well as THEMIS CDF files.

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

    Downloading IMAGE data requires filling out a form. MechanicalSoup is used for web scraping and
    retrieving data files.

    Acknowledgement: We thank the institutes who maintain the IMAGE Magnetometer Array:
    Tromsø Geophysical Observatory of UiT the Arctic University of Norway (Norway),
    Finnish Meteorological Institute (Finland), Institute of Geophysics Polish Academy of Sciences (Poland),
    GFZ German Research Centre for Geosciences (Germany), Geological Survey of Sweden (Sweden),
    Swedish Institute of Space Physics (Sweden), Sodankylä Geophysical Observatory of the University of Oulu (Finland),
    and Polar Geophysical Institute (Russia).

References
----------
.. [1] Tanskanen, E.I. (2009): A comprehensive high-throughput analysis of substorms observed
    by IMAGE magnetometer network: Years 1993-2003 examined.
    J. Geophys. Res., 114, A05204, doi:10.1029/2008JA013682.

"""

import os
import pandas as pd
import numpy as np
import gzip
import wget

import gmag
from gmag.config import get_config_file

from gmag import utils

local_dir =os.path.join(gmag.config_set['data_dir'],'magnetometer','IMAGE')
http_dir = gmag.config_set['im_http']

# check if local dir exists
if not os.path.exists(local_dir):
    try:
        os.makedirs(local_dir)
    except FileNotFoundError:
        print('Local IMAGE Drive does not exist')


def list_files(sdate,
               ndays=1,
               edate=None,
               prefix='image',
               fformat='.col2',
               gz=True):
    """Return a Pandas DataFrame containing the date, file name, and directory
    for every file. Assume filename is generated for every day.

    Used to generate a list of files for either downloading or loading

    Directory structure is assumed
    local_dir\\YYYY\\MM\\filename

    Parameters
    ----------
    sdate : str or datetime-like
        Initial day to be loaded
    ndays : int, optional
        Number of days to be listed  (the default is 1, which will create a DataFram for a single file)
    edate : str, optional
        Last day in generated list (the default is None, which will defualt to ndays)
    prefix : str, optional
        Prefix for filename (the default is 'image')
    fformat : str, optional
        File format  (the default is '.col2')
    gz : bool, optional
        Create gzipped filenames (the default is True)

    Returns
    -------
    f_df : DataFrame
        Pandas dataframe with columns date (file date), fname (file name), fdir (file directory)

    """

    # create a panda series of dates
    if edate is not None:
        d_ser = pd.Series(pd.date_range(start=sdate, end=edate, freq='D'))
    else:
        d_ser = pd.Series(pd.date_range(start=sdate, periods=ndays, freq='D'))

    f_df = pd.DataFrame(columns=['date', 'fname', 'dir'])

    # create file name and directory structure
    for di, dt in d_ser.iteritems():
        # filename
        fnm = prefix + \
            '{0:04d}{1:02d}{2:02d}{3:02d}{4}'.format(
                dt.year, dt.month, dt.day, dt.hour, fformat)
        if gz:
            fnm = fnm + '.gz'

        # directory where file will be saved
        # IMAGE data is stored in the local_dir as YYYY\MM\image_file
        fdr = os.path.join(local_dir, '{0:04d}'.format(
            dt.year), '{0:02d}'.format(dt.month))
        if not os.path.exists(fdr):
            os.makedirs(fdr)

        f_df = f_df.append(
            {'date': dt, 'fname': fnm, 'dir': fdr}, ignore_index=True)

    return f_df


def download(sdate,
             ndays=1,
             edate=None,
             gz=True,
             force=False,
             verbose=0):
    """Download IMAGE magnetometer data from the IMAGE request website

    Parameters
    ----------
    sdate : str or datetime-like
        Initial day to be downloaded
    ndays : int, optional
        Number of days to download, by default 1
    edate : str or datetime-like, optional
        Last day to download. If set overrides ndays.
        By default None
    gz : bool, optional
        Download gzipped files, by default True
    force: bool, optional
        Force download even if file exists
    verbose : int, optional
        List files being downloaded, by default 0
    """

    # get file names
    f_df = list_files(sdate, ndays=ndays, edate=edate, gz=gz)

    for ind, row in f_df.iterrows():
        # generate file name
        fn = os.path.join(row['dir'], row['fname'])
        # only donwnload if file does not exist
        #or force is true
        if not os.path.exists(fn) or force:
            # if forcing download and file
            #exists remove file before
            #redownloading
            if os.path.exists(fn):
                os.remove(fn)

            # generate http link for file
            hlink = http_dir+'starttime={0:04d}{1:02d}{2:02d}&length=1440&format=text&sample_rate=10'.format(
                row['date'].year, row['date'].month, row['date'].day)
            if gz:
                hlink = hlink+'&compress'
            #download data
            print(hlink)
            req = wget.download(hlink,out=fn,bar=wget.bar_adaptive)
            print('\n {}'.format(req))
        else:
            print('File {0} exists use force=True to download'.format(row['fname']))

         

def load(site: str = ['AND'],
         sdate='2010-01-01',
         ndays: int = 1,
         edate=None,
         gz=True):
    """Loads IMAGE magnetometer data in the .col2 data
    format

    Parameters
    ----------
    site : str, optional
        IMAGE sites to load, by default ['AND']
    sdate : str or datetime-like, optional
        Initial day to load, by default '2010-01-01'
    ndays : int, optional
        Number of days to load, by default 1
    edate : str or datetime-like, optional
        End date to load. If set overrides ndays, by default None
    gz : bool, optional
        File to be loaded is gzip file, by default True

    Returns
    -------
    r_df : DataFrame
        Cleaned and rotated IMAGE magnetometer data
    """
    # create a site list for returns
    if type(site) is str:
        site = [site]

    # get list of file names
    f_df = list_files(sdate, ndays=ndays, edate=edate, gz=gz)

    # create empty data frame for data
    d_df = pd.DataFrame()

    for ind, row in f_df.iterrows():
        print(os.path.join(row['dir'], row['fname']))

        # get file name and check
        # if it exists
        fn = os.path.join(row['dir'], row['fname'])
        if not os.path.exists(fn):
            print('File does not exist: {0}'.format(fn))
            continue

        # get header information
        if gz:
            with gzip.open(fn, mode='rt') as f:
                col = f.readline().rstrip('\n')
        else:
            with open(fn, 'r') as f:
                col = f.readline().rstrip('\n')

        # fix header for data fram
        col = col.replace(' X', '_X').replace(' Y', '_Y').replace(' Z', '_Z')
        col = col.split()
        col[3:6] = ['hh', 'mm', 'ss']

        # read in data
        i_df = pd.read_csv(fn, delim_whitespace=True, header=None,
                           skiprows=2, names=col, parse_dates=[[0, 1, 2, 3, 4, 5]])
        i_df = i_df.rename(index=str, columns={"YYYY_MM_DD_hh_mm_ss": "t"})

        i_df['t'] = pd.to_datetime(
            i_df['t'].astype(str), format='%Y %m %d %H %M %S')

        d_df = d_df.append(i_df, ignore_index=True)

    if d_df.empty:
        return None

    # keep only listed stations
    s_df = pd.DataFrame()
    s_df['t'] = d_df['t']
    # empty list for stations
    # that where actually read in
    s_l = []
    for stn in site:
        try:
            s_df[stn.upper()+'_X'] = d_df[stn.upper()+'_X']
            s_df[stn.upper()+'_Y'] = d_df[stn.upper()+'_Y']
            s_df[stn.upper()+'_Z'] = d_df[stn.upper()+'_Z']
            s_l.append(stn.upper())
        except KeyError:
            print('Station not found: {0}'.format(stn))

    # clean and rotate data
    # as long as one station
    # exists
    if len(s_l):
        # clean data frame
        c_df = clean(s_df)
        # rotate data frame
        r_df = rotate(c_df, s_l, sdate)
        r_df = r_df.set_index('t')
    else:
        return None

    return r_df


def clean(i_df):
    """Remove bad data from IMAGE DataFrame

    This is a function so that additional utility can
    be easily added.

    Parameters
    ----------
    i_df : DataFrame
        IMAGE magnetometer data loaded with image.load()

    Returns
    -------
    c_df : DataFrame
        Cleaned IMAGE magnetometer data
    """
    c_df = i_df.replace(to_replace=99999.9, value=np.nan).sort_values(
        by=['t']).reset_index(drop=True)

    return c_df


def rotate(i_df,
           site,
           date):
    """Rotate XYZ to HDZ for selec sites, append
    to existing DataFrame and return

    Parameters
    ----------
    i_df : DataFrame
        IMAGE magnetometer data loaded with image.load()
    site : List[str]
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

    for stn in site:
        stn_dat = utils.load_station_coor(param=stn, year=dt.year)
        # if the stn_dat can't be found don't rotate
        if stn_dat is None:
            return i_df
        dec = float(stn_dat['declination'])

        # some of the IMAGE magnetometers
        # have negative Z values. Z should
        # always positive. These mags are
        # likely measuring variations which
        # we can't calculate H and D for.
        if any(i_df[stn+'_Z'] < 0):
            i_df[stn+'_H'] = np.nan
            i_df[stn+'_D'] = np.nan
        else:
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
