#!/usr/bin/python

import os
import glob

# A whole bunch of defines
MasterPackages=shelve.open(myfile,)

Tags=['Package', 'Name', 'Section', 'Description']

path = '/var/lib/apt/lists'
for packagesfile in glob.glob( os.path.join(path, '*_Packages') ):
    with open(packages) as reader:
        for line in reader:
            line=line.strip()
            if line == '':
                if LastTag != "Description":
                    if PkgInfo.has_key('Package'):
                        PackageID=PkgInfo['Package']
                        del PkgInfo['Package']
                        if MasterPackages.has_key(PackageID): # TODO:
                            pass # check version number to find out which is newer
                        MasterPackages[PackageID]=PkgInfo
                        PkgInfo={}
            elif len(line.split(': ',1)) == 2:
                line=line.split(':', 1)
                if line[0] in Tags:
                    LastTag=line[0]
                    PkgInfo[line[0]]=line[1]
            else:
                if line.startswith(' '):
                    PkgInfo['Description']=PkgInfo[Description]+line+"\n"
raw_input("All Packages Loaded, press enter to view")
writer = open("output",'w')
writer.write(str(MasterPackages))
writer.close()

print "<table>"
for PID in MasterPackages:
    print "<tr><td>", MasterPackages[PID["Name"]], "</td></tr>"
print "</table>"