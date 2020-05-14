---
layout: default
---

# Empty

<div class="display compact" style="height:100%; width:140%; font-size:	12px; overflow:auto;">

<table id="catalogue" class="display sortable">
<thead>
<tr class="header">
<th style="font-size: 16px">Array</th>
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


