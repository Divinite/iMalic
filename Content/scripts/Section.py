#!/usr/bin/python

import sqlite3
import time

StartTime=time.time()
DBTable = 'AvailablePacakges'
DBFolder = 'Cache'
DBPath = DBFolder+'/Master.sqlite'

db = sqlite3.connect(DBPath)
c = db.cursor()

tags=['Name','Package']
try:
    t = (request['Section'][0],)
except KeyError:
    print 'No Section Specified'
    print request
    exit()
query='SELECT '+",".join(tags)+' FROM '+DBTable+' WHERE '+DBTable+'.Section=?'
c.execute(query,t)

PackageList={}
for row in c:
    # PackageList[PID]=Package Name
    if row[0] != '?':
        PackageList[str(row[1])]=str(row[0])
    else:
        PackageList[str(row[1])]=str(row[1])

for PID in PackageList:
    print '<div id="PackageList"><a href="Package.py?Package='+PID+'">'+PackageList[PID]+'</a></div>'
c.close()
db.close()

print time.time()-StartTime
