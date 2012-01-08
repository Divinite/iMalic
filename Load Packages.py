#!/usr/bin/python

import os
import glob

# A whole bunch of defines
MasterPackages={}
package="Package"
version="Version"

path = '/var/lib/apt/lists'
for  packages in glob.glob( os.path.join(path, '*_Packages') ):
    repo = packages.split(path)[1].split('/')[1] # gets the repo url
    print repo+'> '
    RepoDict = {}
    reader = open(packages)
    PackageDict={}
    for line in reader.readlines():
        line=line.split('\n')[0].split('\r')[0]
        if len(line) >= 1:
            if line.startswith('Package: '):
                PackageDict[package]=line.split(': ')[1]
            elif line.startswith('Version'):
                PackageDict[version]=line.split(': ')[1]
        else: # newline, commit to repodict
            try:
                RepoDict[PackageDict[package]]=PackageDict
                PackageDict={}
            except KeyError:
                pass
#                print "Warning...problem lading "
#                print PackageDict
#                print RepoDict
#                print line
#                print packages
#                print repo
#                raw_input()
    reader.close()
    MasterPackages[repo]=RepoDict
raw_input("All Packages Loaded, press enter to view")
writer = open("output",'w')
writer.write(str(MasterPackages))
writer.close()
print MasterPackages