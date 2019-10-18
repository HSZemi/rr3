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

relic = 285
rock = 623
torch = 499
countdowns = [
	303,  #/* seagulls */ 
	333, #/* fakedeer */
	862  #/* stormydog */
	]

# relics
for i in range(50):
	scenario.units.new(x=0.5,y=0.5, owner=0, type=relic)

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
x = 10
for y in range(10, height-10, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# northeast
x = width-10
for y in range(11, height-10, 13):
	scenario.units.new(x=x-0.5,y=y+0.5, owner=0, type=torch)

# northwest
y = 10
for x in range(10, width-11, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# southeast
y = height-10
for x in range(11, width-11, 13):
	scenario.units.new(x=x+0.5,y=y-0.5, owner=0, type=torch)

# southwest
x = 20
for y in range(20, height-21, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# northeast
x = width-20
for y in range(20, height-21, 13):
	scenario.units.new(x=x-0.5,y=y+0.5, owner=0, type=torch)

# northwest
y = 20
for x in range(21, width-21, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# southeast
y = height-20
for x in range(21, width-21, 13):
	scenario.units.new(x=x+0.5,y=y-0.5, owner=0, type=torch)

# southwest
x = 30
for y in range(30, height-31, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# northeast
x = width-30
for y in range(30, height-31, 13):
	scenario.units.new(x=x-0.5,y=y+0.5, owner=0, type=torch)

# northwest
y = 30
for x in range(31, width-31, 13):
	scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=torch)

# southeast
y = height-30
for x in range(31, width-31, 13):
	scenario.units.new(x=x+0.5,y=y-0.5, owner=0, type=torch)

scenario.save(inputfile[:-4] + '_patched.scx')
