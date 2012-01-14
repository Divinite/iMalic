#!/usr/bin/python

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

print 'Enter a Package ID to Look Up\nPress ^C to Exit'
while True:
    PID=raw_input('\nPackage ID> ')
    c.execute('SELECT '+','.join(Tags)+' FROM '+DBTable+' WHERE '+DBTable+".Package='"+PID+"'")
    i = 0
    for row in c:
        i += 1
        print
        print 'Result '+str(i)
        o = 0
        for tag in Tags:
            if str(row[o]) != '?':
                print tag + ': ' + str(row[o])
            o += 1
    if i == 0 :
        print 'No Packages Found'
