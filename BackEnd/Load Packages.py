#!/usr/bin/python

import os
import glob
import shelve

PkgBrowse = shelve.open('../Cache/PkgBrowse', writeback=True)
Sections = shelve.open('../Cache/Sections', writeback=True)


# Magic command to get urls
# ls -1 | grep Packages | grep -v Packages.|  sed -e 's|_Packages||' | tr '_' '/'

def CommitPakgage(pkg):
    if pkg.has_key('Package'):
        PID=pkg['Package'].replace(' ','')
        del pkg['Package'] 
        print 'Processing ' + PID
        PkgBrowse[PID]={}
        if not pkg.has_key('Section'):
            pkg['Section'] = 'No Catagory'
        if not Sections.has_key(pkg['Section']):
            Sections[pkg['Section']]={} # if there is no dictionary for this section, create one
        Sections[pkg['Section']][PID]=shelve.open('../Cache/Packages/'+PID,writeback=True)
        if pkg.has_key('Name'):
            Sections[pkg['Section']][PID]['Name'] = pkg['Name']
            PkgBrowse[PID]['Name'] = pkg['Name']
        else:
            Sections[pkg['Section']][PID]['Name'] = PID
            PkgBrowse[PID]['Name'] = PID
        if pkg.has_key('Icon'):
            PkgBrowse[PID]['Icon'] = pkg['Icon']
        for tag in pkg:
            if tag != 'Section': # to avoid storing section as well
                Sections[pkg['Section']][PID][tag] = pkg[tag]
        Sections[pkg['Section']][PID].close()
    else:
        #screw it, if there is no package id we can't install it
        #so just forget recording it at all
        return None # that should stop the execution of this function\

Tags=['Package', 'Name', 'Section', 'Description', 'Publisher', 'IconName',
      'dev', 'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon',
      'Depiction', 'Filename', 'MD5sum', 'Size', 'Maintainer', 'Sponsor',
      'SHA256', 'Version', 'Architecture', 'Author', 'Priority', 'SHA1', 'tag',
      'Conflicts', 'Replaces', 'Pre-Depends', 'Installed-Size', 'price',
      'appsidydev', 'Essential', 'Bundle', 'Website', 'Suggests', 'Provides',
      'Price', 'Languages', 'Support', 'More', 'Author',
      'Recommends', 'Enhances']

path = '/var/lib/apt/lists'
i = 0
o = 0 
for packagesfile in glob.glob( os.path.join(path, '*_Packages') ):
    reader = open(packagesfile)
    PkgInfo={}
    NullCount=0
    LastTag=''
    line = reader.readline()
    while True: # the NullCount Var will break when we reach 100 null lines
        i = i + 1
        line=line.strip()
        if line != '':
            line = line.split(': ',1)
            if len(line) == 2: # looks like there is a tag there
                if line[0] in Tags:
                    LastTag = line[0]
                    if PkgInfo.has_key(line[0]):
                        if line[0] == 'Package':
                            print 'Warning Overwriting '
                            print '   ' + line[0] + ': ' + PkgInfo[line[0]]
                            print 'With:'
                            print '   ' + line[0] + ': ' + line[1]
                            o = o + 1
                    PkgInfo[line[0]] = line[1]
                    # aka pkginfo[tag] = value
                else: # it looks like a tag, but isn't
                    if PkgInfo.has_key('Description') :
                        PkgInfo['Description']=PkgInfo['Description']+'\n'+line[0]+': '+line[1]
                        # add the value to the description
                    else:
                        print 'Warning: Discarding ' + line[0] + ': ' + line [1]
                        raw_input()
                        # discard the info because idk what to do with it
        else:
            if LastTag == 'Description': # some descriptions have blank lines
                PkgInfo['Description']=PkgInfo['Description'] #apt is almost nastier than HTMl
            elif PkgInfo.has_key('Package'): # the problem is that you have to account for all
                CommitPakgage(PkgInfo)       # stupid things people can do, and do all the
                PkgInfo={}                   # time and expect to work
            else:
                print 'Warning Null Line Falling Through'
                raw_input()
            NullCount = NullCount + 1
            if NullCount == 100:
                break
            
        line = reader.readline()
PkgBrowse.close()
Sections.close()
print "Updated Cache"
print 'Read ' + str(i) +' lines'
print 'Overwrote ' + str (o) +' Packages'