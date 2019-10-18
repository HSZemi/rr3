#! /usr/bin/env python3

import os
import math


waves = [
	{'minutes': 90, 'radius': 20}, # 90
	{'minutes': 120, 'radius': 40}, # 120
	{'minutes': 150, 'radius': 60}, # 150
]

NO_HOUSES = ['RR3_Settlers']

food_per_minute = 15 # .25 food per second
for wave in waves:
	wave['food'] = food_per_minute * wave['minutes']


PATCH_HEADER = '''/* ** REGICIDE RUMBLE 3 ** */
/* an event by T90Official */
/* Map: {mapname} ({variant}) */
/* FEATURES */
/* - Battle Royale */
/* - Custom Regicide with Treason instead of Spies */
/* - Relic victory disabled */
/* - Wonders disabled */
/* - Kings drop 1 relic on death */
/* - Bombard Towers disabled */
/* - Masonry, Architecture and Hoardings disabled */
/* - Byzantine HP bonus disabled */
/* - Defensive structures (Castles, Towers, Walls and Gates) -30% HP */

'''

PATCH_START = '''
/* timers */
#const COUNTDOWN01 303 /* seagulls */  /* 0.25 food per sec */
#const COUNTDOWN02 333 /* fakedeer */  /* 0.25 food per sec */
#const COUNTDOWN03 862 /* stormydog */ /* 0.25 food per sec */

/* exploders */
#const STORM01 486    /* bear */  /* 0.5 food per sec */
#const STORM02 1028   /* stork */  /* 0.25 food per sec */
#const STORM03 1056   /* falcon */ /* 0.25 food per sec */

#const DUPLICATOR 1193
#const DUPLICATED 1194

#const EXPLODER1 640
#const EXPLODER2 173
#const EXPLODER3 198

/* relic spawning */
#const PRIEST_WITH_RELIC 1025

/* Disable wonders */
#const WONDER_TECH 144

/* Disable Bombard Towers */
#const BBT_TECH 64
#const FREE_BBT_TECH 444

/* Disable Masonry, Architecture, Hoardings */
#const MASONRY_TECH 50
#const ARCHITECTURE_TECH 51
#const HOARDINGS_TECH 379

/* Nerf Byzantine building HP bonus */
#const BYZ_20_HP_TECH 417
#const BYZ_30_HP_TECH 418
#const BYZ_40_HP_TECH 419

/* Nerf defensive structures -30% HP */
#const GATE_A 64
#const GATE_B 88
#const GATE_C 659
#const GATE_D 667

#const FORTIFIED_GATE_A 63
#const FORTIFIED_GATE_B 85
#const FORTIFIED_GATE_C 660
#const FORTIFIED_GATE_D 668

#const PALISADE_GATE_A 790
#const PALISADE_GATE_B 794
#const PALISADE_GATE_C 798
#const PALISADE_GATE_D 802
#const PALISADE_GATE_E 789
#const PALISADE_GATE_F 793
#const PALISADE_GATE_G 797
#const PALISADE_GATE_H 801

#const DATA_MODE_FLAGS 1
#const GAIA_SET_PLAYER_DATA -10

'''

PATCH_PLAYER_SETUP = '''
/* king drops relic */

effect_amount SET_ATTRIBUTE KING ATTR_DEAD_ID 1025
effect_amount SET_ATTRIBUTE PRIEST_WITH_RELIC ATTR_HITPOINTS 0

/* Disable wonders */

effect_amount DISABLE_TECH WONDER_TECH ATTR_DISABLE 144

/* disable bombard towers */

effect_amount DISABLE_TECH BBT_TECH ATTR_DISABLE 64
effect_amount DISABLE_TECH FREE_BBT_TECH ATTR_DISABLE 444

/* Disable Masonry, Architecture, Hoardings */

effect_amount DISABLE_TECH MASONRY_TECH ATTR_DISABLE 50
effect_amount DISABLE_TECH ARCHITECTURE_TECH ATTR_DISABLE 51
effect_amount DISABLE_TECH HOARDINGS_TECH ATTR_DISABLE 379

/* Nerf Byzantine building HP bonus */

effect_amount DISABLE_TECH BYZ_20_HP_TECH ATTR_DISABLE 417
effect_amount DISABLE_TECH BYZ_30_HP_TECH ATTR_DISABLE 418
effect_amount DISABLE_TECH BYZ_40_HP_TECH ATTR_DISABLE 419

/* Nerf defensive structures -30% HP */

effect_percent MUL_ATTRIBUTE CASTLE ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE WATCH_TOWER ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE GUARD_TOWER ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE KEEP ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_WALL ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE WALL ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE FORTIFIED_WALL ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE GATE_A 64 ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE GATE_B 88 ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE GATE_C 659 ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE GATE_D 667 ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE FORTIFIED_GATE_A ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE FORTIFIED_GATE_B ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE FORTIFIED_GATE_C ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE FORTIFIED_GATE_D ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_GATE_A ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_GATE_B ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_GATE_C ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_GATE_D ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_GATE_E ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_GATE_F ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_GATE_G ATTR_HITPOINTS 70
effect_percent MUL_ATTRIBUTE PALISADE_GATE_H ATTR_HITPOINTS 70

/* regicide stuff */

if REGICIDE
else
	effect_amount MOD_RESOURCE AMOUNT_STARTING_WOOD ATTR_ADD 300
	effect_amount MOD_RESOURCE AMOUNT_STARTING_FOOD ATTR_ADD 300
	effect_amount MOD_RESOURCE AMOUNT_STARTING_GOLD ATTR_ADD -100
	effect_amount MOD_RESOURCE AMOUNT_STARTING_STONE ATTR_ADD -50
	guard_state KING AMOUNT_GOLD 0 1
endif

/* remove spies, add treason */
effect_amount GAIA_SET_PLAYER_DATA DATA_MODE_FLAGS ATTR_SET 3


/* {waves[0][minutes]} min */
	effect_amount SET_ATTRIBUTE COUNTDOWN01 ATTR_DEAD_ID 486
	effect_amount SET_ATTRIBUTE COUNTDOWN01 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN01 ATTR_STORAGE_VALUE {waves[0][food]}
	effect_amount SET_ATTRIBUTE COUNTDOWN01 ATTR_STORAGE_VALUE -32

/* {waves[1][minutes]} min */
	effect_amount SET_ATTRIBUTE COUNTDOWN02 ATTR_DEAD_ID 1028
	effect_amount SET_ATTRIBUTE COUNTDOWN02 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN02 ATTR_STORAGE_VALUE {waves[1][food]}
	effect_amount SET_ATTRIBUTE COUNTDOWN02 ATTR_STORAGE_VALUE -32

/* {waves[2][minutes]} min */
	effect_amount SET_ATTRIBUTE COUNTDOWN03 ATTR_DEAD_ID 1056
	effect_amount SET_ATTRIBUTE COUNTDOWN03 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN03 ATTR_STORAGE_VALUE {waves[2][food]}
	effect_amount SET_ATTRIBUTE COUNTDOWN03 ATTR_STORAGE_VALUE -32

/* short timers */
	effect_amount SET_ATTRIBUTE STORM01 ATTR_STORAGE_VALUE 10
	effect_amount SET_ATTRIBUTE STORM01 ATTR_DEAD_ID 1193
	effect_amount SET_ATTRIBUTE STORM01 ATTR_HITPOINTS 0

	effect_amount SET_ATTRIBUTE STORM02 ATTR_STORAGE_VALUE 10
	effect_amount SET_ATTRIBUTE STORM02 ATTR_DEAD_ID 173
	effect_amount SET_ATTRIBUTE STORM02 ATTR_HITPOINTS 0

	effect_amount SET_ATTRIBUTE STORM03 ATTR_STORAGE_VALUE 10
	effect_amount SET_ATTRIBUTE STORM03 ATTR_DEAD_ID 198
	effect_amount SET_ATTRIBUTE STORM03 ATTR_HITPOINTS 0

/* duplicators */
	effect_amount SET_ATTRIBUTE DUPLICATOR ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE DUPLICATOR ATTR_CREATION_TIME 0
	effect_amount SET_ATTRIBUTE DUPLICATOR ATTR_DEAD_ID 486

	effect_amount SET_ATTRIBUTE DUPLICATED ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE DUPLICATED ATTR_CREATION_TIME 0
	effect_amount SET_ATTRIBUTE DUPLICATED ATTR_DEAD_ID 640


/* STORM-DAMAGE */

/* {waves[0][minutes]} min 1 dmg */
	effect_amount SET_ATTRIBUTE EXPLODER1 ATTR_HERO_STATUS 32
	effect_amount SET_ATTRIBUTE EXPLODER1 ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE EXPLODER1 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE EXPLODER1 ATTR_ATTACK 5
	effect_amount SET_ATTRIBUTE EXPLODER1 ATTR_ATTACK 257
	effect_amount SET_ATTRIBUTE EXPLODER1 ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE EXPLODER1 ATTR_BLAST_RADIUS {waves[0][radius]}

/* {waves[1][minutes]} min 1 dmg */
	effect_amount SET_ATTRIBUTE EXPLODER2 ATTR_HERO_STATUS 32
	effect_amount SET_ATTRIBUTE EXPLODER2 ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE EXPLODER2 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE EXPLODER2 ATTR_ATTACK 5
	effect_amount SET_ATTRIBUTE EXPLODER2 ATTR_ATTACK 257
	effect_amount SET_ATTRIBUTE EXPLODER2 ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE EXPLODER2 ATTR_BLAST_RADIUS {waves[1][radius]}
	effect_amount SET_ATTRIBUTE EXPLODER2 ATTR_DEAD_ID 1028

/* {waves[2][minutes]} min 1 dmg */
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_HERO_STATUS 32
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_ATTACK 5
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_ATTACK 257
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_ATTACK 512
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_BLAST_RADIUS {waves[2][radius]}
	effect_amount SET_ATTRIBUTE EXPLODER3 ATTR_DEAD_ID 1056

'''.format(waves=waves)

PATCH_OBJECTS_GENERATION = '''

/* Regicide ingredients */

create_object VILLAGER
{
    number_of_groups 7
    number_of_objects 1
    set_place_for_every_player
    min_distance_to_players 3
    max_distance_to_players 7
}

create_object KING
{
    set_place_for_every_player
    max_distance_to_players 5
}
'''
PATCH_OBJECTS_GENERATION_HOUSES = '''
create_object HOUSE
{
    number_of_groups 2
    set_place_for_every_player
    max_distance_to_players 12
    min_distance_group_placement 2
}

'''

rmsfiles = []
for filename in os.listdir('.'):
	if filename[-4:] == '.rms':
		rmsfiles.append(filename)

for rmsfile in rmsfiles:
	print(rmsfile)
	scxPart = True
	rmsPart = True
	inStart = True
	endOfStart = False
	inPlayerSetup = False
	endOfPlayerSetup = False
	inObjectsGeneration = False
	endOfObjectsGeneration = False
	seenCreateVillagerStatement = False
	seenClosingBracketOfCreateVillagerStatement = False
	shouldPatchObjectGeneration = True
	create_tc_capture = []
	tc_capture_active = False
	foldername = rmsfile[:-4].replace('ZR@','')
	print('Creating folder ' + foldername)
	os.makedirs(os.path.join('output', foldername), exist_ok=True)
	if rmsfile == 'ZR@RR3_King_of_Kings.rms':
		print('Please extract ZR@RR3_King_of_Kings manually since it already is a ZR map')
		continue
	with open(rmsfile, 'r') as inrms, open(os.path.join('output', foldername, rmsfile), 'w') as outrms, open(os.path.join('output', foldername, 'scx_'+rmsfile), 'w') as outscx:
		print(PATCH_HEADER.format(mapname=foldername, variant='scenario generation part for ZR map'), file=outscx)
		print(PATCH_HEADER.format(mapname=foldername, variant='rms part for ZR map'), file=outrms)
		for line in inrms:
			line = line.replace('create_object RELIC', 'create_object PRIEST_WITH_RELIC')
			if '<PLAYER_SETUP>' in line:
				endOfStart = inStart
				endOfObjectsGeneration = inObjectsGeneration
			if '<LAND_GENERATION>' in line:
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<ELEVATION_GENERATION>' in line:
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<CLIFF_GENERATION>' in line:
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<TERRAIN_GENERATION>' in line:
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<CONNECTION_GENERATION>' in line:
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<OBJECTS_GENERATION>' in line:
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup

			if endOfStart:
				print(PATCH_START, file=outscx)
				print(PATCH_START, file=outrms)
				inStart = False
				endOfStart = False
			if endOfPlayerSetup:
				if scxPart:
					print(PATCH_PLAYER_SETUP, file=outscx)
				if rmsPart:
					print(PATCH_PLAYER_SETUP, file=outrms)
				inPlayerSetup = False
				endOfPlayerSetup = False
			if endOfObjectsGeneration:
				inObjectsGeneration = False
				endOfObjectsGeneration = False
			if inObjectsGeneration:
				if 'create_object TOWN_CENTER' in line:
					tc_capture_active = True
				if tc_capture_active:
					create_tc_capture.append(line)
					if '}' in line:
						tc_capture_active = False

			if '<PLAYER_SETUP>' in line:
				scxPart = False
				rmsPart = True
				inPlayerSetup = True
			if '<LAND_GENERATION>' in line:
				scxPart = True
				rmsPart = False
			if '<ELEVATION_GENERATION>' in line:
				scxPart = True
				rmsPart = False
			if '<CLIFF_GENERATION>' in line:
				scxPart = True
				rmsPart = False
			if '<TERRAIN_GENERATION>' in line:
				scxPart = True
				rmsPart = False
			if '<CONNECTION_GENERATION>' in line:
				scxPart = True
				rmsPart = False
			if '<OBJECTS_GENERATION>' in line:
				scxPart = False
				rmsPart = True
				inObjectsGeneration = True

			if scxPart:
				print(line, file=outscx, end='')
			if rmsPart:
				print(line, file=outrms, end='')
			
			if inObjectsGeneration and shouldPatchObjectGeneration:
				if seenCreateVillagerStatement and '}' in line:
					seenClosingBracketOfCreateVillagerStatement = True
				if 'create_object VILLAGER' in line:
					seenCreateVillagerStatement = True
				if seenClosingBracketOfCreateVillagerStatement:
					if scxPart:
						print(PATCH_OBJECTS_GENERATION, file=outscx, end='')
						if foldername not in NO_HOUSES:
							print(PATCH_OBJECTS_GENERATION_HOUSES, file=outscx, end='')
					if rmsPart:
						print(PATCH_OBJECTS_GENERATION, file=outrms, end='')
						if foldername not in NO_HOUSES:
							print(PATCH_OBJECTS_GENERATION_HOUSES, file=outrms, end='')
					shouldPatchObjectGeneration = False

		endOfStart = inStart
		endOfPlayerSetup = inPlayerSetup
		endOfObjectsGeneration = inObjectsGeneration

		if endOfStart:
			print(PATCH_START, file=outscx)
			print(PATCH_START, file=outrms)
			inStart = False
			endOfStart = False
		if endOfPlayerSetup:
			if scxPart:
				print(PATCH_PLAYER_SETUP, file=outscx)
			if rmsPart:
				print(PATCH_PLAYER_SETUP, file=outrms)
			inPlayerSetup = False
			endOfPlayerSetup = False
		if endOfObjectsGeneration:
			inObjectsGeneration = False
			endOfObjectsGeneration = False
		
		print('<OBJECTS_GENERATION>\n', file=outscx)
		print(''.join(create_tc_capture), file=outscx)
