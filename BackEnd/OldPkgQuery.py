#!/usr/bin/python

import shelve

print 'Loading...'
MasterPackages=shelve.open('../Cache/MasterPackages') 

i = 0
for PID in MasterPackages:
    i = i + 1
 
print 'Loaded ' + str(i) + ' Packages'
print 'Please enter the package id that you wish to look up'
print 'Press ^C to exit'
while True:
    ID = raw_input('\nPackage ID> ')
    if MasterPackages.has_key(ID):
        print ID + ':'
        for tag in MasterPackages[ID]:
           print '  ' + tag + ': ' + MasterPackages[ID][tag]
    else:
        print 'Package Not Found'
