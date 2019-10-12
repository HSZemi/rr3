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
'''

PATCH_PLAYER_SETUP = '''
/* disable hunter workrate */
effect_amount SET_ATTRIBUTE VILLAGER_HUNTER_M ATTR_WORK_RATE 0
effect_amount SET_ATTRIBUTE VILLAGER_HUNTER_F ATTR_WORK_RATE 0
 
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
			if '<PLAYER_SETUP>' in line:
				scxPart = False
				rmsPart = True
				endOfStart = inStart
				inPlayerSetup = True
				endOfObjectsGeneration = inObjectsGeneration
			if '<LAND_GENERATION>' in line:
				scxPart = True
				rmsPart = False
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<ELEVATION_GENERATION>' in line:
				scxPart = True
				rmsPart = False
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<CLIFF_GENERATION>' in line:
				scxPart = True
				rmsPart = False
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<TERRAIN_GENERATION>' in line:
				scxPart = True
				rmsPart = False
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<CONNECTION_GENERATION>' in line:
				scxPart = False
				rmsPart = True
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
			if '<OBJECTS_GENERATION>' in line:
				scxPart = False
				rmsPart = True
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
				endOfObjectsGeneration = inObjectsGeneration
				inObjectsGeneration = True
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
