#! /usr/bin/env python3

from agescx import *
import sys

if(len(sys.argv) < 2):
	print('Usage: ./{} <scx file>'.format(sys.argv[0]))
	sys.exit()

inputfile = sys.argv[1]

if inputfile[-4:] != '.scx':
	print('Input file is not a .scx file!')
	sys.exit()

scenario = Scenario(inputfile)

width = scenario.tiles.width
height = scenario.tiles.height

rock = 623
torch = 499
countdowns = [
	1137, #/* tiger */
	860,  #/* monkey */
	1135  #/* komodo */
	]

# spawners and rocks

# southwest
x = 0
for y in range(0, height, 5):
	for unit in countdowns:
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=unit)
for y in range(1,height-1):
	scenario.units.new(x=x+1.5,y=y+0.5, owner=0, type=rock)

# northeast
x = width-1
for y in range(0, height, 5):
	for unit in countdowns:
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=unit)
for y in range(1,height-1):
	scenario.units.new(x=x-0.5,y=y+0.5, owner=0, type=rock)

# northwest
y = 0
for x in range(5, width-1, 5):
	for unit in countdowns:
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=unit)
for x in range(2,width-2):
	scenario.units.new(x=x+0.5,y=y+1.5, owner=0, type=rock)

# southeast
y = height-1
for x in range(5, width-1, 5):
	for unit in countdowns:
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=unit)
for x in range(2,width-2):
	scenario.units.new(x=x+0.5,y=y-0.5, owner=0, type=rock)


# torches

# southwest
x = 20
for y in range(20, height-20, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# northeast
x = width-20
for y in range(21, height-20, 13):
	scenario.units.new(x=x-0.5,y=y+0.5, owner=0, type=torch)

# northwest
y = 20
for x in range(20, width-21, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# southeast
y = height-20
for x in range(21, width-21, 13):
	scenario.units.new(x=x+0.5,y=y-0.5, owner=0, type=torch)

# southwest
x = 40
for y in range(40, height-41, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# northeast
x = width-40
for y in range(40, height-41, 13):
	scenario.units.new(x=x-0.5,y=y+0.5, owner=0, type=torch)

# northwest
y = 40
for x in range(41, width-41, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# southeast
y = height-40
for x in range(41, width-41, 13):
	scenario.units.new(x=x+0.5,y=y-0.5, owner=0, type=torch)

# southwest
x = 60
for y in range(60, height-61, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# northeast
x = width-60
for y in range(60, height-61, 13):
	scenario.units.new(x=x-0.5,y=y+0.5, owner=0, type=torch)

# northwest
y = 60
for x in range(61, width-61, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# southeast
y = height-60
for x in range(61, width-61, 13):
	scenario.units.new(x=x+0.5,y=y-0.5, owner=0, type=torch)

scenario.save(inputfile[:-4] + '_patched.scx')
