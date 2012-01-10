#!/usr/bin/python

from __future__ import with_statement
import os
import glob
import shelve

PkgBrowse = shelve.open('../Cache/PkgBrowse', flag='c')
Sections = shelve.open('../Cache/Sections', flag='c')
i = 0

# Magic command to get urls
# ls -1 /var/lib/apt/lists| grep Packages | grep -v Packages.|  sed -e 's|_Packages||' | tr '_' '/'


def CommitPakgage(pkg):
    if 'Package' in pkg:
        global i
        i = i + 1
        PID=pkg['Package'].replace(' ','')
        print str(i) + ' Processing ' + PID 
        del pkg['Package'] 
        PkgBrowse[PID]={}
        if not 'Section' in pkg:
            pkg['Section'] = 'No Catagory'
        if not pkg['Section'] in Sections:
            Sections[pkg['Section']]={} # if there is no dictionary for this section, create one
        Sections[pkg['Section']][PID]='../Cache/Packages/'+PID
        PackageInfo = shelve.open('../Cache/Packages/'+PID, flag='c')
        if 'Name' in pkg:
            PackageInfo['Name'] = pkg['Name']
            PkgBrowse[PID]['Name'] = pkg['Name']
        else:
            PackageInfo['Name'] = PID
            PkgBrowse[PID]['Name'] = PID
        if 'Icon' in pkg:
            PkgBrowse[PID]['Icon'] = pkg['Icon']
        for tag in pkg:
            if tag != 'Section': # to avoid storing section as well
                PackageInfo[tag] = pkg[tag]
        PackageInfo.close()
    else:
        #screw it, if there is no package id we can't install it
        #so just forget recording it at all
        return None # that should stop the execution of this function\

Tags=['Package', 'Name', 'Section', 'Description'] #, 'Publisher', 'IconName',
'''
      'dev', 'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon',
      'Depiction', 'Filename', 'MD5sum', 'Size', 'Maintainer', 'Sponsor',
      'SHA256', 'Version', 'Architecture', 'Author', 'Priority', 'SHA1', 'tag',
      'Conflicts', 'Replaces', 'Pre-Depends', 'Installed-Size', 'price',
      'appsidydev', 'Essential', 'Bundle', 'Website', 'Suggests', 'Provides',
      'Price', 'Languages', 'Support', 'More', 'Author',
      'Recommends', 'Enhances']
'''

path = '/var/lib/apt/lists'

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
                        else:
                            pass
                            # discard the info because idk what to do with it
            else:
                if LastTag == 'Description': # some descriptions have blank lines
                    PkgInfo['Description']=PkgInfo['Description'] + '\n' #apt is almost nastier than HTMl
                elif 'Package' in PkgInfo: # the problem is that you have to account for all
                    CommitPakgage(PkgInfo)       # stupid things people can do, and do all the
                    PkgInfo={}                   # time and expect to work
                else:
                    pass
                    # idk what to do so I'll do nothing

PkgBrowse.close()
Sections.close()
print "Updated Cache"
