#!/usr/bin/python

import shelve

print 'Loading...'

PkgBrowse = shelve.open('../Cache/PkgBrowse', writeback=False)
Sections = shelve.open('../Cache/Sections', writeback=False)

i = 0
for PID in PkgBrowse:
    i = i + 1

print 'Loaded ' + str(i) + ' Packages'
print 'Enter a Package id to query, or press ^C to exit'
while True:
    PID = raw_input('\nPackage ID> ')
    if PID in PkgBrowse:
        Package = shelve.open('../Cache/Packages/'+PID, writeback=False)
        print PID + ':'
        for tag in Package:
            print '    ' + tag + ': ' + Package[tag]
        Package.close()