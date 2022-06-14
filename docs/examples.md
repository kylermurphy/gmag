---
layout: default
---

# Arrays and Stations 

## [Station table and map.][1]

## IMPORTANT NOTES

1. THEMIS is an excellent resourcee for the ground-based magnetometer arrays loaded by ```gmag```. However, data downloaded from the THEMIS data server are not necessarily  THEMIS magnetometers. Please appropriately reference and acknowledge each array whose data you use;  acknowledgements and reference for the arrays (when available) can be found below.
2. The data from the THEMIS data server are generally in geomagnetic cooridinates, though this is not a given. To overcome this the returned metadata Pandas DataFrame stores data labels from the CDF for data loaded using the ```themis``` module. These labels will specify the coordinate system of the loaded data.
3. CARISMA and IMAGE data loaded using the ```carisma``` and ```image``` modules are roated from XYZ to HDZ. 

## Arrays

Below is a list of the arrays suported by the ```gmag``` code. Additional details for each array including the arrays webiste, terms of use, data download, map of stations, and acknowledgement are found below.

Information on individual stations can be found [here][1].

| Array | Module | Secondary Module |
|-------|--------|------------------|
| [CARISMA](#carisma) | ```carisma``` | ```themis```|
| [CANOPUS](#carisma) | ```canopus``` | N/A |
| [CANMOS](#canmos) | ```themis``` | N/A |
| [AUTUMN and AUTUMN X](#autumn-and-autumn-x)  | ```themis``` | N/A |
| [DTU](#dtu)  | ```themis``` | N/A |
| [IMAGE](#image) | ```image``` | ```themis``` |
| [GIMA](#gima)  | ```themis``` | N/A |
| [MACCS](#maccs)  | ```themis``` | N/A |
| [McMAC](#mcmac)  | ```themis``` | N/A |
| [THEMIS EPO and GBO](#themis-epo-and-gbo)  | ```themis``` | N/A |
| [USGS](#usgs)  | ```themis``` | N/A |
| [PENGUIN](#penguin)  | ```themis``` | N/A |


Station data can typically be downloaded from the homepage of each array. However, a significant amount of data can be downloaded from the [THEMIS data server](http://themis.ssl.berkeley.edu/data/themis/thg/l2/mag/), [THEMIS ftp server](ftp://justice.ssl.berkeley.edu), and corresponding [CDAWeb mirror](ftp://cdaweb.gsfc.nasa.gov/pub/data/themis/thg/l2/mag/) in the form of CDFs.

The [THEMIS website](http://themis.ssl.berkeley.edu) is also an excellent resource for information pertaining the stations and corresponding arrays which are stored on the [THEMIS data server](http://themis.ssl.berkeley.edu/data/themis/thg/l2/mag/). See also this [overview](ftp://apollo.ssl.berkeley.edu/pub/THEMIS/3%20Ground%20Systems/3.2%20Science%20Operations/Science%20Operations%20Documents/GMAG_Station_Data_Processing_Notes.pdf) 

- [Fluxgate Magnetometer Overview](http://themis.ssl.berkeley.edu/instrument_gmags.shtml)
- [Ground Magnetometer Data Availability](http://themis.ssl.berkeley.edu/gmag/gmag_list.php?selyear=4000&selmonth=13&smap=on&sinfo=on&saelist=on&ae=on)
- [Data Policy and Credits for various arrays](http://themis.ssl.berkeley.edu/roadrules.shtml). However always check with the arrays homepage for updated polices and terms of conditions (below).


--- 

#### CARISMA/CANOPUS

The Canadian Array for Realtime Investigations of Magnetic Activity, [CARISMA](http://carisma.ca/), hosted by the University of Alberta. Formerly the e Canadian Auroral Network for the OPEN Program Unified Study (CANOPUS, pre 1 April 2005).

- [Terms and Conditions of use](http://carisma.ca/carisma-data/data-use-requirements)
- [Data download](http://carisma.ca/carisma-data-repository)
- [Map of stations](http://carisma.ca/station-information)
- Acknowledgement: _"I.R. Mann, D.K. Milling and the rest of the CARISMA team for use of GMAG data. CARISMA is operated by the University of Alberta, funded by the Canadian Space Agency."_

---

#### CANMOS

The Natural Resources Canada Canadian Magnetic Observatory System, [CANMOS](http://geomag.nrcan.gc.ca/obs/canmos-en.php).

- [Terms and Conditions of use](http://geomag.nrcan.gc.ca/data-donnee/sd-en.php)
- [Data download](http://geomag.nrcan.gc.ca/data-donnee/dl/dl-en.php)
- [Map of stations](http://geomag.nrcan.gc.ca/obs/default-en.php)
- Acknowledgement: acknowledge the Geological Survey of Canada as the source of the data.

---

#### AUTUMN and AUTUMN X

The Athatbasca University THEMIS UCLA Magnetometer Network, [AUTUMN and AUTUMNX](http://autumn.athabascau.ca/).

- Data download via [CDAWeb](ftp://cdaweb.gsfc.nasa.gov/pub/data/themis/thg/l2/mag/) and [THEMIS](http://themis.ssl.berkeley.edu/data/themis/thg/l2/mag/)
- Acknowledgement: _"Martin Connors and C.T. Russell and the rest of the AUTUMN/AUTUMNX team for use of the GMAG data."_

---

#### DTU

Technical University of Denmark National Space Institute ground based magnetometer array, [DTU](http://www.space.dtu.dk/english/Research/Scientific_data_and_models/Magnetic_Ground_Stations).

- [Terms and Conditions of Use](http://www.space.dtu.dk/english/Research/Scientific_data_and_models/Magnetic_Ground_Stations/dtu_data_policies)
- [Data Download](http://www.space.dtu.dk/english/Research/Scientific_data_and_models/Magnetic_Ground_Stations#requ), currently under constructions. Data can also be downloaded via via [CDAWeb](ftp://cdaweb.gsfc.nasa.gov/pub/data/themis/thg/l2/mag/) and [THEMIS](http://themis.ssl.berkeley.edu/data/themis/thg/l2/mag/).
- [Map of Stations](http://www.space.dtu.dk/English/Research/Scientific_data_and_models/Magnetic_Ground_Stations.aspx#map)
- Acknowledgement: _"Magnetometer data from the Greenland Magnetometer Array were provided by the National Space Institute at the Technical University of Denmark (DTU Space)."_

---

#### IMAGE

The International Monitor for Auroral Geomagnetic Effects, [IMAGE](http://space.fmi.fi/image/www/index.php?page=home), ground based magnetometer array. Data is provided by multiple institutions, see [IMAGE organization](http://space.fmi.fi/image/www/index.php?page=contributors) for details.

- [Terms and Conditions of Use](http://space.fmi.fi/image/www/index.php?page=rules_of_road)
- [Data Download](http://space.fmi.fi/image/www/index.php?page=request#)
- [Map of stations](http://space.fmi.fi/image/www/index.php?page=maps)
- Acknowledgement: _"We thank the institutes who maintain the IMAGE Magnetometer Array: Tromsø Geophysical Observatory of UiT the Arctic University of Norway (Norway), Finnish Meteorological Institute (Finland), Institute of Geophysics Polish Academy of Sciences (Poland), GFZ German Research Centre for Geosciences (Germany), Geological Survey of Sweden (Sweden), Swedish Institute of Space Physics (Sweden), Sodankylä Geophysical Observatory of the University of Oulu (Finland), and Polar Geophysical Institute (Russia)."_

---

#### GIMA

The Geophysical Institute Magnetometer Array, [GIMA](https://www.gi.alaska.edu/monitors/magnetometer) at the University of Alaska Fairbanks.

- [Terms and Conditions](https://www.gi.alaska.edu/monitors/magnetometer) under **Citing Magnetometer Data**.
- [Data Download](https://www.gi.alaska.edu/monitors/magnetometer/archive)
- Acknowledgement: _"Data provided by the Geophysical Institute Magnetometer Array operated by the Geophysical Institute, University of Alaska."_

---

#### MACCS

The Augsburg College Space Physics Magnetometer Array for Cups and Cleft Studies, [MACCS](http://space.augsburg.edu/maccs/index.html)

- [Terms and Conditions](http://space.augsburg.edu/maccs/datausepolicy.html)
- [Data Download](http://space.augsburg.edu/maccs/requestdatafile.jsp)
- [Map of Stations](http://space.augsburg.edu/maccs/coordinates.html)
- Acknowledgement: _"Erik Steinmetz, Augsburg College for the use of GMAG data."_

---

#### McMAC

The Mid‐continent MAgnetoseismic Chain, [McMAC magnetometers](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/jgra.50274).

- Data Download via [CDAWeb](ftp://cdaweb.gsfc.nasa.gov/pub/data/themis/thg/l2/mag/) and [THEMIS](http://themis.ssl.berkeley.edu/data/themis/thg/l2/mag/).
- Acknowledgement: _"Peter Chi for use of the McMAC data and NSF for support through grant ATM-0245139."_


---

#### THEMIS EPO and GBO

The Time History of Events and Macroscal Interaction During Substorms (THEMIS) Ground Based Observatory (GBO) and Educations and Public Outreach (EPO) [magnetoemters](http://themis.ssl.berkeley.edu/instrument_gmags.shtml).

- [Terms and Conditions](http://themis.ssl.berkeley.edu/roadrules.shtml)
- [Data Download](http://themis.ssl.berkeley.edu/data/themis/thg/l2/mag/)
- [Map of Stations](http://themis.ssl.berkeley.edu/instrument_gmags.shtml)
- Acknowledgement: _"S. Mende and C. T. Russell for use of the GMAG data and NSF for support through grant AGS-1004814."_

---

#### USGS

The Unites States Geological Survery, [USGS magnetometers](https://www.usgs.gov/natural-hazards/geomagnetism]).

- [Terms and Conditions](https://www.usgs.gov/natural-hazards/geomagnetism/science/download-data?qt-science_center_objects=0#qt-science_center_objects)
- [Data Download](https://www.usgs.gov/natural-hazards/geomagnetism/science/web-service-0?qt-science_center_objects=0#qt-science_center_objects)
- [Map of stations](https://www.usgs.gov/natural-hazards/geomagnetism/science/observatories?qt-science_center_objects=0#qt-science_center_objects)
- Acknowledgement: _"Original data provided by the USGS Geomagnetism Program (http://geomag.usgs.gov)."_

---

#### PENGUIN

The Virgina Tech Polar Experimental Network for Geospace Upper atmosphere Investigations, [PENGUIN](http://mist.nianet.org/index.html) Ground Based Observatory.

- [Terms and Conditions](http://mist.nianet.org/CDFdata/VT_MIST_Data_Policy.pdf)
- Data Download, [IDL save files](http://mist.nianet.org/IDLsavePGx/) and [CDFs](http://mist.nianet.org/CDFdata/)
- Acknowledgement: _"Polar Experimental Network for Geospace Upper atmosphere Investigations (PENGUIn) Ground Based Observatory, PI, C. Robert Clauer, Virginia Tech. This effort is supported by the National Science Foundation through the following awards: ANT0839858, ATM922979 (Virginia Tech), and ANT0838861 (University of Michigan)."_

[1]: ./stations.md