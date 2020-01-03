# leveling_system.py
# This is what will be run when the player has recieved enough experience to gain a level.

import random
from time import sleep
from colored_text import *


def level_up(stat):

	# Using a while loop here, in case the player somehow gains enough experience to level up multiple times in a single battle.
	while stat['current_exp'] >= stat['next_level_exp']:
	#for i in range(14):
		# Raises the player's level by 1, while subracting how much is required for that level up.
		stat['p_LV'] += 1
		stat['current_exp'] -= stat['next_level_exp']


		# Tell the player they've just leveled up. The silly print formatting is colorama's fault.
		print_white(" "), print_white(stat['p_name']), print_green(" levels up!\n")
		sleep(.9)
		

		# This is the formula for how much more experience the player will need to obtain the next level.
		# I fiddled with values in graph making software to come up with this one.
		stat['next_level_exp'] = round((6 * (stat['p_LV']**.769))-7.182)
		
		# And the player's stats have to increase for it to mean anything.
		stat['ATT'] += random.randint(1, 2)
		HP = random.randint(1, 2)
		stat['current_HP'] += HP
		stat['base_HP']  += HP
		x = random.randint(1, 8)
		if x == 7:
			stat['p_DEF'] += 1
			x = -1

		print_white(" HP"), print_green(" rose to:  "+str(stat['base_HP']))
		print()
		print_white(" ATT"), print_green(" rose to: "+str(stat['ATT']))
		print()
		if x == -1:
			print_white(" DEF"), print_green(" rose to: "+str(stat['p_DEF']))
			print()
		else:
			print_white(" DEF remains:  "+str(stat['p_DEF']))
			print()


		# And for good measure, tell the player how much more they'll need for their next level.
		print_white(" Next Lv. at "), print_yellow(stat['next_level_exp']), print_white(" EXP.\n\n")
		sleep(.9)

	print_white(" Currently at "), print_green("Lv. "+str(stat['p_LV'])+'\n\n')
	sleep(.9)
	return stat

def check_stats(stat):

	if len(stat['p_name']) <8: print_green(" "+stat['p_name']+"	  Lv. "+str(stat['p_LV']))
	else: print_green(" "+stat['p_name']+"  Lv. "+str(stat['p_LV']))
	print()
	print_white(" EXP:	  "), print_green(str(stat['current_exp'])+"/"+str(stat['next_level_exp']))
	print()
	print_white(" HP:	  "), print_yellow(str(stat['current_HP'])+"/"+str(stat['base_HP']))
	print()
	print_white(" ATT:	  "), print_yellow(str(stat['ATT']))
	print()
	print_white(" DEF:	  "), print_yellow(str(stat['p_DEF']))
	print("\n")

	print_green(" Inventory:\n")
	print_white(" Potion:  "), print_yellow(str(stat['potions']))
	print()
	print_white(" Gold:	  "), print_yellow(str(stat['p_G']))
	print()
	if stat['magic_item'] >0:
		print_white(" "+str(stat['magic_item_type'])+":	  "), print_yellow(str(stat['magic_item']))
		print()
	if stat['mwc'] == True:
		print("",stat['magic_weapon'])
	if stat['shield'] == True:
		print_white(" Shield\n")
	sleep(2)
	print()



# This is for testing the level system on its own.
# Grog's stats are that of a Lv. 3 Warrior.
if __name__ == '__main__':

	stat = {
		'p_name': 'Grog',
		'p_class': 'Warrior',
		'p_LV': 3,
		'ATT': 5,
		'ATT_type': 'slashes at',
		'p_DEF': 9,
		'current_HP': 17,
		'base_HP': 17,
		'current_exp': 0,
		'next_level_exp': 4,
		'potions': 2,
		'p_G': 2,
		'quest': 0,
		'magic_weapon': 'Sun Sword',
		'mwc': False,
		'magic_weaponer': 'Blacksmith',
		'magic_item_type': 'Ore',
		'magic_item': 3,
		'shield': False,
		'rathat': False,
		'shopbro': -1,
		'p_left': 4,
		'fairies': 1,
		'inn': 0,
		'orc': False
		}
	
	stat['current_exp'] = 12
	print()
	level_up(stat)
	#check_stats(stat)
