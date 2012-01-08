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
    raw_input()
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
                #print "Finished with ", PackageDict
                PackageDict={}
            except KeyError:
                print "Warning...problem lading "
                print PackageDict
                print RepoDict
                print line
                print packages
                print repo
                raw_input()
    reader.close()
    MasterPackages[repo]=RepoDict
    
print MasterPackages