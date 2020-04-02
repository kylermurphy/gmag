# README for gmag code

Basic documentation for gmag code. 

## gmagrc

This file sets the local directory to download data. 

- CARISMA files: local_dir\CARISMA\YYYY\MM\DD\station.file
- IMAGE files: local_dir\IMAGE\YYYY\MM\array_day.file
- THEMIS files: local_dir\THEMIS\site\YYYY\station.file

This file also includes the http directory for downloading data. If the addresses change they can updated in this file. 



## Magnetometers 

This code provides utility to load and download data from various ground-based magtometer arrays. The code for loading various arrays is divided into a seperate module for each array; CARISMA, IMAGE, and THEMIS. **Note** that the THEMIS module works with several arrays and loads a number of stations which are not all THEMIS stations. **When using the THEMIS module be sure to properly acknowledge where the data has come from.** 

The ```carisma``` modules loads data from the CARISMA magnetometer array.

The ```image``` modules loads data from IMAGE. 

The ```themis``` modules loads data from THEMIS EPO and GBO, CARISMA, CANMOS, AUTUMN and AUTUMN X, DTU, IMAGE, GIMA, MACCS, McMAC, , USGS, PENGUIN.

Details on the arrays can be found [here](./Stations/README.md)

### Station Parameters

Station, geographic, geomagnetic, L-shell, and declinations, are loaded in yearly files. The declinations are used to rotate geographic coordinates (XYZ) into geomagnetic coordinates (HDZ sometimes referred to as heZ) when necessary. This is done using:

H = X cos(dec) + Y sin(dec)

D = Y cos(dec) - H sin(dec)

This rotation is applied to both the CARISMA and IMAGE data. Data loaded through the THEMIS module is not roated but is generally in geomagnetic coordinates.

The ```util``` module will load station coordinates from text files in ./Stations/

```python
from gmag import utils
#load all CARISMA station data for 2002
car_stn = utils.load_station_coor(param='CARISMA',col='array',year=2002)

#load GILL data from 2012
gill_stn = utils.load_station_coor(param='GILL',col='code',year=2012)
```

## Loading data

The load routines in each of the modules will load (rotate if necessary) and download files. Some examples can be found in the notebooks folder. Simple examples are below. Note the load routines are the same for each array.

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


