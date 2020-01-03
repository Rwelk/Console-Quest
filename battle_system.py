# battle_system.py
# These are the commands that are run when the player gets into a battle.

import os
import sys
import random
from time import sleep
from leveling_system import level_up



# This is the battle system that gets triggered whenever a battle happens.
# Make sure it's formatted as:
# 
# goblin(e_stat)
# battle(stat, e_stat)
# 
# when you call it.

def battle(stat, e_stat):

	os.system('clear')
	superatack = 0
	should_be_dead = False
	heavy_attack = False
	while True:

		# Check to see if the player has died.
		if stat['current_HP'] <= 0:
			print_red('\n You died!\n\n')
			sleep(1.5)
			print_red(' The villagers ran out of tributes for the orc.\n')
			print_red(" With no adventurers to protect them, the orc killed everybody.\n")
			sleep(3)
			print_red('\n Game over.\n')
			sleep(3)
			sys.exit(0)
			


		# Give a line for the player and monster stats.
		print_green('\n HP: '+str(stat['current_HP'])+'/'+str(stat['base_HP'])+"\t"+e_stat['e_type']+': '+str(e_stat['e_HP'])+'\n')


		# These loops are what allow the player to input their actions.
		# It accounts for both upper and lower case, and prevents the player from inputing an invalid action.
		# Player will always goes first.
		while True:

			# What the player can input. Note that they can only use [A] [P], or [R].
			print_yellow(' [A]ttack    [P]otion ('+str(stat['potions'])+')    [R]un\n')
			x = input(' >>> ').lower()
			print()

			# If the player tries to use something that isn't [A] [P], or [R]:
			if x!='a' and x!='p' and x!='r':
				invalid()

			# Everything that follows after is the meat of what happens when the player inputs their action.
			# This runs the attack command, to damage the opposing monster.
			elif x == 'a':

				# The battle system is like DnD. There a roll to see if the attack hits, then another for the actual damage dealt.
				attack = random.randint(10, 20) + (stat['ATT']/2)
				if attack >= e_stat['e_DEF']:
					damage = round(random.randint(1,5) + (stat['ATT']/2.5))
					e_stat['e_HP'] -= damage
					print_white(' '+stat['p_name']+" "+stat['ATT_type']+" the enemy for "), print_red(str(damage)+' DMG.\n')
					if e_stat['e_HP'] <0:
						e_stat['e_HP'] = 0
					sleep(.75)

					# Tell the player how much damage the attack did.
					print(' ', e_stat['e_type'], "'s HP dropped to ", e_stat['e_HP'], sep="")
					break

				# And in case the attack missed:
				else:
					print(' Your attack missed!')
					break


			# Run the potion command.
			# This is for letting the player restore their health mid-battle.
			elif x == 'p':

				# Just in case the player no longer has any potions:
				if stat['potions'] == 0:
					print(' No more potions!\n')
					sleep(.5)

				# Otherwise, restore their health. Tell the player so.
				else:
					stat['potions'] -= 1
					stat['current_HP'] += round(random.randint(4,10)* 4.2)

					if stat['current_HP'] > stat['base_HP']:
						stat['current_HP'] = stat['base_HP']

					print_white(' HP restored to '), print_green(str(stat['current_HP'])+'/'+str(stat['base_HP'])+'\n')
					break


			# Run the run command.
			# This is in case the player wants to try to escape from battle.
			elif x == 'r':

				# The escape formula is based on what level the player is versus what level the monster is.
				# The if the player has a higher level than the opponent, they have a higher chance of escape..
				# Conversly, if the monster has a higher level, it'll be harder for the player to run.
				j = stat['p_LV'] - e_stat['e_LV']
				if j == 0:
					j = 1

				if j*2 + random.randint(4,8) < 7:
					print(' Escape Failed!')
					break

				else:
					print(' Escape Success!\n')
					sleep(1)
					return stat

		sleep(.75)


		# Check to see if the enemy died last turn.
		# If so, give out rewards, and maybe level up.
		if e_stat['e_HP'] == 0:
			print('', e_stat['e_type'], 'died!\n')
			sleep(.5)

			if e_stat['e_type'] == 'Orc':
				stat['orc'] = 'Dead'
				print(" Congratulations!")
				sleep(1)
				print(" The orc is finally slain!")
				sleep(2)
				return stat

			else:	
				print(' You gained', e_stat['e_EXP'], 'XP and', e_stat['e_G'], 'gold.\n')
				stat['current_exp'] += e_stat['e_EXP']
				stat['p_G'] += e_stat['e_G']
				sleep(1)
				level_up(stat)
				return stat


		# Time for the monster's turn!
		else:
			while True:

				# The orc's various attacks.
				# It can do normal attacks for normal damage, or a super attack for a little under 1/3 of the player's HP.
				# If its HP is low, it might try to restore some itself.
				if e_stat['e_type'] == 'Orc':

					if heavy_attack == True:
						heavy_attack = False
						damage = round(stat['base_HP']/random.uniform(2, 2.5))
						f = stat['current_HP']
						stat['current_HP'] -= damage
						if stat['current_HP'] < 0:
							damage = f
							stat['current_HP'] = 0

							# A short line that trigger 1 time only.
							# If the player has taken the super attack and the damage is more than a third of their health, AND they would have died from it,...
							# the player is given a bit of amnesty with one HP remaining to drink a potion.
							if should_be_dead == False and damage>int(f/3):
								should_be_dead = True
								damage -= 1
								stat['current_HP'] = 1


						print_white(" The orc takes a big swing, dealing "), print_red(str(damage)+' DMG.\n')
						sleep(1.25)
						print(' ', stat['p_name'], "'s HP dropped to ", stat['current_HP'], ".", sep='')
						sleep(1.2)
						break


					orc_move = random.randint(1,4)

					# The part where the orc might heal itself.
					# In playtesting, this makes for a nailbiter of a battle.
					if orc_move == 3 and e_stat['e_HP'] < 28:
						heal = round(random.randint(4,7)* 4.2)
						e_stat['e_HP'] += heal
						print(" The orc grabs and eats a nearby hunk of meat, restoring", heal, "health.")
						sleep(1)
						break

					# The part where the orc readies a heavy attack.
					# It does significantly more damage than the normal ones.
					if orc_move == 4:
						heavy_attack = True
						print(" The orc gets ready for a heavy attack.")
						break

					else:
						normal_attack = True


				# Normal attacks from the other monster and the orc:
				if e_stat['e_type'] != 'Orc' or normal_attack == True:

					normal_attack = False
					attack = e_attack(e_stat)
					if attack >= stat['p_DEF']:
						damage = e_damage(e_stat)
						print_white(' '+e_stat['e_type']+' did '), print_red(str(damage)+' DMG.\n')
						stat['current_HP'] -= damage
						if stat['current_HP'] < 0:
							stat['current_HP'] = 0
						sleep(.75)
						print(' ', stat['p_name'], "'s HP dropped to ", stat['current_HP'], ".", sep='')
						sleep(.75)
						break

					# And in case the enemy misses as well:
					else:
						print(' ', e_stat['e_type'], "'s attack missed!", sep='')
						sleep(.75)
						break



# Here is where all the enemy types are stored, grouped into the separate phases they would appear in.
# The first chunk is defines the monsters' base stats.

# Enemy group 1:
def goblin(e_stat):
	e_stat['e_type'] = 'Goblin'
	e_stat['e_DEF'] = 10
	e_stat['e_LV'] = random.randint(1,7)
	e_stat['e_HP'] = round((e_stat['e_LV']+1) /2) + 4
	e_stat['e_EXP'] = random.randint(2,8)
	e_stat['e_G'] = random.randint(1,2)
	return e_stat

def rat(e_stat):
	e_stat['e_type'] = 'Rat'
	e_stat['e_DEF'] = 5
	e_stat['e_LV'] = random.randint(3,7)
	e_stat['e_HP'] = round((e_stat['e_LV'] +1) /2) + 8
	e_stat['e_EXP'] = random.randint(6,11)
	e_stat['e_G'] = random.randint(1,2)
	return e_stat

def slime(e_stat):
	e_stat['e_type'] = 'Slime'
	e_stat['e_DEF'] = 16
	e_stat['e_LV'] = random.randint(3,5)
	e_stat['e_HP'] = round((e_stat['e_LV'] +1) /2) + 9
	e_stat['e_EXP'] = random.randint(6,11)
	e_stat['e_G'] = random.randint(0,3)
	return e_stat

def reginald(e_stat):
	e_stat['e_type'] = 'Reginald'
	e_stat['e_DEF'] = 5
	e_stat['e_HP'] = 30
	e_stat['e_LV'] = 9
	e_stat['e_EXP'] = random.randint(10,15)
	e_stat['e_G'] = random.randint(7,10)
	return e_stat


# Enemy group 2:
def wolf(e_stat):
	e_stat['e_type'] = 'Wolf'
	e_stat['e_DEF'] = 20
	e_stat['e_LV'] = random.randint(8,12)
	e_stat['e_HP'] = ((e_stat['e_LV']-8)*4)+15
	e_stat['e_EXP'] = random.randint(12,18)
	e_stat['e_G'] = random.randint(1,4)
	return e_stat

def large_spider(e_stat):
	e_stat['e_type'] = 'Large Spider'
	e_stat['e_DEF'] = 20
	e_stat['e_LV'] = random.randint(8,12)
	e_stat['e_HP'] = ((e_stat['e_LV']-8)*4)+15
	e_stat['e_EXP'] = random.randint(12,18)
	e_stat['e_G'] = random.randint(1,4)
	return e_stat

def snake(e_stat):
	e_stat['e_type'] = 'Snake'
	e_stat['e_DEF'] = 22
	e_stat['e_LV'] = random.randint(8,12)
	e_stat['e_HP'] = ((e_stat['e_LV']-8)*4)+15
	e_stat['e_EXP'] = random.randint(12,18)
	e_stat['e_G'] = random.randint(1,4)
	return e_stat

# Enemy group 3:
def bear(e_stat):
	e_stat['e_type'] = 'Bear'
	e_stat['e_DEF'] = 20
	e_stat['e_LV'] = random.randint(13,17)
	e_stat['e_HP'] = ((e_stat['e_LV']-13)*2)+36
	e_stat['e_EXP'] = random.randint(26,36)
	e_stat['e_G'] = random.randint(1,4)
	return e_stat

def goblin_warrior(e_stat):
	e_stat['e_type'] = 'Goblin Warrior'
	e_stat['e_DEF'] = 22
	e_stat['e_LV'] = random.randint(13,17)
	e_stat['e_HP'] = ((e_stat['e_LV']-13)*2)+30
	e_stat['e_EXP'] = random.randint(26,36)
	e_stat['e_G'] = random.randint(4,7)
	return e_stat

def goblin_shaman(e_stat):
	e_stat['e_type'] = 'Goblin Shaman'
	e_stat['e_DEF'] = 23
	e_stat['e_LV'] = random.randint(13,17)
	e_stat['e_HP'] = ((e_stat['e_LV']-13)*2)+29
	e_stat['e_EXP'] = random.randint(26,36)
	e_stat['e_G'] = random.randint(5,9)
	return e_stat

def goblin_rider(e_stat):
	e_stat['e_type'] = 'Goblin Rider'
	e_stat['e_DEF'] = 24
	e_stat['e_LV'] = random.randint(13,17)
	e_stat['e_HP'] = ((e_stat['e_LV']-13)*2)+33
	e_stat['e_EXP'] = random.randint(26,36)
	e_stat['e_G'] = random.randint(2,6)
	return e_stat

# Final Boss Battle:
def orc(e_stat):
	e_stat['e_type'] = 'Orc'
	e_stat['e_DEF'] = 29
	e_stat['e_LV'] = 18
	e_stat['e_HP'] = 84
	return e_stat


# The next chunk defines what the monster's attack roll is.
# Because this should be different every round, I made it its own function.
def e_attack(e_stat):

	if e_stat['e_type'] == 'Goblin':
		return random.randint(7,40)

	elif e_stat['e_type'] == 'Rat':
		return random.randint(7,16)

	elif e_stat['e_type'] == 'Slime':
		return random.randint(7,15)

	elif e_stat['e_type'] == 'Reginald':
		return random.randint(10,20)


	elif e_stat['e_type'] == 'Wolf':
		return random.randint(10,30)

	elif e_stat['e_type'] == 'Large Spider':
		return random.randint(12,21)

	elif e_stat['e_type'] == 'Snake':
		return random.randint(14,23)


	elif e_stat['e_type'] == 'Bear':
		return random.randint(13,23)

	elif e_stat['e_type'] == 'Goblin Warrior':
		return random.randint(15,20)

	elif e_stat['e_type'] == 'Goblin Shaman':
		return random.randint(14,21)

	elif e_stat['e_type'] == 'Goblin Rider':
		return random.randint(15,22)


	elif e_stat['e_type'] == 'Orc':
		return random.randint(17,25)



# The final chunk is for how much damage the monster does.
# Like the attack roll, this should be different for ever success, so I made it ITs own function as well.
def e_damage(e_stat):
	if e_stat['e_type'] == 'Goblin':
		return random.randint(1,3)

	elif e_stat['e_type'] == 'Rat':
		return random.randint(2,4)

	elif e_stat['e_type'] == 'Slime':
		return random.randint(3,5)

	elif e_stat['e_type'] == 'Reginald':
		return random.randint(4,9)


	elif e_stat['e_type'] == 'Wolf':
		return random.randint(3,6)

	elif e_stat['e_type'] == 'Large Spider':
		return random.randint(4,6)

	elif e_stat['e_type'] == 'Snake':
		return random.randint(2,8)


	elif e_stat['e_type'] == 'Bear':
		return random.randint(8,11)

	elif e_stat['e_type'] == 'Goblin Warrior':
		return random.randint(7,8)

	elif e_stat['e_type'] == 'Goblin Shaman':
		return random.randint(7,8)

	elif e_stat['e_type'] == 'Goblin Rider':
		return random.randint(6,9)


	elif e_stat['e_type'] == 'Orc':
		return random.randint(7,9)



# Testing the battle system.
# Grog is a Lv. 2 Warrior fighting a Goblin.
# He has 10/30 HP and 3 potions to use. No gold though.
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

	e_stat = {  
		'e_type': "Raq Coon, Bane of Chickens",
		'e_DEF': 10000,
		'e_HP': 10000,
		'e_LV': 30,
		'e_EXP': random.randint(1,2),
		'e_G': random.randint(1,2)
		}
	for i in range(2):
		goblin_rider(e_stat)
		#goblin_shaman(e_stat)
		battle(stat, e_stat)

	# Now, after all that, does the program still give out the right values?
	print(stat['p_name'], "Lv:", stat['p_LV'])
	print("ATT:", stat['ATT'])
	print("DEF:", stat['p_DEF'])
	print("HP: ", stat['current_HP'], "/", stat['base_HP'], sep="")
	print("EXP: ", stat['current_exp'], "/", stat['next_level_exp'], sep="")

	sleep(3)