"""

This module supports data from the CANOPUS (now CARISMA) magnetometer array.

Directory structure is assumed
local_dir\\YYYY\\MM\\SITE\\file

local_dir is set in gmagrc

Example
-------

Load data from multiple stations
df = canopus.load(site=['GILL','ISLL','PINA'],sdate='2012-01-01',ndays=1)

You can download data a site at time with xxxx.download, though its
easier to use xxxx.load as it will loop through stations


Attributes
----------
local_dir : str
    Directory for CANOPUS data. This directory will be used to download and load CANOPUS files.
http_dir : str
    Web address for CANOPUS data. This points to the website of CANOPUS data.


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


local_dir = os.path.join(gmag.config_set['data_dir'],'magnetometer','CARISMA')
http_dir = False

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
     local_dir\\YYYY\\MM\\SITE\\filename

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
            print('hi')
            #hdr = http_dir+'FGM/1Hz/'+'{0:04d}'.format(dt.year)+'/'
            #hdr = hdr+'{0:02d}'.format(dt.month)+'/'+'{0:02d}'.format(dt.day)+'/'
        else: 
            hdr = False
                


        f_df = f_df.append(
            {'date': dt, 'fname': fnm, 'dir': fdr, 'hdir':hdr}, ignore_index=True)

    return f_df