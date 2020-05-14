---
layout: default
---

# Overview

This code provides the utility to download and load data from various ground-based magtometer arrays. The code for is divided into a seperate module for each array. These are the ```carisma```, ```image```, and ```themis``` modules. 

The ```carisma``` module loads data from the [CARISMA][1] magnetometer array.

The ```image``` modules loads data from the [IMAGE][2] magnetometer array.

The ```themis``` modules loads data from the [THEMIS EPO and GBO][3], [CARISMA][1], [CANMOS][4], [AUTUMN and AUTUMN X][5], [DTU][6], [IMAGE][2], [GIMA][7], [MACCS][8], [McMAC][9], [USGS][10], and [PENGUIN][11] arrays. When using the ```themis``` module be sure to properly acknowledge **each** array whose data is used. 

For additional information regarding the stations see [Arrays and Stations][12].

## Installation

```bash
pip install -e .
```

## gmagrc

The ```gmagrc``` file defines the local directory where magnetoemter data is downloaded.

*   CARISMA files: local_dir\CARISMA\YYYY\MM\DD\station.file
*   IMAGE files: local_dir\IMAGE\YYYY\MM\array_day.file
*   THEMIS files: local_dir\THEMIS\site\YYYY\station.file

The ```carisma``` and ```themis``` modules download a daily file for each station. The ```image``` module downloads a single file including data from multiple stations each day. 

The ```gmagrc``` files also defines the web address where data is stored for each array. If the addreses change they can be updated here. 

## Station Parameters

The names of stations, 4 letter codes, home array, geographic and geomagnetic coordinates, L-shell, and declinations are stored in [yearly files][13] and can be loaded with the ```utlis``` module. These files and the declinations are used to rotate **CARISMA** and **IMAGE** date from  geographic (XYZ) to geomagnetic coordinates (HDZ, or heZ). This is done using: 

H = X cos(dec) + Y sin(dec)
D = Y cos(dec) - H sin(dec)

Data loaded using the ```themis``` module is not rotated as the data is generally already in geomagnetic coordinates. Details on the processing of the ground-based magnetometer data from THEMIS can be found [here][14]. 

The ```util``` module will load station coordinates from text files in ./gmag/Stations/

```python
from gmag import utils
#load all CARISMA station data for 2002
car_stn = utils.load_station_coor(
  param='CARISMA',col='array',year=2002)

#load GILL data from 2012
gill_stn = utils.load_station_coor(
  param='GILL',col='code',year=2012)
```

## Loading Data

The load routines in each of the modules will load (rotate if necessary) and download files. Some examples can be found in [notebooks][15] folder. Simple examples are below. Note the load routines are the same for each array.

```python
#load CARISMA
import gmag.carisma as carisma
df = carisma.load(['ISLL','PINA'],'2012-01-01',ndays=2)
df = carisma.load(['ISLL','PINA'],'2012-01-01',edate='2012-01-03')

#load IMAGE
import gmag.image as image
df = image.load('AND','2012-01-01',ndays=21)

#load THEMIS, force download even if file exists
import gmag.themis as themis
df = themis.load('KUUJ',sdate='2012-01-01',ndays=22, dl=True,force=True)
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
[12]: ./arrays_stations.md
[13]: https://github.com/kylermurphy/gmag/tree/master/gmag/Stations
[14]: ftp://apollo.ssl.berkeley.edu/pub/THEMIS/3%20Ground%20Systems/3.2%20Science%20Operations/Science%20Operations%20Documents/GMAG_Station_Data_Processing_Notes.pdf
[15]: https://github.com/kylermurphy/gmag/tree/master/notebooks