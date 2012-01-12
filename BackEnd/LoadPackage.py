#!/usr/bin/python

from __future__ import with_statement
import os
import sys
import glob
import sqlite3
import time

start_time = time.time()
TotalPackages=0
errors={}
path = '/var/lib/apt/lists'
DBPath = '../Cache/Packages.db'
Tags=['Package', 'Name', 'Section', 'Description', 'Publisher', 'IconName',
      'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon', 'Depiction',
      'Filename', 'MD5sum', 'Size', 'Maintainer', 'Sponsor', 'SHA256',
      'Version', 'Architecture', 'Author', 'Priority', 'SHA1', 'Conflicts',
      'Replaces',  'Price', 'Essential', 'Bundle', 'Website', 'Suggests',
      'Provides', 'Languages', 'Support', 'More', 'Recommends', 'Enhances',
      'Pre-Depends', 'Installed-Size']
        
print ('Warning this will destroy any existing databases')
if raw_input('Proceed? [y/N]: ') != 'y':
    exit()

try:
    os.system('rm '+DBPath+'>/dev/null 2>&1') # quick and dirty
except:
    pass 

db = sqlite3.connect(DBPath)
c = db.cursor()
c.execute('create table packages (Package string)')
db.commit()
for tag in Tags:
    if tag != 'Package':
        c.execute("alter table packages add column '" + tag + "' 'string'")
        db.commit()
c.close()

def CommitPackage(Package):
    if 'Package' in Package:
        global TotalPackages
        TotalPackages=TotalPackages+1
        print 'Processing ' + Package['Package']
        for tag in Tags:
            if not tag in Package:
                Package[tag]='?' # fill in the blanks
        cursor = db.cursor()
        TagList=[]
        for tag in Package:
            TagList.append("'"+Package[tag]+"'")
        query = 'INSERT INTO packages VALUES(%s)' % ','.join(['?'] * len(TagList))
        #print query
        #raw_input()
        try:
            cursor.execute(query, TagList)
        except:
            print 'Error: ', sys.exc_info()[0] #While Processing ', Package['Package']
            print query
            raw_input()
            return sys.exc_info()[0]
        db.commit()
        cursor.close()
    else:
        pass # no package ID, then there is nothing we can do with it

for packagesfile in glob.glob( os.path.join(path, '*_Packages') ):
    with open(packagesfile) as reader:
        PkgInfo={}
        LastTag=''
        for line in reader:
            line=line.strip()
            if line != '':
                line = line.split(': ',1)
                if len(line) == 2: # looks like there is a tag there
                    if line[0] in Tags:
                        LastTag = line[0]
                        PkgInfo[line[0]] = line[1]
                        # aka pkginfo[tag] = value
                    else: # it looks like a tag, but isn't
                        if 'Description' in PkgInfo :
                            PkgInfo['Description']=PkgInfo['Description']+'\n'+line[0]+': '+line[1]
                            # add the value to the description
                        else: # just to be explicit
                            pass # discard the info because idk what it is
            else:
                if LastTag == 'Description':# some descriptions have blank lines
                    PkgInfo['Description']=PkgInfo['Description'] + '\n' 
                elif 'Package' in PkgInfo:
                    PkgInfo['Package']=PkgInfo['Package'].replace(' ', '')
                    RetVal = CommitPackage(PkgInfo)
                    if RetVal != None:
                        errors[PkgInfo['Package']]=RetVal
                    PkgInfo={}
                else:
                    pass  # idk what to do with it so I'll do nothing
db.close()
print 'Loaded '+str(TotalPackages)+' Packages'
if len(errors) != 0:
    print "There were ",len(errors)," Errors during processing"
    raw_input('Press Enter To View')
    for PID in errors:
        print 'Encounter an ', errors[PID], ' when processing ', PID
print "Execution time: ", time.time() - start_time, "seconds"
