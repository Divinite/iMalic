#!/usr/bin/python

import time
import shelve

StartTime=time.time()

Sections=shelve.open('../Cache/SectionsList', writeback=True)

if not 'Unknown' in Sections:
    # bad practive not importing at the script's start
    # but this really helps with perfomance
    import sqlite3
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


    Sections['Unknown']=0
    c.execute('SELECT Section From '+DBTable)
    for result in c:
        if  str(result[0]) in Sections:
            Sections[str(result[0])] += 1
        elif str(result[0]) == '?':
            Sections['Unknown'] += 1
        else: # result no in list
            Sections[str(result[0])] = 1

for section in Sections:
    print '<div id = "sections">' + section + ' (' + str(Sections[section])+ ') Packages </div>'
print time.time()-StartTime
