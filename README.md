# rr3
Maps for T90Official's Regicide Rumble 3

How to use this:

1. Prepare the rms files
2. Configure the storms at the top of `prepare.py`
2. Run `./prepare.py`
3. Create a fancy scenario from each of the rms files in `output/<map_name>/scx_<map_name>.rms` files
4. Run `./scenario.py <scx_file>` on each of those scx files, creating a `<scx_file>_patched.scx` file in the same folder. 
   (You need https://github.com/dderevjanik/agescx for it to work, for example by installing it in a virtualenv)
5. Pack the `output/<map_name>/<map_name>.rms` (not the scx one!) and the patched `.scx` file from above into a `ZR@<map_name>.rms` file
6. Yay!
