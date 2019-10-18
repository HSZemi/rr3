 #! /bin/bash
 
 # This script only works if the scenario files have been created manually already and are in their respective output folders
 
./prepare.py

for i in `ls output/**/RR3*.scx | grep -v 'patched'`; do ./scenario.py $i; done

rm output/**/ZR@*

for i in output/*; do zip -0 -j $i/ZR@T`basename $i`.rms $i/`basename $i`.rms $i/`basename $i`_patched.scx; done

rm -rf RR3_ALPHA

mkdir -p RR3_ALPHA

cp output/**/ZR@T* ./RR3_ALPHA/
