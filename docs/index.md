---
layout: default
---

# Updates

Version 2.0.0 has just been released. Major update is compatibility with Pandas >=2.0.2 and cdflib >=1.0.4!

# Overview

This code provides the utility to **download and load data** from various ground-based magnetometer arrays into a Pandas DataFrame. The code also return **metadata** for the loaded stations. The code is divided into a seperate module for each array. These are the ```carisma```, ```canopus```, ```image```, and ```themis``` modules. 

The ```carisma``` module loads data from the [CARISMA][1] magnetometer array.

The ```canopus``` module loads data from the legacy [CANOPUS][1] magnetometer array pre 1 April 2005. The data must be downloaded from the [CARISMA][1] website and cannot be downloaded using the module.

The ```image``` modules loads data from the [IMAGE][2] magnetometer array.

The ```themis``` modules loads data from the [THEMIS EPO and GBO][3], [CARISMA][1], [CANMOS][4], [AUTUMN and AUTUMN X][5], [DTU][6], [IMAGE][2], [GIMA][7], [MACCS][8], [McMAC][9], [USGS][10], and [PENGUIN][11] arrays. When loading data from the ```themis``` module be sure to properly acknowledge **each** individual array used. 

## [Arrays][12] 

Additonal information on the [arrays][12] supported by ```gmag```. 

## [Stations][19] 

Table and map of [stations][19] for each array. 

## Installation

Download or fork the repository. Replace the example configuration file ```gmagrc_example``` with ```gmagrc``` and fill in the variable ```data_dir``` with the directory you would like all files downloaded then CD to the local GMAG directory and install via:

```bash
pip install -e .
```

## gmagrc

The ```gmagrc``` file defines the local directory where magnetoemter data is downloaded and the web address where data is stored for each array. If the addreses change they can be updated here.

- CARISMA files
  - local_dir\CARISMA\YYYY\MM\DD\station.file
- CANOPUS files
  - local_dir\CANOPUS\YYYY\MM\DD\station.file
- IMAGE files
  - local_dir\IMAGE\YYYY\MM\array_day.file
- THEMIS files
  - local_dir\THEMIS\site\YYYY\station.file

The ```carisma``` and ```themis``` modules download a daily file for each station. The ```image``` module downloads a single file including data from multiple stations each day. 

## Station Parameters

The names of stations, 4 letter codes, home array, geographic and geomagnetic coordinates, L-shell, and declinations are stored in [yearly coordinate files][13] and can be loaded with the ```utlis``` module. These files and the declinations are used to rotate **CARISMA** and **IMAGE** date from  geographic (XYZ) to geomagnetic coordinates (HDZ, or heZ). This is done using: 

H = X cos(dec) + Y sin(dec)

D = Y cos(dec) - H sin(dec)

Data loaded using the ```themis``` module is not rotated as the data is generally already in geomagnetic coordinates. Details on the processing of the ground-based magnetometer data from THEMIS can be found [here][14]. 

The ```util``` module will load station coordinates from text files in ./gmag/Stations/

```python
from gmag import utils
#load geomagnetic data
#load all CARISMA station data for 2002
car_stn = utils.load_station_coor(
  param='CARISMA',col='array',year=2002)

#load GILL data from 2012
gill_stn = utils.load_station_coor(
  param='GILL',col='code',year=2012)

#load all data from 2012
all_stn = utils.load_station_coor(param='ALL',year=2012)

#load station geographic data
#load all CARISMA data
geo_stn = utils.load_station_geo(param='CARISMA',col='array')

#load all stations
all_stn = utils.load_station_geo(param='ALL')
```

The [yearly coordinate files][13] are generated using [Convert_coords.ipynb][15] which requires the [IGRF][16] and [aacgmv2][17] modules which can be difficult to install. For simplicity, the coordinate files are pre-generated and will updated when possible.

## Loading Data

The load routines in each of the modules will load (rotate if necessary) and download files. Some examples can be found in [notebooks][18] folder. Simple examples are below. The load routines are similar for each array and load data into Pandas DataFrames.

```python
#load CARISMA
import gmag.arrays.carisma as carisma
df, meta = carisma.load(['ISLL','PINA'],'2012-01-01',ndays=2)
df, meta = carisma.load(['ISLL','PINA'],
                  '2012-01-01',edate='2012-01-03')

#load IMAGE
import gmag.arrays.image as image
df, meta = image.load('AND','2012-01-01',ndays=21)

#load THEMIS, force download even if file exists
import gmag.arrays.themis as themis
df, meta = themis.load('KUUJ',sdate='2012-01-01',
                  ndays=22, dl=True,force=True)

#load CANOPUS
import gmag.arrays.canopus as canopus
df, meta = canopus.load('ISLL',sdate='2001-01-01',ndays=1)                  
```


[1]: http://carisma.ca/
[2]: https://space.fmi.fi/image/www/index.php?page=contributors
[3]: http://themis.ssl.berkeley.edu/instrument_gmags.shtml
[4]: http://geomag.nrcan.gc.ca/obs/canmos-en.php
[5]: http://autumn.athabascau.ca/
[6]: http://www.space.dtu.dk/english/Research/Scientific_data_and_models/Magnetic_Ground_Stations
[7]: https://www.gi.alaska.edu/monitors/magnetometer
[8]: http://space.augsburg.edu/maccs/index.html
[9]: https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/jgra.50274
[10]: https://www.usgs.gov/natural-hazards/geomagnetism
[11]: http://mist.nianet.org/index.html
[12]: ./arrays.md
[13]: https://github.com/kylermurphy/gmag/tree/master/gmag/Stations
[14]: ftp://apollo.ssl.berkeley.edu/pub/THEMIS/3%20Ground%20Systems/3.2%20Science%20Operations/Science%20Operations%20Documents/GMAG_Station_Data_Processing_Notes.pdf
[15]: https://github.com/kylermurphy/gmag/blob/master/notebooks/Convert_coords.ipynb
[16]: https://github.com/space-physics/igrf12
[17]: https://github.com/aburrell/aacgmv2
[18]: https://github.com/kylermurphy/gmag/tree/master/notebooks
[19]: ./stations.md