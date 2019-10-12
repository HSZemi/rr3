#! /usr/bin/env python3

import os
import math

minutes_until_first_wave = 90
minutes_until_second_wave = 120
radius_first_wave_tiles = 20
radius_second_wave_tiles = 40
interval_seconds_first_wave = 10
interval_seconds_second_wave = 10
attack_value_first_wave = 5
attack_value_second_wave = 5
timer_terrain = 'DESERT'

# calculating values...

storage_value_fake_deer = math.floor(minutes_until_first_wave * 60 / 4)
storage_value_hunting_wolf = math.floor(minutes_until_second_wave * 60 / 2)
storage_value_dire_wolf = math.floor(interval_seconds_first_wave / 2)
storage_value_rabid_wolf = math.floor(interval_seconds_second_wave / 2)
attack_dire_wolf = attack_value_first_wave
attack_rabid_wolf = attack_value_second_wave
radius_dire_wolf = radius_first_wave_tiles
radius_rabid_wolf = radius_second_wave_tiles

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
 
#const FAKE_DEER 333
#const HUNTING_WOLF 700

/* exploders */
#const DIRE_WOLF 89 
#const RABID_WOLF 202 
 
/* disable hunters */
#const VILLAGER_HUNTER_M 122
#const VILLAGER_HUNTER_F 216

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
/* disable hunter workrate */

effect_amount SET_ATTRIBUTE VILLAGER_HUNTER_M ATTR_WORK_RATE 0
effect_amount SET_ATTRIBUTE VILLAGER_HUNTER_F ATTR_WORK_RATE 0

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


/* timers (predators decay 1food/2secs and other hunt decays 1food/4secs) */
 
/* first wave */
	effect_amount SET_ATTRIBUTE FAKE_DEER ATTR_DEAD_ID 89
	effect_amount SET_ATTRIBUTE FAKE_DEER ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE FAKE_DEER ATTR_STORAGE_VALUE {storage_value_fake_deer}
	effect_amount SET_ATTRIBUTE FAKE_DEER ATTR_ATTACK 0
 
/* second wave */
	effect_amount SET_ATTRIBUTE HUNTING_WOLF ATTR_DEAD_ID 202
	effect_amount SET_ATTRIBUTE HUNTING_WOLF ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE HUNTING_WOLF ATTR_STORAGE_VALUE {storage_value_hunting_wolf}
	effect_amount SET_ATTRIBUTE HUNTING_WOLF ATTR_ATTACK 0
 
/* exploders */
/* splash radius for 8 players map */
 
	effect_amount SET_ATTRIBUTE DIRE_WOLF ATTR_HERO_STATUS 32 
	effect_amount SET_ATTRIBUTE DIRE_WOLF ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE DIRE_WOLF ATTR_STORAGE_VALUE {storage_value_dire_wolf}
	effect_amount SET_ATTRIBUTE DIRE_WOLF ATTR_DEAD_ID 89
	effect_amount SET_ATTRIBUTE DIRE_WOLF ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE DIRE_WOLF ATTR_ATTACK {attack_dire_wolf}
	effect_amount SET_ATTRIBUTE DIRE_WOLF ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE DIRE_WOLF ATTR_BLAST_RADIUS {radius_dire_wolf}

	effect_amount SET_ATTRIBUTE RABID_WOLF ATTR_HERO_STATUS 32 
	effect_amount SET_ATTRIBUTE RABID_WOLF ATTR_RESOURCE_CARRY 1
	effect_amount SET_ATTRIBUTE RABID_WOLF ATTR_STORAGE_VALUE {storage_value_rabid_wolf}
	effect_amount SET_ATTRIBUTE RABID_WOLF ATTR_DEAD_ID 202
	effect_amount SET_ATTRIBUTE RABID_WOLF ATTR_HITPOINTS 0
	effect_amount SET_ATTRIBUTE RABID_WOLF ATTR_ATTACK {attack_rabid_wolf}
	effect_amount SET_ATTRIBUTE RABID_WOLF ATTR_BLAST_LEVEL 1
	effect_amount SET_ATTRIBUTE RABID_WOLF ATTR_BLAST_RADIUS {radius_rabid_wolf}
 
'''.format(
	storage_value_fake_deer=storage_value_fake_deer, 
	storage_value_hunting_wolf=storage_value_hunting_wolf,
	storage_value_dire_wolf=storage_value_dire_wolf,
	storage_value_rabid_wolf=storage_value_rabid_wolf,
	attack_dire_wolf=attack_dire_wolf,
	attack_rabid_wolf=attack_rabid_wolf,
	radius_dire_wolf=radius_dire_wolf,
	radius_rabid_wolf=radius_rabid_wolf
	)

PATCH_OBJECTS_GENERATION = '''

/* timers */

create_object FAKE_DEER
{
    number_of_objects 999
    terrain_to_place_on %TIMER_TERRAIN%
    set_gaia_object_only
    temp_min_distance_group_placement 4
}

create_object HUNTING_WOLF
{
    number_of_objects 999
    terrain_to_place_on %TIMER_TERRAIN%
    set_gaia_object_only
    temp_min_distance_group_placement 4
}

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

'''.replace('%TIMER_TERRAIN%', timer_terrain)

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
