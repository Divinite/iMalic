#!/usr/bin/python

import time
import shelve

StartTime=time.time()

Sections=shelve.open('Cache/SectionsList', writeback=True)

# Going to make set the html we need for the sections page, otherwise it can't be formatted correctly
head = '<!DOCTYPE html><head><title>iMalic</title><script src="../jquery/jquery.min.js"></script><script src="../jquery/jquery.mobile.conf.js"></script><script src="../javascript/base.js"></script><script src="../jquery/jquery.mobile.js"></script><link rel="stylesheet" href="../jquery/jquery.mobile.css" /><meta content="minimum-scale=1.0, width=device-width, maximum-scale=0.6667, user-scalable=no" name="viewport" /><meta name="apple-mobileweb-app-capable" content="yes" /><link rel="apple-touch-icon" href="image.png" /></head>'
body1 = '<body><div data-role="page" id="sections" data-dom-cache="true"><header data-role="header"><h1>Sections</h1></header><div data-role="content"><h1>Sections</h1>'
body2 = '</div></div><div id="contain-dock"></div></body></html>'

if not 'Unknown' in Sections:
    # bad practive not importing at the script's start
    # but this really helps with perfomance
    import sqlite3
    DBTable = 'AvailablePacakges'
    DBFolder = 'Cache'
    DBPath = DBFolder+'/Master.sqlite'
    db = sqlite3.connect(DBPath)
    c = db.cursor()
    Tags=['Package', 'Name', 'Section', 'Description', 'Publisher', 'Status',
      'Contact', 'Source', 'Tag', 'Depends', 'Homepage', 'Icon', 'Depiction',
      'Filename', 'MD5sum', 'Size', 'Maintainer', 'Sponsor', 'SHA256',
      'Version', 'Architecture', 'Author', 'Priority', 'SHA1', 'Conflicts',
      'Replaces',  'Price', 'Essential', 'Bundle', 'Website', 'Suggests',
      'Provides', 'Languages', 'Support', 'More', 'Recommends', 'Enhances',
      'Dev', 'Breaks', 'Repo' ]

    Sections['Unknown']=0
    c.execute('SELECT Section From '+DBTable)
    for result in c:
        if  str(result[0]) in Sections:
            Sections[str(result[0])] += 1
        elif str(result[0]) == '?':
            Sections['Unknown'] += 1
        else: # result no in list
            Sections[str(result[0])] = 1
    c.close()
    db.close()


# alphabetize
# for some reason they don't like shelves/dictionaries
SortList=[]
SortNums=[]
for section in  Sections:
    SortList.append(section)
SortList.sort()
for section in SortList:
    SortNums.append(Sections[section]) # save numbers

LastChar=''
print head + body1
for section in SortList:
    if section[0].upper() != LastChar:
        LastChar=section[0].upper()
        print '<ul data-role="listview" data-inset="true" data-theme="g">' + '<li data-role="list-divider">' + section[0].upper() + '</li>'
    print '<li><a href="../../scripts/Section.py?Section='+section+'">' + section + ' (' + str(SortNums[SortList.index(section)]) + ')</a></li>'
print '</ul>' + "<br><br><h7>Page Generated in",time.time()-StartTime,"Seconds</h7>" + body2