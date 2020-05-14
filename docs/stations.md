---
layout: default
---

# Stations

### Geomagnetic Coordinates

[2000][1] [2001][2] [2002][3] [2004][4] [2004][5] [2005][6] [2006][7] [2007][8] [2008][9] [2009][10] 

[2010][11] [2011][12] [2012][13] [2013][14] [2014][15] [2015][16] [2016][17] [2017][18] [2018][19] [2019][20] 

### Map


### Geographic Coordinates

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


[1]: ./stations_2000.md
[2]: ./stations_2001.md
[3]: ./stations_2002.md
[4]: ./stations_2003.md
[5]: ./stations_2004.md
[6]: ./stations_2005.md
[7]: ./stations_2006.md
[8]: ./stations_2007.md
[9]: ./stations_2008.md
[10]: ./stations_2009.md
[11]: ./stations_2010.md
[12]: ./stations_2011.md
[13]: ./stations_2012.md
[14]: ./stations_2013.md
[15]: ./stations_2014.md
[16]: ./stations_2015.md
[17]: ./stations_2016.md
[18]: ./stations_2017.md
[19]: ./stations_2018.md
[20]: ./stations_2019.md