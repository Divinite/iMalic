#!/usr/bin/python

import sqlite3
import time

StartTime=time.time()
DBTable = 'AvailablePacakges'
DBFolder = '../Cache'
DBPath = DBFolder+'/Master.sqlite'

db = sqlite3.connect(DBPath)
c = db.cursor()
Tags=['Package', 'Name', 'Section', 'Description', 'Publisher', 'Status',
      'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon', 'Depiction',
      'Filename', 'MD5sum', 'Size', 'Maintainer', 'Sponsor', 'SHA256',
      'Version', 'Architecture', 'Author', 'Priority', 'SHA1', 'Conflicts',
      'Replaces',  'Price', 'Essential', 'Bundle', 'Website', 'Suggests',
      'Provides', 'Languages', 'Support', 'More', 'Recommends', 'Enhances',
      'Dev', 'Breaks', 'Repo' ]

PID=request['Package'][0]
c.execute('SELECT '+','.join(Tags)+' FROM '+DBTable+' WHERE '+DBTable+".Package='"+PID+"'")
i = 0

print '<html><body>'

PkgInfo={}
for row in c:
    i += 1
    o = 0
    for tag in Tags:
        if str(row[o]) != '?':
            PkgInfo[tag] = str(row[o])
        o += 1
    
    if 'Icon' in PkgInfo:
        import subprocess # once again, bad form, but better performace
        # safari doesn't like file:// links
        subprocess.Popen(['cp',PkgInfo['Icon'].replace('file://',''),'/var/root/iMalic/FrontEnd/Icons'])
        Icon='Icons/'+PkgInfo['Icon'].replace('file://','').split('/')[-1:][0]
        print '<a href="'+Icon+'"><img src="'+Icon+'" height="64", width="64"></a><br>'
    if 'Name' in PkgInfo:
        print PkgInfo['Name']+'<br>'
    else:
        print PkgInfo['Package']+'<br>'
    if 'Version' in PkgInfo:
        print 'Version: '+PkgInfo['Version']
    if 'Description' in PkgInfo:
        print '<br><br>'+PkgInfo['Description']+'<br>'
if i == 0 :
    print 'Package Not Found :('

print '<br><h7>Page Generated in',time.time()-StartTime, 'Seconds</h7>'
print '</body></html>'