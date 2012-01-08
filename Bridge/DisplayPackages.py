#!/usr/bin/python

import os

MasterPackages={}

def readFile(fileHandle, dictName): 

     line = fileHandle.readline() 
     dictName = {} 
     keycounter = 1 

     while line: 
         key = str(keycounter) 
         dictName[key] = line 
         keycounter = keycounter + 1 
         line = fileHandle.readline() 

     return dictName

reader = open("output")
readFile(reader, MasterPackages)
reader.close()

#print MasterPackages

type(MasterPackages)
print "<table>"
for PID in MasterPackages:
    print "<tr><td>", MasterPackages[PID], "</td></tr>"
print "</table>"
