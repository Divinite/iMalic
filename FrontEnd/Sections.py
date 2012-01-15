#!/usr/bin/python

import sqlite3
import shelve

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


Sections=shelve.open('../Cache/SectionsList', writeback=True)
if not 'Unknown' in Sections:
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
