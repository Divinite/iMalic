#!/usr/bin/python

from __future__ import with_statement
import os
import sys
import glob
import sqlite3
import time
import subprocess

start_time = time.time()
IDV={}
TotalPackages=0
errors={}
IDVersion={}
path = '/var/lib/apt/lists'
AvailableDBTable = 'AvailablePacakges'
InstallDBTable = 'InstalledPacakges'
DBFolder = 'Cache'
DBPath = DBFolder+'/Master.sqlite'
Tags=['Package', 'Name', 'Section', 'Description', 'Publisher', 'Status',
      'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon', 'Depiction',
      'Filename', 'MD5sum', 'Size', 'Maintainer', 'Sponsor', 'SHA256',
      'Version', 'Architecture', 'Author', 'Priority', 'SHA1', 'Conflicts',
      'Replaces',  'Price', 'Essential', 'Bundle', 'Website', 'Suggests',
      'Provides', 'Languages', 'Support', 'More', 'Recommends', 'Enhances',
      'Pre-Depends', 'Installed-Size', 'Dev', 'Breaks', 'Repo' ]

Tags=sorted(Tags) # just to keep the columns alphabetized
os.system('clear')
print '####################################################'
print '#                                          1/12/12 #'
print '#           iMalic DataBase Rebuild Tool           #'
print '#               Written By: Trcx528                #'
print '#               <Trcx528@gmail.com>                #' #I already regret
print '#                                                  #' # putting my email
print '#  Check Out iNinjas.com for more iPhone utilites! #' # on here, lol
print '#                                                  #'
print '####################################################'
print ''
print 'WARNING: This will destroy and rebuild iMalic\'s'
print 'package database! You must let the script finish'
print 'otherwise iMalic will be rendered unusable!\n'
print 'DO NOT use this tool, unless explicitly instructed'
print 'to by an advanced user.\n'
if not raw_input('Proceed? [y/N]: ') in [ 'y', 'Y', 'yes', 'YES' ]:
    exit()

subprocess.Popen(['mkdir','-p',DBFolder])
subprocess.Popen(['touch',DBPath])

db = sqlite3.connect(DBPath)
c = db.cursor()
c.execute('drop table if exists '+AvailableDBTable)
c.execute('drop table if exists '+InstallDBTable)
db.commit()
c.execute('create table ' + AvailableDBTable + ' (Package string)')
c.execute('create table ' + InstallDBTable + ' (Package string)')
db.commit()
for tag in Tags:
    if tag != 'Package':
        c.execute("alter table " + AvailableDBTable + " add column '" + tag +
                  "' 'string'")
        c.execute("alter table " + InstallDBTable + " add column '" + tag +
                  "' 'string'")
        db.commit()

print '\nThis will take a couple minutes.'
print 'Rebuild in process...please wait'

def Parse(line, PkgInfo, LastTag):
    line=line.strip().split(': ', 1)
    if len(line) == 1 and LastTag == 'Description':
        return ['Description', PkgInfo['Description']+'\n']
    elif len(line) == 1 and 'Package' in PkgInfo:
        return 'commit'
    elif len(line) != 2 and LastTag == 'Description':
        return ['Description', PkgInfo['Description']+'\n'+': '.join(line)]
    elif len(line) == 2 and line[0] in Tags:
        return [line[0], line[1]]
    elif len(line) == 2 and line[0].capitalize() in Tags:
        return [line[0].capitalize(), line[1]]
    elif len(line) == 2 and LastTag == 'Description':
        return ['Description', PkgInfo['Description']+'\n'+': '.join(line)]
    else: # just to be explicit
        return 'Discarded'

def Commit(Package, Table, IDV):
    if Package['Package'] in IDV and 'Version' in Package:
        try:
            if not Package['Version'].replace('-', '.') >= IDV[Package['Package']].replace('-'):
                return [IDV,'Newer Verion']
        except:
            return [IDV,'Already Exists'] # do not replace
    elif Package['Package'] in IDV:
        IDV[Package['Package']]=Package['Version']
    else:
        IDV[Package['Package']]=0
    for tag in Tags:
        if not tag in Package:
            Package[tag]='?' # fill in the blanks
    TagList=[Package['Package']]
    for tag in Tags:
        if tag != 'Package':
            TagList.append(Package[tag])
    query = 'INSERT INTO ' + Table + ' VALUES(%s)' % ','.join(['?'] * len(TagList))
    try:
        c.execute(query, TagList)
    except:
        print 'Error: ', sys.exc_info()[0], 'While Processing ', Package['Package']
        return [IDV,sys.exc_info()[0]]
    return [IDV, 'Sucessful']
    


for packagesfile in glob.glob( os.path.join(path, '*_Packages') ):
    repo=packagesfile.split('/')
    repo='http://'+repo[len(repo)-1].replace('._Packages','').replace('_Packages','').replace('_','/')
    with open(packagesfile) as reader:
        Package={'Repo':repo}
        LastTag=''
        for line in reader:
            Result=Parse(line, Package, LastTag)
            if Result == 'commit':
                TotalPackages += 1
                CommitResult=Commit(Package, AvailableDBTable, IDV)
                IDV=CommitResult[0]
                if not CommitResult[1] in ['Sucessful','Already Exists','Newer Verion']:
                    errors[Package['Package']]=CommitResult[1]
                Package={'Repo':repo}
                LastTag=''
            elif len(Result) == 2:
                Package[Result[0]]=Result[1]
                LastTag=Result[0]
db.commit()
print 'Finished Building Avalible Packages'
print 'Building Installed Packages...'

pipe1=subprocess.Popen(['dpkg', '-l'], stdout=subprocess.PIPE)
PIDs=subprocess.Popen(['awk', '{ print $2 }'], stdin=pipe1.stdout, stdout=subprocess.PIPE).communicate()[0].split()[3:]
for PID in PIDs:
    Package={}
    LastTag=''
    Output=subprocess.Popen(['dpkg', '-s', PID], stdout=subprocess.PIPE).communicate()[0]
    for line in Output.split('\n') :
        Result=Parse(line, Package, LastTag)
        if Result == 'commit':
            TotalPackages += 1
            Commit(Package, InstallDBTable, IDV)
            Package={}
            LastTag=''
        else:
            Package[Result[0]]=Result[1]
            LastTag=Result[0]

c.close()
db.commit()
db.close()
print '\nProcessed '+str(TotalPackages)+' Packages'
print "Execution time: ",   time.time() - start_time, "Seconds"
if len(errors) != 0:
    print "There were ",len(errors)," Errors during processing"
    if raw_input('Press Enter To View') == '':
        for PID in errors:
            print 'Encounter an ', errors[PID], ' when processing ', PID
