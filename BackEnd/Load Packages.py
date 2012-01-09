#!/usr/bin/python

import os
import glob
import shelve

PkgBrowse = shelve.open('../Cache/PkgBrowse', writeback=True)
Sections = shelve.open('../Cache/Sections', writeback=True)


# Magic command to get urls
# ls -1 | grep Packages | grep -v Packages.|  sed -e 's|_Packages||' | tr '_' '/'

def CommitPakgage(pkg):
    if pkg.has_key('Section'):
        if not Sections.has_key(pkg['Section']):
            Sections[pkg['Section']]={}
        if pkg.has_key('Package'):            
            Sections[pkg['Section']][pkg['Package']]=shelve.open('../Cache/Packages/'+pkg['Package'],writeback=True)
            for tag in pkg:
                
            Sections[pkg['Section']][pkg['Package']]
            if pkg.has_key('Name'): # just to be explicit
                Sections[pkg['Section']][pkg['Package']]['Name'] = pkg['Name']
            else: # use the package id as the name
                Sections[pkg['Section']][pkg['Package']]['Name'] = pkg['Package']
            Sections[pkg['Section']][pkg['Package']].close()
        else:
            #screw it, if there is no package id we can't install it
            #so just forget recording it at all
            return None # that should stop the execution of this function
            
        


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
    NullCount=0
    LastTag=''
    line = reader.readline()
    while True: # the NullCount Var will break when we reach 100 null lines
        line=line.strip()
        if line != '':
            line = line.split(': ',1)
            if len(line) == 2: # looks like there is a tag there
                if line[0] in Tags:
                    LastTag = line[0]
                    PkgInfo[line[0]] = line[1]
                    # aka pkginfo[tag] = value
                else: # it looks like a tag, but isn't
                    if PkgInfo.has_key('Description') :
                        PkgInfo['Description']=PkgInfo['Description']+'\n'+line[0]+': '+line[1]
                        # add the value to the description
                    else:
                        pass
                        # discard the info because idk what to do with it
        else:
            if LastTag == 'Description': # some descriptions have blank lines
                PkgInfo['Description']=PkgInfo['Description'] #apt is almost nastier than HTMl
            elif PkgInfo.has_key('Package'): # the problem is that you have to account for all
                pass # commit package        # stupid things people can do, and do all the
            NullCount = NullCount + 1        # time and expect to work
            if NullCount == 100:
                break
            
        line = reader.readline()
MasterPackages.close()
print "Updated Cache"


'''
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
                '''