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

print('Scenario size: {} x {}'.format(width, height))

beach = 2
shallow = 4
dirt = 6
dirt3 = 3
area = scenario.tiles.getArea(25,25,width-25,height-25)
for tile in area:
	if tile.type == shallow:
		tile.type = dirt
	if tile.type == beach:
		tile.type = dirt3

scenario.save(inputfile[:-4] + '_patchedterrains.scx')
