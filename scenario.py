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
haystack = 857
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
		tile.type = deepwater

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

letters = {}
letters['R'] = [(0,y) for y in range(7)] + [(x,0) for x in range(1,4)] + [(x,2) for x in range(1,4)] + [(4,1)] + [(4,y) for y in range(3,7)]
letters['E'] = [(x,0) for x in range(5)] + [(x,6) for x in range(5)] + [(x,2) for x in range(1,3)] + [(0,y) for y in range(1,6)]
letters['G'] = [(0,y) for y in range(1,6)] + [(4,y) for y in range(2,6)] + [(x,0) for x in range(1,5)] + [(x,2) for x in range(2,4)] + [(x,6) for x in range(1,4)] 
letters['I'] = [(x,0) for x in range(3)] + [(x,6) for x in range(3)] + [(1,y) for y in range(1,6)]
letters['C'] = [(0,y) for y in range(1,6)] + [(x,0) for x in range(1,4)] + [(x,6) for x in range(1,4)] + [(4,1),(4,5)]
letters['D'] = [(x,0) for x in range(4)] + [(x,6) for x in range(4)] + [(0,y) for y in range(1,6)] + [(4,y) for y in range(1,6)]
letters['U'] = [(0,y) for y in range(6)] + [(4,y) for y in range(6)] + [(x,6) for x in range(1,4)]
letters['M'] = [(0,y) for y in range(7)] + [(4,y) for y in range(7)] + [(1,1),(2,2),(3,1)]
letters['B'] = [(0,y) for y in range(7)] + [(x,0) for x in range(1,4)] + [(x,2) for x in range(1,4)] + [(x,6) for x in range(1,4)] + [(4,y) for y in range(3,6)] + [(4,1)]
letters['L'] = [(0,y) for y in range(7)] + [(x,6) for x in range(1,5)]
letters['3'] = [(0,1),(0,5)] + [(x,0) for x in range(1,4)] + [(x,6) for x in range(1,4)] + [(x,3) for x in range(2,4)] + [(4,y) for y in range(1,3)] + [(4,y) for y in range(4,6)]
letters[' '] = []

def write_letter_at(letter,x,y,terrain):
	for pos in letters[letter]:
		scenario.tiles[pos[1]+y][pos[0]+x].type = terrain
		scenario.units.new(x=pos[0]+x+0.5,y=pos[1]+y+0.5, owner=0, type=haystack)

def get_width(letter):
	if letter == ' ':
		return 1
	if letter == 'I':
		return 3
	return 5

total_width = 0
for char in 'REGICIDE RUMBLE 3':
	total_width += get_width(char) + 1

x = width - total_width - 15
y = 1
for char in 'REGICIDE RUMBLE 3':
	write_letter_at(char,x,y,beach)
	x += get_width(char) + 1

scenario.save(inputfile[:-4] + '_patched.scx')
