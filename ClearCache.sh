#!/bin/bash

cd Cache
rm *
cd Packages
for file in *; do
    rm $file
done
