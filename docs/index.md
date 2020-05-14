---
layout: default
---

# Overview

This code provides the utility to download and load data from various ground-based magtometer arrays. The code for is divided into a seperate module for each array. These are the **CARISMA**, **IMAGE**, and **THEMIS** modules. 

The ```carisma``` module loads data from the CARISMA magnetometer array.

The ```image``` modules loads data from the IMAGE magnetometer array.

The ```themis``` modules loads data from the THEMIS EPO and GBO, CARISMA, CANMOS, AUTUMN and AUTUMN X, DTU, IMAGE, GIMA, MACCS, McMAC, USGS, and PENGUIN arrays. When using the **THEMIS** module be sure to properly acknowledge **each** array whose data is used. 

[Arrays and Stations][1]

## Installation

To install the module clone the repository and within the repository directory type ```pip install -e .```

## gmagrc

The ```gmagrc``` file defines the local directory where magnetoemter data is downloaded.

*   CARISMA files: local_dir\CARISMA\YYYY\MM\DD\station.file
*   IMAGE files: local_dir\IMAGE\YYYY\MM\array_day.file
*   THEMIS files: local_dir\THEMIS\site\YYYY\station.file

The ```carisma``` and ```themis``` modules download a daily file for each station. The ```image``` module downloads a single file including data from multiple stations each day. 

The ```gmagrc``` files also defines the web address to download data for each array. If the addreses change they can be updated here. 

## Station Parameters

The names of stations, 4 letter codes, home array, geographic and geomagnetic coordinates, L-shell, and declinations are stored in [yearly files][2] and can be loaded with ```????```. These files and the declinations are used to rotate **CARISMA** and **IMAGE** date from  geographic (XYZ) to geomagnetic coordinates (HDZ, or heZ). This is done using: 

H = X cos(dec) + Y sin(dec)
D = Y cos(dec) - H sin(dec)

Data loaded using the ```themis``` module is not rotated as the data is generally already in geomagnetic coordinates. Details on the processing of the ground-based magnetometer data from THEMIS can be found [here][3]. 

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

Text can be **bold**, _italic_, or ~~strikethrough~~.

[Link to another page](./another-page.html).

There should be whitespace between paragraphs.

There should be whitespace between paragraphs. We recommend including a README, or a file with information about your project.

# Header 1

This is a normal paragraph following a header. GitHub is a code hosting platform for version control and collaboration. It lets you and others work together on projects from anywhere.

## Header 2

> This is a blockquote following a header.
>
> When something is important enough, you do it even if the odds are not in your favor.

### Header 3

```js
// Javascript code with syntax highlighting.
var fun = function lang(l) {
  dateformat.i18n = require('./lang/' + l)
  return true;
}
```

```ruby
# Ruby code with syntax highlighting
GitHubPages::Dependencies.gems.each do |gem, version|
  s.add_dependency(gem, "= #{version}")
end
```

#### Header 4

*   This is an unordered list following a header.
*   This is an unordered list following a header.
*   This is an unordered list following a header.

##### Header 5

1.  This is an ordered list following a header.
2.  This is an ordered list following a header.
3.  This is an ordered list following a header.

###### Header 6

| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |

### There's a horizontal rule below this.

* * *

### Here is an unordered list:

*   Item foo
*   Item bar
*   Item baz
*   Item zip

### And an ordered list:

1.  Item one
1.  Item two
1.  Item three
1.  Item four

### And a nested list:

- level 1 item
  - level 2 item
  - level 2 item
    - level 3 item
    - level 3 item
- level 1 item
  - level 2 item
  - level 2 item
  - level 2 item
- level 1 item
  - level 2 item
  - level 2 item
- level 1 item

### Small image

![Octocat](https://github.githubassets.com/images/icons/emoji/octocat.png)

### Large image

![Branching](https://guides.github.com/activities/hello-world/branching.png)


### Definition lists can be used with HTML syntax.

<dl>
<dt>Name</dt>
<dd>Godzilla</dd>
<dt>Born</dt>
<dd>1952</dd>
<dt>Birthplace</dt>
<dd>Japan</dd>
<dt>Color</dt>
<dd>Green</dd>
</dl>

```
Long, single-line code blocks should not wrap. They should horizontally scroll if they are too long. This line should be long enough to demonstrate this.
```

```
The final element.
```

[1]: ftp://apollo.ssl.berkeley.edu/pub/THEMIS/3%20Ground%20Systems/3.2%20Science%20Operations/Science%20Operations%20Documents/GMAG_Station_Data_Processing_Notes.pdf
[2]: ftp://apollo.ssl.berkeley.edu/pub/THEMIS/3%20Ground%20Systems/3.2%20Science%20Operations/Science%20Operations%20Documents/GMAG_Station_Data_Processing_Notes.pdf
[3]: ftp://apollo.ssl.berkeley.edu/pub/THEMIS/3%20Ground%20Systems/3.2%20Science%20Operations/Science%20Operations%20Documents/GMAG_Station_Data_Processing_Notes.pdf