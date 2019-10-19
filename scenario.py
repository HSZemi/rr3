#! /usr/bin/env python3

from agescx import *
import sys

def place_rectangle(distance, spacing, object_to_place):
	# southwest
	x = distance
	for y in range(distance, height-distance, spacing):
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=object_to_place)

	# northeast
	x = width-distance-1
	for y in range(distance, height-distance, spacing):
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=object_to_place)

	# northwest
	y = distance
	for x in range(distance+spacing, width-distance-1, spacing):
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=object_to_place)

	# southeast
	y = height-distance-1
	for x in range(distance+spacing, width-distance-1, spacing):
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=object_to_place)
	

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

print('Scenario size: {} x {}'.format(width, height))

scenario.map.resize(width+20, height+20)

# move old map into the new center
for w in range(width-1, -1, -1):
	for h in range(height-1, -1, -1):
		oldPosition = scenario.map.tiles._tiles[w][h]
		scenario.map.tiles._tiles[w+10][h+10] = Tile(row=w+10, col=h+10, type=oldPosition.type, elevation=oldPosition.elevation)

for unit in scenario.units:
	unit.move(10,10)

width = scenario.tiles.width
height = scenario.tiles.height


relic = 285
rock = 623
torch = 499
deepwater = 22
beach = 37
countdowns = [
	303,  #/* seagulls */ 
	333, #/* fakedeer */
	862  #/* stormydog */
	]

# water around the outside

areas = [
	scenario.tiles.getArea(0,0,width-1,9),
	scenario.tiles.getArea(0,height-10,width-1,height-1),
	scenario.tiles.getArea(0,0,9,height-1),
	scenario.tiles.getArea(width-10,0,width-1,height-1)
	]
for area in areas:
	for tile in area:
		if (tile.x + tile.y) % 2 == 0:
			tile.type = deepwater
		else:
			tile.type = beach

# relics
for i in range(50):
	scenario.units.new(x=0.5,y=0.5, owner=0, type=relic)

#spawners
for unit in countdowns:
	place_rectangle(0, 5, unit)

# rocks
place_rectangle(9, 1, rock)

# torches
for distance in [10, 20, 30]:
	d = distance + 10
	place_rectangle(d, 13, torch)

scenario.save(inputfile[:-4] + '_patched.scx')
