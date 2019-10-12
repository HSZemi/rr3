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
			if '<LAND_GENERATION>' in line:
				scxPart = True
				rmsPart = False
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
			if '<ELEVATION_GENERATION>' in line:
				scxPart = True
				rmsPart = False
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
			if '<CLIFF_GENERATION>' in line:
				scxPart = True
				rmsPart = False
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
			if '<TERRAIN_GENERATION>' in line:
				scxPart = True
				rmsPart = False
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
			if '<CONNECTION_GENERATION>' in line:
				scxPart = False
				rmsPart = True
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
			if '<OBJECTS_GENERATION>' in line:
				scxPart = False
				rmsPart = True
				endOfStart = inStart
				endOfPlayerSetup = inPlayerSetup
			if endOfStart:
				print(PATCH_START, file=outscx)
				print(PATCH_START, file=outrms)
				inStart = False
				endOfStart = False
			if endOfPlayerSetup:
				print(PATCH_PLAYER_SETUP, file=outscx)
				print(PATCH_PLAYER_SETUP, file=outrms)
				inPlayerSetup = False
				endOfPlayerSetup = False
			if scxPart:
				print(line, file=outscx, end='')
			if rmsPart:
				print(line, file=outrms, end='')
