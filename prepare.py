#! /usr/bin/env python3

import os
import math

PATCH_HEADER = '''/* ** REGICIDE RUMBLE 3 ** */
/* an event by T90Official */
/* Map: {mapname} ({variant}) */
/* FEATURES */
/* - Battle Royale */
/* - Custom Regicide with Treason instead of Spies */
/* - Relic victory disabled */
/* - Kings drop 1 relic on death */
/* - Bombard Towers disabled */
/* - Masonry, Architecture and Hoardings disabled */
/* - Byzantine HP bonus disabled */
/* - Defensive structures (Castles, Towers, Walls and Gates) -30% HP */

'''

PATCH_START = '''
/* timers */

#const COUNTDOWN01 486 /* bear */
#const COUNTDOWN02 812 /* jag */
#const COUNTDOWN03 1029 /* lion */
#const COUNTDOWN04 1031 /* croc */
#const COUNTDOWN05 1135 /* komodo */
#const COUNTDOWN06 1137 /* tiger */
#const COUNTDOWN07 860 /* monkey */

/* exploders */
#const STORM01 89 /* direwolf */
#const STORM02 202 /* rabidwolf */
#const STORM03 707 /* ornlu */
#const STORM04 810 /* ironboar */
#const STORM05 544 /* flyingdog */
#const STORM06 594 /* sheep */
#const STORM07 705 /* cow */

/* disable gathering from stormy animals */
#const VILLAGER_BASE_M 83
#const VILLAGER_BASE_F 293

/* relic spawning */
#const PRIEST_WITH_RELIC 1025

/* Disable Bombard Towers */
#const BBT_TECH 64
#const FREE_BBT_TECH 444

/* Disable Masonry, Architecture, Hoardings */
#const MASONRY_TECH 50
#const ARCHITECTURE_TECH 51
#const HOARDINGS_TECH 379

/* Disable Byzantine building HP bonus */
#const BYZ_10_HP_TECH 283
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

'''

PATCH_PLAYER_SETUP = '''
/* disable gathering from stormy animals */

effect_amount SET_ATTRIBUTE VILLAGER_BASE_M ATTR_WORK_RATE 0
effect_amount SET_ATTRIBUTE VILLAGER_BASE_F ATTR_WORK_RATE 0

/* king drops relic */

effect_amount SET_ATTRIBUTE KING ATTR_DEAD_ID 1025
effect_amount SET_ATTRIBUTE PRIEST_WITH_RELIC ATTR_HITPOINTS 0

/* disable bombard towers */

effect_amount DISABLE_TECH BBT_TECH ATTR_DISABLE 64
effect_amount DISABLE_TECH FREE_BBT_TECH ATTR_DISABLE 444

/* Disable Masonry, Architecture, Hoardings */

effect_amount DISABLE_TECH MASONRY_TECH ATTR_DISABLE 50
effect_amount DISABLE_TECH ARCHITECTURE_TECH ATTR_DISABLE 51
effect_amount DISABLE_TECH HOARDINGS_TECH ATTR_DISABLE 379

/* Disable Byzantine building HP bonus */

effect_amount DISABLE_TECH BYZ_10_HP_TECH ATTR_DISABLE 283
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

effect_amount MOD_RESOURCE AMOUNT_STARTING_WOOD ATTR_ADD 300
effect_amount MOD_RESOURCE AMOUNT_STARTING_FOOD ATTR_ADD 300
effect_amount MOD_RESOURCE AMOUNT_STARTING_GOLD ATTR_ADD -100
effect_amount MOD_RESOURCE AMOUNT_STARTING_STONE ATTR_ADD -50
guard_state KING AMOUNT_GOLD 0 1

/* remove spies, add treason */
effect_amount GAIA_SET_PLAYER_DATA DATA_MODE_FLAGS ATTR_SET 3


/* 30 min */
	effect_amount SET_ATTRIBUTE COUNTDOWN01 ATTR_DEAD_ID 89
	effect_amount SET_ATTRIBUTE COUNTDOWN01 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN01 ATTR_STORAGE_VALUE 900
/* 35 min */
	effect_amount SET_ATTRIBUTE COUNTDOWN02 ATTR_DEAD_ID 202
	effect_amount SET_ATTRIBUTE COUNTDOWN02 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN02 ATTR_STORAGE_VALUE 1050
/* 40 min */
	effect_amount SET_ATTRIBUTE COUNTDOWN03 ATTR_DEAD_ID 707
	effect_amount SET_ATTRIBUTE COUNTDOWN03 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN03 ATTR_STORAGE_VALUE 1200
/* 45 min */
	effect_amount SET_ATTRIBUTE COUNTDOWN04 ATTR_DEAD_ID 810
	effect_amount SET_ATTRIBUTE COUNTDOWN04 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN04 ATTR_STORAGE_VALUE 1350
/* 50 min */
	effect_amount SET_ATTRIBUTE COUNTDOWN05 ATTR_DEAD_ID 544
	effect_amount SET_ATTRIBUTE COUNTDOWN05 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN05 ATTR_STORAGE_VALUE 1500
/* 55 min */
	effect_amount SET_ATTRIBUTE COUNTDOWN06 ATTR_DEAD_ID 594
	effect_amount SET_ATTRIBUTE COUNTDOWN06 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN06 ATTR_STORAGE_VALUE 1650
/* 60 min */
	effect_amount SET_ATTRIBUTE COUNTDOWN07 ATTR_DEAD_ID 705
	effect_amount SET_ATTRIBUTE COUNTDOWN07 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE COUNTDOWN07 ATTR_STORAGE_VALUE 1800

/* STORM-DAMAGE */

/* 30min dire wolf; 1dmg */
	effect_amount SET_ATTRIBUTE STORM01 ATTR_HERO_STATUS 32
	effect_amount SET_ATTRIBUTE STORM01 ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE STORM01 ATTR_STORAGE_VALUE 5
	effect_amount SET_ATTRIBUTE STORM01 ATTR_DEAD_ID 89
	effect_amount SET_ATTRIBUTE STORM01 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE STORM01 ATTR_ATTACK 1
	effect_amount SET_ATTRIBUTE STORM01 ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE STORM01 ATTR_BLAST_RADIUS 12

/* 35min rabid wolf; 1dmg */
	effect_amount SET_ATTRIBUTE STORM02 ATTR_HERO_STATUS 32
	effect_amount SET_ATTRIBUTE STORM02 ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE STORM02 ATTR_STORAGE_VALUE 5
	effect_amount SET_ATTRIBUTE STORM02 ATTR_DEAD_ID 202
	effect_amount SET_ATTRIBUTE STORM02 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE STORM02 ATTR_ATTACK 1
	effect_amount SET_ATTRIBUTE STORM02 ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE STORM02 ATTR_BLAST_RADIUS 24

/* 40min ornlu the wolf; 2dmg */
	effect_amount SET_ATTRIBUTE STORM03 ATTR_HERO_STATUS 32
	effect_amount SET_ATTRIBUTE STORM03 ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE STORM03 ATTR_STORAGE_VALUE 5
	effect_amount SET_ATTRIBUTE STORM03 ATTR_DEAD_ID 707
	effect_amount SET_ATTRIBUTE STORM03 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE STORM03 ATTR_ATTACK 2
	effect_amount SET_ATTRIBUTE STORM03 ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE STORM03 ATTR_BLAST_RADIUS 34

/* 45min iron boar; 2dmg */
	effect_amount SET_ATTRIBUTE STORM04 ATTR_HERO_STATUS 32
	effect_amount SET_ATTRIBUTE STORM04 ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE STORM04 ATTR_STORAGE_VALUE 5
	effect_amount SET_ATTRIBUTE STORM04 ATTR_DEAD_ID 810
	effect_amount SET_ATTRIBUTE STORM04 ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE STORM04 ATTR_ATTACK 2
	effect_amount SET_ATTRIBUTE STORM04 ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE STORM04 ATTR_BLAST_RADIUS 39

/* 50min flying dog - saboteur; 20-3-20 dmg (building, mellee, walls) */

	effect_amount SET_ATTRIBUTE STORM05 ATTR_STORAGE_VALUE 3
	effect_amount SET_ATTRIBUTE STORM05 ATTR_DEAD_ID 706
	effect_amount SET_ATTRIBUTE STORM05 ATTR_HITPOINTS 0

/* 55min llama - sheriff; 30-3 dmg (building, mellee) */

	effect_amount SET_ATTRIBUTE STORM06 ATTR_STORAGE_VALUE 3
	effect_amount SET_ATTRIBUTE STORM06 ATTR_DEAD_ID 164
	effect_amount SET_ATTRIBUTE STORM06 ATTR_HITPOINTS 0

/* 60min cow - siegfried; 40-4 dmg (building, mellee) */

	effect_amount SET_ATTRIBUTE STORM07 ATTR_STORAGE_VALUE 3
	effect_amount SET_ATTRIBUTE STORM07 ATTR_DEAD_ID 170
	effect_amount SET_ATTRIBUTE STORM07 ATTR_HITPOINTS 0

'''

PATCH_OBJECTS_GENERATION = '''

/* Regicide ingredients */

create_object VILLAGER
{
    number_of_groups 7
    number_of_objects 1
    set_place_for_every_player
    temp_min_distance_group_placement 2
    min_distance_group_placement 2
    min_distance_to_players 3
    max_distance_to_players 7
}

create_object HOUSE
{
    number_of_groups 2
    set_place_for_every_player
    max_distance_to_players 12
    min_distance_group_placement 2
    temp_min_distance_group_placement 12
}

create_object KING
{
    set_place_for_every_player
    max_distance_to_players 5
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
			line = line.replace(' RELIC', ' PRIEST_WITH_RELIC')
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
				if scxPart:
					print(PATCH_OBJECTS_GENERATION, file=outscx)
				if rmsPart:
					print(PATCH_OBJECTS_GENERATION, file=outrms)
				inObjectsGeneration = False
				endOfObjectsGeneration = False


			if '<PLAYER_SETUP>' in line:
				scxPart = False
				rmsPart = True
				inPlayerSetup = True
			if '<LAND_GENERATION>' in line:
				scxPart = True
				rmsPart = False
			if '<ELEVATION_GENERATION>' in line:
				scxPart = False
				rmsPart = True
			if '<CLIFF_GENERATION>' in line:
				scxPart = False
				rmsPart = True
			if '<TERRAIN_GENERATION>' in line:
				scxPart = False
				rmsPart = True
			if '<CONNECTION_GENERATION>' in line:
				scxPart = False
				rmsPart = True
			if '<OBJECTS_GENERATION>' in line:
				scxPart = False
				rmsPart = True
				inObjectsGeneration = True

			if scxPart:
				print(line, file=outscx, end='')
			if rmsPart:
				print(line, file=outrms, end='')

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
			if scxPart:
				print(PATCH_OBJECTS_GENERATION, file=outscx)
			if rmsPart:
				print(PATCH_OBJECTS_GENERATION, file=outrms)
			inObjectsGeneration = False
			endOfObjectsGeneration = False
