#!/usr/bin/python3
# -*- coding: UTF-8 -*-
print("Content-Type: text/html")
print('')
import subprocess
import os
#cmd = os.system('echo ls')
# enable debugging
import cgitb
cgitb.enable()
proc = subprocess.Popen(['/bin/ls', '/'])

print('''
<head>
<body bgcolor="#F0F8FF">
</head>
<html>
<body>
''')

print('Hi')
print(proc)
print('</body></html>')
