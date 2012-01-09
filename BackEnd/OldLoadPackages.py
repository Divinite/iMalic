#!/usr/bin/python

import os
import glob
import shelve

MasterPackages=shelve.open('../Cache/MasterPackages', writeback=True)

# Magic command to get urls
# ls -1 | grep Packages | grep -v Packages.|  sed -e 's|_Packages||' | tr '_' '/'

Tags=['Package', 'Name', 'Section', 'Description', 'Publisher', 'IconName',
      'dev', 'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon',
      'Depiction', 'Filename', 'MD5sum', 'Size', 'Maintainer', 'Sponsor',
      'SHA256', 'Version', 'Architecture', 'Author', 'Priority', 'SHA1', 'tag',
      'Conflicts', 'Replaces', 'Pre-Depends', 'Installed-Size', 'price',
      'appsidydev', 'Essential', 'Bundle', 'Website', 'Suggests', 'Provides',
      'Price', 'Languages', 'Support', 'More', 'Author',
      'Recommends', 'Enhances']

path = '/var/lib/apt/lists'
for packagesfile in glob.glob( os.path.join(path, '*_Packages') ):
    reader = open(packagesfile)
    PkgInfo={}
    untags=[]
    NullCount=0
    LastTag=''
    line = reader.readline()
    while True: # the NullCount Var will break when we reach 100 null lines
        line=line.strip()
        if line == '':
            if LastTag != "Description":
                if PkgInfo.has_key('Package'):
                    PackageID=PkgInfo['Package']
                    del PkgInfo['Package']
                    if MasterPackages.has_key(PackageID): # TODO:
                        pass # check version number to find out which is newer
                    MasterPackages[PackageID]=PkgInfo
                    print PackageID
                    PkgInfo={}
                else:
                    NullCount=NullCount+1
                    if NullCount == 100:
                        NullCount = 0
                        reader.close()
                        break
            else:
                PkgInfo["Description"]=PkgInfo["Description"]+'\n'
        elif len(line.split(': ', 1)) == 2:
            line=line.split(': ', 1)
            if line[0] in Tags:
                LastTag=line[0]
                PkgInfo[line[0]]=line[1]
            else:
                if LastTag == 'Description':
                    line=line[0]+': '+line[1]
                    if  line.startswith(' '): #descriptions should be indented by one space
                        PkgInfo['Desciption']=PkgInfo['Description']+'\n'+line
                #if it fails all of these tests then idk what that data is
        else:
            if PkgInfo.has_key('Descriptiom'):
                PkgInfo['Description']=PkgInfo[Description]+'\n'+line
        line = reader.readline()
MasterPackages.close()
print "Updated Cache"