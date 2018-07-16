#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

# enable debugging
import cgitb
cgitb.enable()

print("Content-Type: text/html")
print()

print('''
<head>
<h1>Download Page</h1>
<body bgcolor="#F0F8FF">
</head>

<body>
<form name="search" action="/cgi-bin/down.py" method="get">
Show/Film: <input type="text" name="searchbox">
<br><p>&#x25BC;leave blank if searching for a film ... obviously&#x25BC;</p>
<form name="search" action="/cgi-bin/down.py" method="get">
Season : <input type="checkbox" name="seasonall" onchange="toggleDisabledS(this.checked)" value="sall"> < Check for all or enter season number > <input type="text" name="seasonsearch" id="stb">
<br>
<form name="search" action="/cgi-bin/down.py" method="get">
Episode: <input type="checkbox" name="episodeall" onchange="toggleDisabledE(this.checked)" id="echk" value="eall"> < Check for all or enter episode number><input type="text" name="episodesearch" id="etb">
<br><input type="submit" value="Submit">
</form>

<script>
function toggleDisabledS(_checked) {
    document.getElementById('stb').disabled = _checked ? true : false;
    document.getElementById('etb').disabled = _checked ? true : false;
    document.getElementById('echk').disabled = _checked ? true : false;
}
function toggleDisabledE(_checked) {
    document.getElementById('etb').disabled = _checked ? true : false;
}
</script>

</body>
''')

