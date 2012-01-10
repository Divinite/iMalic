#!/usr/bin/python

from __future__ import with_statement
import os
import glob
from buzhug import Base

path = '/var/lib/apt/lists'

Tags=['Package', 'Name', 'Section', 'Description', 'Publisher', 'IconName',
      'dev', 'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon',
      'Depiction', 'Filename', 'MD5sum', 'Size', 'Maintainer', 'Sponsor',
      'SHA256', 'Version', 'Architecture', 'Author', 'Priority', 'SHA1', 'tag',
      'Conflicts', 'Replaces',  'price',
      'appsidydev', 'Essential', 'Bundle', 'Website', 'Suggests', 'Provides',
      'Price', 'Languages', 'Support', 'More', 'Recommends', 'Enhances']
        # damn reserved keywords!
        #'Pre-Depends', 'Installed-Size', <----python no like
        # i'll figure out how to fix it later
        

db = Base('../Cache/db')
try:
    db.create()
    for tag in Tags:
        db.add_field(tag, str)
except IOError: # already exists
    if raw_input('Database exists, clear it? [Y/n] '):
        db.destroy()
        db.create()
        for tag in Tags:
            db.add_field(tag, str)
    else:
        db.open()

def CommitPackage (Package={}): # define as {} for auto complete purposes
    if 'Package' in Package:
        print 'Processing ' + Package['Package']
        for tag in Tags:
            if not tag in Package:
                Package[tag]=''
        # I Have a feeling that this is going to be ugly :(
        db.insert(Package=Package['Package'],  Name=Package['Name'],
                  Section=Package['Section'],
                  Description=Package['Description'],
                  Publisher=Package['Publisher'],  IconName=Package['IconName'],
                  dev=Package['dev'],  Contact=Package['Contact'],
                  Source=Package['Source'],  Tag=Package['Tag'],
                  Depends=Package['Depends'],  Homepage=Package['Homepage'],
                  Icon=Package['Icon'],  Depiction=Package['Depiction'],
                  Filename=Package['Filename'],  MD5sum=Package['MD5sum'],
                  Size=Package['Size'],  Maintainer=Package['Maintainer'],
                  Sponsor=Package['Sponsor'],  SHA256=Package['SHA256'],
                  Version=Package['Version'],
                  Architecture=Package['Architecture'],
                  Author=Package['Author'],  Priority=Package['Priority'],
                  SHA1=Package['SHA1'],  tag=Package['tag'],
                  Conflicts=Package['Conflicts'],  Replaces=Package['Replaces'],
#                  Pre-Depends=Package['Pre-Depends'], # see line 17
#                 Installed-Size=Package['Installed-Size'], # ^
                  price=Package['price'],  appsidydev=Package['appsidydev'],
                  Essential=Package['Essential'],  Bundle=Package['Bundle'],
                  Website=Package['Website'],  Suggests=Package['Suggests'],
                  Provides=Package['Provides'],  Price=Package['Price'],
                  Languages=Package['Languages'],  Support=Package['Support'],
                  More=Package['More'],  Recommends=Package['Recommends'],
                  Enhances=Package['Enhances'])
        # yes ugly would be an understatment
        
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
                        else:
                            pass
                            # discard the info because idk what to do with it
            else:
                if LastTag == 'Description': # some descriptions have blank lines
                    PkgInfo['Description']=PkgInfo['Description'] + '\n' #apt is almost nastier than HTMl
                elif 'Package' in PkgInfo: # the problem is that you have to account for all
                    CommitPackage(PkgInfo)       # stupid things people can do, and do all the
                    PkgInfo={}                   # time and expect to work
                else:
                    pass
                    # idk what to do so I'll do nothing
                    
db.close()