#!/usr/bin/python

import sqlite3

DBTable = 'AvailablePacakges'
DBFolder = '../Cache'
DBPath = DBFolder+'/Master.sqlite'

db = sqlite3.connect(DBPath)
c = db.cursor()
tags=['Name','Section', 'Version', 'Filename', 'Publisher', 'Status', 'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon',]

print 'Enter a Section to Look Up\nPress ^C to Exit'
while True:
    PID=raw_input('\nSection Name> ') 
    c.execute('SELECT '+','.join(tags)+' FROM '+DBTable+' WHERE '+DBTable+".Section='"+PID+"'")
    i = 0
    for row in c:
        i += 1
        print
        print 'Result '+str(i)
        o = 0
        for tag in tags:
            print tag + ': ' + str(row[o])
            o += 1
    if i == 0 :
        print 'No Packages Found'
