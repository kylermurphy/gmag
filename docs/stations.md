---
layout: default
---

# Stations

## Geomagnetic Coordinates

A table of Geomagnetic coordinates for 2000-2019, mapped to 100 km altitude using [IGRF12][1] and [aacgmv2][2] are below.

<div class="display compact" style="height:100%; width:100%; overflow:auto;">
{% for row in site.data.year %}
    <a href='./cgm_{{ row.year }}.html'>{{ row.year }} </a>
{% endfor %}
<br>
<br>
</div>


## Map

<iframe src="https://kylermurphy.github.io/gmag/assets/stn_map.html" width="650" height="400"></iframe>


## Geographic Coordinates

**Table can be organized by column and is searchable.**

<div class="display compact" style="height:100%; width:100%; font-size:	12px; overflow:auto;">

<table id="catalogue" class="display">
<thead>
<tr class="header">
<th style="font-size: 16px" data-sort>Array</th>
<th style="font-size: 16px">Code</th>
<th style="font-size: 16px">Name</th>
<th style="font-size: 16px">Latitude</th>
<th style="font-size: 16px">Longitude</th>

</tr>
</thead>
<tbody>

{% for row in site.data.station_list %}
  <tr>
  <td> {{ row.Array }} </td>
  <td> {{ row.Code }}</td>
  <td> {{ row.Name}} </td>
  <td> {{ row.Latitude }} </td>
  <td> {{ row.Longitude }} </td>
  </tr>
{% endfor %}
</tbody>
</table>

</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>

<script type="text/javascript"
        src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

<script>
 
$(document).ready(function() {
    $("#catalogue").dataTable( {
        paging: false,
        'data-sort': true,
        order: [[ 0, "desc" ], [3, "desc"]],
        stateSave: true,
        searching: true
    });
});
</script>


[1]: https://github.com/space-physics/igrf12
[2]: https://github.com/aburrell/aacgmv2