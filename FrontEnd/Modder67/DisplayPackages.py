#!/usr/bin/python

import os
import shelve

MasterPackages=shelve.open('../Cache/MasterPackages', writeback=False)

print "<html><body><table>"
for PID in MasterPackages:
    try:
        print "<tr><td>",MasterPackages[PID]['Name'],"</td></tr>"
    except KeyError:
        print '<tr><td>&ltNo Name&gt</tr></td>'
print "</table></body></table>"
