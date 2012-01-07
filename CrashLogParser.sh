#!/bin/bash

script=$(basename $0)_errors
log3=/var/iNinjas-Installer/ermesg

mydate=$(date +%b\ %d)

for log in $log{1,2,3}
do
if [ -e $log ] && [ -s $log ]
then
echo
echo BEGIN $log
grep -E "$mydate" $log | grep -E 'Device|fail'  2> $script
echo END $log
echo
fi
done
