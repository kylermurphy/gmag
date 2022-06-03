# README for gmag code

Basic documentation for gmag code. 

Requires: Pandas, NumPy, wget, requests, cdflib.

Installation: ```pip install -e .```

## gmagrc

This file sets the local directory to download and load data. 

- CARISMA files: local_dir\CARISMA\YYYY\MM\DD\station.file
- CANOPUS files: local_dir\CANOPUS\YYYY\MM\DD\station.file
- IMAGE files: local_dir\IMAGE\YYYY\MM\array_day.file
- THEMIS files: local_dir\THEMIS\site\YYYY\station.file

This file also includes the http directory for downloading data. If the addresses change they can updated in this file. 

## Magnetometers 

This code provides utility to load and download data from various ground-based magtometer arrays. The code for loading various arrays is divided into a seperate module for each array; CARISMA, IMAGE, and THEMIS. **Note** that the THEMIS module works with several arrays and loads a number of stations which are not all THEMIS stations. **When using the THEMIS module be sure to properly acknowledge where the data has come from.** 

The ```carisma``` modules loads data from the CARISMA magnetometer array. 

The ```canopus``` module loads data from the older CANOPUS array avaiable for download at the CARISMA website (pre 1 April 2005). The ```canopus``` module does not download data.

The ```image``` modules loads data from IMAGE. 

The ```themis``` modules loads data from THEMIS EPO and GBO, CARISMA, CANMOS, AUTUMN and AUTUMN X, DTU, IMAGE, GIMA, MACCS, McMAC, USGS, PENGUIN.

Details on the arrays can be found [here](./gmag/README.md).

### Station Parameters

Station, geographic, geomagnetic, L-shell, and declinations, are loaded in yearly files. The declinations are used to rotate geographic coordinates (XYZ) into geomagnetic coordinates (HDZ sometimes referred to as heZ) when necessary. This is done using:

H = X cos(dec) + Y sin(dec)

D = Y cos(dec) - H sin(dec)

This rotation is applied to both the CARISMA (CANOPUS) and IMAGE data. Data loaded through the THEMIS module is not roated but is generally in geomagnetic coordinates. The station geographic/geomagnetic location, declication, resolution, and magnetic field coordinates are returned as metadata. 

The ```util``` module will load station information and coordinates from text files in ./Stations/. 

- ```util.load_station_coor```: load geomagnetic/geographic coordinates and station info by year
- ```util.load_station_geo```: load only geographic coordinates and station info

```python
from gmag import utils
#load geomagnetic data
#load all CARISMA station data for 2002
car_stn = utils.load_station_coor(param='CARISMA',col='array',year=2002)

#load GILL data from 2012
gill_stn = utils.load_station_coor(param='GILL',col='code',year=2012)

#load all data from 2012
all_stn = utils.load_station_coor(param='ALL',year=2012)

#load station geographic data
#load all CARISMA data
geo_stn = utils.load_station_geo(param='CARISMA',col='array')

#load all stations
all_stn = utils.load_station_geo(param='ALL')
```

## Loading data

The load routines in each of the modules will load (rotate if necessary) and download files. Some examples can be found in ```notebooks``` folder. Simple examples are below. Note the load routines are the same for each array.

```python
#load CARISMA
import gmag.arrays.carisma as carisma
df, meta = carisma.load(['ISLL','PINA'],'2012-01-01',ndays=2)
df, meta = carisma.load(['ISLL','PINA'],'2012-01-01',edate='2012-01-03')

#load IMAGE
import gmag.arrays.image as image
df, meta = image.load('AND','2012-01-01',ndays=21)

#load THEMIS, force download even if file exists
import gmag.arrays.themis as themis
df, meta = themis.load('KUUJ',sdate='2012-01-01',ndays=22, dl=True,force=True)

#load CANOPUS
import gmag.arrays.canopus as canopus
df, meta = canopus.load('ISLL',sdate='2001-01-01',ndays=1)
```


