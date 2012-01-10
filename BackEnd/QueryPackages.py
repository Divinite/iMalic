#!/usr/bin/python

print 'Loading...' # the import takes a moment, so that's why I'm doing it here

from buzhug import Base 

db=Base('../Cache/db')
try:
    db.open()
except IOError:
    print 'Error: db not found!'
    exit()

print 'Querying db for packages...'
i = 0
for record in db :
    i = i + 1

print 'Loaded ' + str(i) + ' Packages'
print 'Please enter the package id that you wish to look up'
print 'Press ^C to exit'
while True:
    ID = raw_input('\nPackage ID> ')
    record = db.select(Package = ID)
    if record != []:
        print record[0]
    else:
        print "Package no found"