---
layout: default
---

# GMAG Examples 

A few simple example of loading and plotting ground-based magnetometer data using the GMAG module. 

### Single Station Plot

Create a single station plot using from data loaded using the ```themis``` module. 

```python
# Plot a simple time series from
# a single station loaded using
# the THEMIS module

# import required modules
import numpy as np
import matplotlib.pyplot as plt
import gmag.arrays.themis as themis

# define start and end dates for plotting
sdate = '2011-04-09 05:30:00'
edate = '2011-04-09 06:30:00'

# load data
th_dat, th_meta = themis.load(['SNKQ'],sdate,ndays=1)

# plot all data in the DataFrame between
# sdate and edate
th_dat[sdate:edate].plot(ylabel='nT', xlabel='Time - UT', figsize=[6,6],subplots=True)
plt.title(sdate[0:11]+' Substorm',y=3.35)
```

### Multi-Panel Plot

Create a multi-panel plot of the H component magnetic field from select CARISMA magnetometer stations using the ```carisma``` module. 

```python
# Plot multi-panel plot of the H compoment
# magnetic field for select CARSIMA stations

# import required modules
import gmag.arrays.carisma as carisma
import numpy as np
import matplotlib.pyplot as plt

# define start and end date for plotting and loading
# assume a single day is loaded
sdate = '2005-07-17 08:00:00'
edate = '2005-07-17 12:30:00'

# define component to be plotted
comp='H'

# load data
car_dat, car_meta=carisma.load(['GILL','ISLL','PINA','RABB','FSMI','FSIM','MCMU'],sdate)

# find the correct columns of the DataFrame
p_col = [col for col in car_dat.columns if col[-1] == comp]

# plot the DataFrame between sdate and edate 
# plot only p_col columns and subtrac the mean from each column
# before plotting
car_dat[sdate:edate][p_col].subtract(car_dat[p_col].mean()).plot(ylabel='nT', xlabel='Time - UT',
                                                            figsize=[6,10],subplots=True)
plt.title(sdate[0:11]+' Substorm/Pseudobreakup',y=8.25)
```

### Multi-Station Stacked Plot

Create a single panel stacked plot of the H component magnetic field from CARISMA stations apart of the Churchill line.

```python
# plot a stacked plot of CARISMA the H component
# magnetic field for stations along the Churchill line

# import required modules
import gmag.arrays.carisma as carisma
import numpy as np
import matplotlib.pyplot as plt

# define start and end date for plotting 
# use start date for loading data
sdate = '2014-11-05 13:25:00'
edate = '2014-11-05 14:25:00'

# define component for plotting
comp='H'

# load data
car_dat, car_meta=carisma.load(['PINA','ISLL','GILL','FCHU','RANK'],sdate)

# find the columns from the loaded DataFrame that have comp
# in the title, these are the columns that will be plotted
p_col = [col for col in car_dat.columns if col[-1] == comp]

# determine the shift to apply to each time series so that they don't
# overlatp

# the shift is determined using the DataFrame returned by the describe()
# method which stores the DataFrame stats including max and min of each column
# only use columns from p_col and values between the start and end of plotting
# defined by sdate and edate
# the shift in the y direction is defined by 1.5 times the range of the series
y_shift = np.array([(val['max']-val['min'])/1.5 for col_h, val in car_dat[sdate:edate][p_col].describe().iteritems()])

# the cumsum() method determines the cumalitative sum up
# to each index
# the cumsum() ensures timeseries don't overlap
y_shift = (y_shift-y_shift.min()).cumsum()

# plot p_col columns of the data frame between sdate and edate
# subtract the mean from each time series and apply the y-shit
car_dat[sdate:edate][p_col].subtract(car_dat[sdate:edate][p_col].mean()-y_shift).plot(ylabel='nT', xlabel='Time - UT',
                                                            figsize=[6,10])
plt.title(sdate[0:11]+' ULF Wave')
```