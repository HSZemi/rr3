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
countdowns = [
	486, # /* bear */
	#812, # /* jag */
	#1029, # /* lion */
	#1031, # /* croc */
	#1135, # /* komodo */
	#1137, # /* tiger */
	#860, # /* monkey */
	]

x = 0
for y in range(height):
	for unit in countdowns:
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=unit)
for y in range(1,height-1):
	scenario.units.new(x=x+1.5,y=y+0.5, owner=0, type=rock)
	
x = width-2
for y in range(height):
	for unit in countdowns:
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=unit)
for y in range(1,height-1):
	scenario.units.new(x=x-0.5,y=y+0.5, owner=0, type=rock)
	
y = 0
for x in range(1,width-1):
	for unit in countdowns:
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=unit)
for x in range(2,width-2):
	scenario.units.new(x=x+0.5,y=y+1.5, owner=0, type=rock)
	
y = height-2
for x in range(1,width-1):
	for unit in countdowns:
		scenario.units.new(x=x+0.5,y=y+0.5, owner=0, type=unit)
for x in range(2,width-2):
	scenario.units.new(x=x+0.5,y=y-0.5, owner=0, type=rock)

scenario.save(inputfile[:-4] + '_patched.scx')
