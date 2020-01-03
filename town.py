# town.py
# The program here is for exploring the town, and, when ready, leaving for the forest.
# The player can visit the shop to buy a shiled and potions, the inn to heal up, and the Weaponer to make the upgraded weapon.
# They can also drink a potion in safety, save their game, and quit if they want to leave.

import os
import sys
import random
import base64
from time import sleep
from pathlib import Path
from colored_text import *
from random_encounters import exploring
from leveling_system import check_stats



# This is the function that triggers when the player goes to the shop to buy stuff.
def shop(stat):

	# The shopkeep will always speak in cyan.
	os.system('clear')
	print()

	# The price of potions. It changes if you meet and help the shopkeep's brother Daniel in the forest.
	pprice = 10		

	if stat['shopbro'] == 1 or stat['shopbro'] == 3:
		pprice = 7

		if stat['shopbro'] != 3:
			stat['shopbro'] = 3
			print_cyan(" Hey there! I heard you bumped into my brother in the forest.")
			sleep(2)
			print_cyan(" He might not be as awesome as me, but I still love the guy.")
			sleep(2)
			print_cyan(" I'll lower their price a little for you.\n")
			sleep(2.25)
			pprice = 15

	# However, if the player is unable to save Daniel, the Shopkeep is in a much more dour mood.
	# Additionally, he only has 4 potions left in stock, meaning the only way to obtain more is to find them from destroyed caravans while exploring.
	elif stat['shopbro'] == 2:
		stat['shopbro'] = 4
		print_cyan(" Hey there. It's been a rough day.")
		sleep(2)
		print_cyan(" I just found out that my brother Daniel was found dead.")
		sleep(2)
		print_cyan(" Since he was the one that made my potions, I don't have many left.")
		sleep(2.25)
		print_cyan(" I'll try to keep acting chipper though.")
		sleep(2)
		print_cyan(" Thanks for hearing me out.\n")
		sleep(2)


	# The shopkeep David introduces himself the first time the player comes to his shop.
	if stat['shopbro'] == -1:
		print_cyan(" Welcome to my shop!")
		sleep(1)
		print_cyan(" You must be that adventurer the town's been buzzing about.")
		sleep(1.5)
		print_cyan(" I'm the shopkeep, and town's best-looking dude. The name's David.")
		sleep(3)
		print_cyan(" What can I do for you?\n")
		sleep(.4)

	# If the player has come before, David just gives this short line:
	else: print_cyan(" Welcome back to my shop! Is there anything you want?\n")


	# These loops are what allow the player to input their actions.
	# It accounts for both upper and lower case, and prevents the player from inputing an invalid action.
	# There are a ton like this one in the document, so I will only explain how it works here.
	while True:

		# What the player can input. Note that they can only use [B] [S], or [L].
		print(" You currently have: " + "\033[32m" + str(stat['p_G'])+"G")
		print_yellow(" [B]uy    [S]ell    [L]eave")
		x = input(' >>> ').lower()
		print()
		
		# If the player tries to use something that isn't [B] [S], or [L]:
		if x!='b' and x!='s' and x!='l':
			invalid()

		# Everything that follows after is the meat of what happens when the player inputs their action.
		# This part here is for buying stuff.  
		elif x=='b':
			sleep(.5)
			while True:

				print("     You currently have: " + "\033[32m" + str(stat['p_G']) + "G")
				if stat['shopbro'] == 4:
					print_yellow("     [S]hield: 30G    [P]otions: " + str(pprice) + "G (" + str(stat['p_left']) + ")    [I]nformation    [R]eturn")					
				else:	
					print_yellow("     [S]hield: 30G    [P]otions: " + str(pprice) + "G    [I]nformation    [R]eturn")
				b = input('     >>> ').lower()
				print()

				if b!='s' and b!='p' and b!='i' and b!='r':
					print('     ', end="")
					invalid()
				# Getting a shield.
				elif b=='s':
					if stat['p_G'] < 30:
						print('     ', end=""), print_cyan("You'll need more money for that.\n")
						sleep(1)
					elif stat['shield'] == 1:
						print('     ', end=""), print_cyan("Looks like you already have a mighty fine shield there.")
						sleep(2)
						print('     ', end=""), print_cyan("Whoever gave you it must've been a really handsome dude.\n")
						sleep(2.5)
					else:
						stat['p_G'] -= 30
						stat['shield'] += 1
						stat['p_DEF'] += 3
						print('     ', end=""), print_cyan("Thanks for your purchase!\n")
						sleep(.7)
						print('     ', end="")
						print_white("DEF just rose by ")
						print_green("3!\n")
						sleep(1)

				# Getting potions.
				elif b=='p':

					if stat['shopbro'] == 2 and stat['p_left'] == 0:
						print('     ', end=""), print_cyan("Sorry, I'm all out of potions.\n")
						sleep(.7)

					elif stat['p_G'] < pprice:
						print('     ', end=""), print_cyan("You'll need more money for that.\n")
						sleep(.7)
					else:
						stat['p_G'] -= pprice		
						stat['potions'] += 1
						print('     ', end=""), print_cyan("Thanks for your purchase!\n")
						if stat['shopbro'] == 2: stat['p_left'] -= 1	
						sleep(.7)

				# Getting information, in case the player didn't read the manual.
				elif b=='i':
					print('         ', end=""), print_cyan("What do you wanna know?")
					while True:

						print_yellow('         [S]hield    [P]otions    [R]eturn')
						i = input('         >>> ').lower()
						print()
						if i!='S' and i!='s' and i!='P' and i!='p' and i!='R' and i!='r':
							invalid()
						elif i=='S' or i=='s':
							print('         ', end=""), print_cyan("The shield will increase your your DEF by 3.\n")
							sleep(1)
						elif i=='P' or i=='p':
							print('         ', end=""), print_cyan("Potions will restore your current HP by 17-42 points.\n")
							sleep(1)
						else:
							break
				else:
					break


		# The part for selling stuff.  
		# Note that the player cannot actually sell anything, since this is, you know, a shop.
		# As such, this area is completely for humor.
		elif x=='s':
			while True:

				fourth_wall = 0
				print("     You currently have: " + "\033[32m" + str(stat['p_G']) + "G")

				print_yellow("     [S]hield: 30G    [P]otions: 10G    [M]agic "+str(stat['magic_item_type'])+": ??G    [R]eturn")
				s = input('     >>> ').lower()
				print()
				if s!='s' and s!='p' and s!='m' and s!='r':
					print('     ', end="")
					invalid()
				elif s=='s':
					if stat['shield'] <1:
						print('     ', end=""), print_white("You don't have a shield to sell.\n")
						sleep(1)
					else:
						print('     ', end=""), print_white("That's a really nice shield you have there.")
						sleep(1.5) 
						print('     ', end=""), print_white("Are you sure you want to get rid of it?")
						while True:

							if fourth_wall > 0:
								break
							print_yellow('     [Y]es    [N]o')
							y = input('     >>> ').lower()
							print()
							if y!='y' and y!='n':
								invalid()
							elif y=='y':
								fourth_wall += 1
								print('     ', end=""), print_white("Are you really sure?")								
								while True:

									if fourth_wall > 1:
										break
									print_yellow('     [Y]es    [N]o')
									y = input('     >>> ').lower()
									print()
									if y!='y' and y!='n':
										print('     ', end="")
										invalid()
									elif y=='y':
										fourth_wall += 1
										print('     ', end=""), print_white("I mean, it's a really nice shield, and there's no real reason to.")
										while True:

											if fourth_wall > 2:
												break
											print_yellow('     [Y]es    [N]o')
											y = input('     >>> ').lower()
											print()
											if y!='y' and y!='n':
												print('     ', end="")
												invalid()
											elif y=='y':
												fourth_wall += 1
												print('     ', end=""), print_white("Your stats'll go down...")
												while True:

													if fourth_wall > 3:
														break
													print_yellow('     [J]ust do it.    [N]o')
													y = input('     >>> ').lower()
													print()
													if y!='j' and y!='y' and y!='n':
														invalid()
													elif y=='j' or y=='y':
														fourth_wall += 1
														print('     ', end=""), print_white("...and you don't really get much money back for it.")
														while True:

															if fourth_wall > 4:
																break
															print_yellow('     [L]et the shopkeep buy my shield!    [N]o')
															y = input('     >>> ').lower()
															print()
															if y!='L' and y!='l' and y!='Y' and y!='y'and y!='N' and y!='n':
																invalid()
															elif y=='L' or y=='l' or y=='Y' or y=='y':
																fourth_wall += 1
																print('     ', end=""), print_white("I'm not sure I want to, with that tone of voice.")
																while True:

																	print_yellow("     [I]'m sorry. Can I just please sell my shield?    [N]o")
																	y = input('     >>> ').lower()
																	print()																
																	if y!='I' and y!='i' and y!='Y' and y!='y'and y!='N' and y!='n':
																		invalid()
																	elif y=='I' or y=='i' or y=='Y' or y=='y':
																		print('     ', end=""), print_white("Alright, since you're so sure.")
																		sleep(2)
																		print('     ', end=""), print_white("Just don't come crying to me if you die because you're DEF was")
																		print('     ', end=""), print_white("so low you got hit a bunch of times.\n")
																		sleep(3)
																		print('     ', end=""), print_cyan("You want to return this shield?")
																		sleep(1)
																		print('     ', end=""), print_cyan("Sorry, but I don't take refunds.\n")
																		sleep(1)
																		break
															else:
																break
													else:
														break
											else:
												break
									else:
										break
							else:
								break

				elif s=='p':
					if stat['potions'] <1:
						print_white("     You don't have any potions to sell.")
						sleep(1)
					else:
						print('     ', end=""), print_cyan("Look man, don't take this personally, but I'm trying to run a")
						print('     ', end=""), print_cyan("business here.")
						sleep(1.5)
						print('     ', end=""), print_cyan("Why the heck would I buy some strange liquid from a rando")
						print('     ', end=""), print_cyan(" adventurer I only met like, a few days ago?")
						sleep(1.5)
						if stat['potions'] >1:
							print('     ', end=""), print_cyan("Also, I'm pretty sure at least some of this is my own stock.\n")
							sleep(2)
				elif s=='m':
					if stat['magic_item'] <1:
						print('     ', end=""), print_white("You don't have any magic items to sell.")
						sleep(1)
					else:
						print('     ', end=""), print_cyan("I have no use for magic items, but I think the "+str(stat['magic_weaponer'])+"might")
						print('     ', end=""), print_cyan("need it for a certain project she's been working on.")
						sleep(4)
				else:
					break


		# Let the player leave the shop.
		elif x=='l':
			print_cyan(' See you around!\n')
			sleep(1)

			# David will tell the player about his missing brother the first time they come to the shop.
			if stat['shopbro'] == -1:
				stat['shopbro'] = 0
				print_cyan(" By the way, my brother's been missing for several days.")
				sleep(1)
				print_cyan(" He's actually the one who makes my potions.")
				sleep(1)
				print_cyan(" If you see him, tell him his more handsome brother's worried.\n")
				sleep(1)

			return stat

		os.system('clear')
		print()



# This is the code that plays when the player goes to the inn the sleep and reheal.
# It also begins the fairy sidequest, as the player is unable to meet them before meeting the Innkeep.
def inn(stat):

	os.system('clear')
	print("\n You currently have: " + "\033[32m" + str(stat['p_G'])+"G\n")

	# This part plays when the player comes to the inn for the first time.
	if stat['inn'] == 0:
		stat['inn'] = 1
		print_green(" Welcome to my inn.\n")
		sleep(1.25)
		print_green(" You're the adventurer here to beat the orc, right?\n")
		sleep(2)
		print_green(" Would you like to stay the night?\n")
		sleep(2)
		print_green(" It'll cost 7G.\n")
		sleep(1)
		print("\n Staying the night will recover all your lost health.")

	# This part plays every other time the player visits the inn.
	else:
		print_green(" Welcome back! Here for the night again?\n")

	# The actual bit where the player decides whether or not they want to stay.
	while True:
		print_yellow(' [Y]es: 7G    [N]o\n')
		x = input(' >>> ').lower()
		print()
		if x!='y' and x!='n':
			invalid()
		elif x=='y':
			# If their health is already at max, they are reminded, just in case they don't want to waste 7G.
			if stat['current_HP'] == stat['base_HP']:
				print(" Are you sure? Your HP is already at max.")
				while True:
					print_yellow(' [Y]es: 7G    [N]o\n')
					x = input(' >>> ').lower()
					print()
					if x!='y' and x!='n':
						invalid()
					elif x=='y':
						break						

					else:
						print_green(" See you later!\n\n")
						return

			# Check to see if the player has enough money.
			if stat['p_G'] < 7:

				# If the player is short on cash, but has stayed at the inn seven other times, the fee is waved.
				# All remaining money is taken, but they can still heal up.
				if stat['inn'] > 8:
					print_green(" You've been such a good customer, I'll waive the fee for tonight.\n")
					sleep(4)
					print_green(" Just give me what you can, and I'll put the rest on your tab.\n\n")
					sleep(3)
					j = True

				else:
					print_green(" You don't have enough money to stay right now.\n\n")
					sleep(3)
					j = False

			else:
				j = True

			break

		elif x=='n':
			j = False
			break

	# If the player has deicided to stay, or the Innkeep has allowed them to.
	if j == True:
		stat['inn'] += 1
		stat['p_G'] -= 7
		if stat['p_G'] < 0:
			stat['p_G'] = 0

		# This line for the final part of the Magic Weapon Quest.
		# The player has to go do something else to give the Weaponer some time to make the weapon.
		if stat['quest'] == 2: stat['quest'] = 3

		# Just a small touch, the player is directed to 1 of 4 rooms to sleep in.
		x = random.randint(1,4)
		if x == 1: print_green(" Your room is right down the hall, second door on the left.\n\n")
		elif x == 2: print_green(" Your room is up the stairs, third door on the right.\n\n")
		elif x == 3: print_green(" Your room is right down the hall, first door on the right.\n\n")
		elif x == 4: print_green(" Your room is up the stairs, first door on the left.\n\n")
		sleep(2)

		# The HP is restored to max, and a short sleep cycle is played.
		stat['current_HP'] = stat['base_HP']
		print(" Z",end=""), sleep(.6), print("z",end=""), sleep(.6), print("z",end=""), sleep(.6),  print(".",end=""), sleep(.6), print(".",end=""), sleep(.6), print(".\n",end=""), sleep(1)
		print(" Health fully restored!\n")
		sleep(1.75)

	# If the player has not talked to the Innkeep about the fairies yet, this section will begin that sidequest for the thrid part of the game.
	if stat['fairies'] == 0 and stat['inn'] > 1:
		stat['fairies'] = 1
		print(" As you're about to leave, the Innkeep waves you down.\n")
		sleep(2.5)
		print_green(" You haven't heard of the mischievous fairies, have you?\n")
		sleep(2)
		print_green(" My father used to tell me tales of how deep in the forest, he and his\n")
		print_green(" adventuring party discovered a cave with fairies in it.\n")
		sleep(5)
		print_green(" When offered a brightly colored juice, some of them became stronger\n")
		print_green(" than ever before.\n")
		sleep(5)
		print_green(" However, a couple others oddly turned weaker.\n")
		sleep(1.75)
		print_green(" The other villagers always mocked him for that story, all the way to\n")
		print_green(" his grave.\n")
		sleep(4)
		print_green(" It's always been a dream of mine to prove him right.\n")
		sleep(2.75)
		print_green(" If you ever do, please tell me about them.\n")
		sleep(3)
		print_green(" Alright, see you later!\n\n")
		sleep(2.5)
		return stat
		
	print_green(" See you around!\n\n")
	sleep(2)
	return stat



# This is the code that plays when the player goes to their Weaponer to make a better weapon.
def magic_maker(stat):

	os.system('clear')
	print()

	# This plays the first time the player meets the Weaponer.
	# This was the original sidequest, which is why its dictionary definition is generically 'quest' while all the others have special names.
	# So like, this was the only one I was going to implement, but I ended up wanting to make the other characters more important too, so... yeah.
	# Created side quests for them too, and now here we are.
	# It was WAY too much, but ehh.
	if stat['quest'] == 0:

		stat['quest'] = 1
		print_magenta(" Hello there! Welcome to my")
		if stat['magic_weaponer'] == 'Blacksmith': print_magenta(" forge.\n")
		else: print_magenta(" workshop.\n")
		sleep(2.75)
		print_magenta(" You must be that adventurer who's here to kill that orc.\n")
		sleep(3.25)
		print_magenta(" "+stat['p_name']+", was it?\n")
		sleep(2)
		print_magenta(" I'm currently working on a project you might be able to help with.\n")
		sleep(3.5)
		print_magenta(" In the forest you might come across some Magic ")
		if stat['magic_weaponer'] == 'Blacksmith': print_magenta("Ore.\n")
		else: print_magenta("Wood.\n")
		sleep(3.5)

		# In case the player has already found magic items in the forest before meeting the Weaponer:
		if stat['magic_item'] >0:

			print("\n Wait! Didn't you pick some up some "+stat['magic_item_type']+" earlier?")
			while True:
				print_yellow(" [L]ike this?\n")
				x = input(' >>> ').lower()
				print()
				if x!='l':
					invalid()
				else:
					print_magenta(" Yes, that's it!\n")
					sleep(1)
					break

		# The Sword and Daggers only need 3 Ore, while the Staff needs 5 Wood.
		if stat['magic_weaponer'] == 'Blacksmith': print_magenta(" If you can gather up 3 of 'em and 25G, I'll be able to hammer out")
		else: print_magenta(" If you can gather up 5 of 'em and 25G, I'll be able to carve up")
		print_magenta("a\n special weapon.\n")
		stat['quest'] = 1

		while True:
			print_yellow(" [Y]ou can count on me!\n")
			x = input(' >>> ').lower()
			print()
			if x!='y':
				invalid()
			else:
				print_magenta(" Great! I'll see you later!\n\n")
				sleep(1.5)
				break


	# When the player returns to the Weaponer, this dialogue plays.
	elif stat['quest'] == 1:

		print_magenta(" How's the search coming?\n")
		while True:
			print_yellow(" [G]ot everything right here.    [S]till searching.\n")
			x = input(' >>> ').lower()
			print()
			if x!='g' and x!='s':
				invalid()
			# If they claim to have everything, the Weaponer checks.
			elif x=='g':

				# In case the player is missing some ore and/or gold, she will tell them what they need.
				if (stat['magic_weaponer'] == 'Blacksmith' and stat['magic_item'] <3) or (stat['magic_weaponer'] == 'Wizard' and stat['magic_item'] <5) or stat['p_G'] <25:
					print_magenta(" Hold on, you're still missing ")
					also = False
					if stat['magic_weaponer'] == 'Blacksmith' and stat['magic_item'] <3:
						print_magenta(str(3-stat['magic_item'])+" Ore")
						also = True
					else:
						print_magenta(str(5-stat['magic_item'])+" Wood")
						also = True

					if also == True and stat['p_G'] <25: print_magenta(" and ")

					if stat['p_G'] <25: print_magenta(str(25-stat['p_G'])+"G")

					print_magenta(".\n")
					sleep(3.5)

					print_magenta(" Come back when you've gotten everything. I'm itching to get started!\n\n")
					sleep(3)
					return

				# But if everything is in order, the Weaponer will get underway immediately.
				else:
					if stat['magic_weaponer'] == 'Blacksmith': stat['magic_item'] -= 3
					else: stat['magic_item'] -= 5
					stat['p_G'] -= 20
					print_magenta(" Sweet! I'll get right to it.\n")
					sleep(3)
					print_magenta(" Come back a little later, and it should be done!\n\n")
					stat['quest'] = 2
					sleep(3.5)
					return stat

			# The player tells the Weaponer they don't have everything, thereby leaving the area and returning to town proper.
			# The Weaponer will remind the player what they need.
			elif x=='s':
				print_magenta(" Well then I'll leave you to it.\n")
				sleep(1.75)
				if stat['magic_weaponer'] == 'Blacksmith': print_magenta(" Remember, you need 3 Ore and 50 G.\n\n")
				else: print_magenta(" Remember, you need 5 Wood and 50 G.\n\n")
				sleep(2)
				break

	# The Weaponer needs time to make the weapon, and if not given it, this dialogue will play.
	# The player will have to either explore the forest once, or sleep off the night to get past this point.
	elif stat['quest'] == 2:
		print_magenta(" Hey there! Progress on your weapon is going good.\n")
		sleep(3)
		print_magenta(" Give me a little more time, and I should be finished.\n")
		sleep(3)
		print_magenta(" I can't wait for you to see it!\n\n")
		sleep(2.75)


	# Once the player has given the Weaponer time, they'll award the new weapon.
	elif stat['quest'] == 3:
		print_magenta(" Welcome back! I'm finally done!\n")
		sleep(2)
		print_magenta(" I present to you: the "+stat['magic_weapon']+"!\n")
		sleep(3)
		stat['ATT'] += 7
		stat['mwc'] = False
		stat['quest'] = 4
		print_white("\n ATT rose by "), print_green("7!\n\n")
		sleep(2.5)
		if stat['magic_weapon'] == 'Vorpal Daggers': print_magenta(" Hope you like them!\n\n")
		else: print_magenta(" Hope you like it!\n\n")
		sleep(3)


	# If the player ever returns afterwards, this short dialogue plays.
	elif stat['quest'] == 4:
		print_magenta(" So, how's my magnum opus treating ya?\n")
		sleep(3)
		print_magenta(" I don't have anything else I can help you with, so get\n")
		print_magenta(" out there and beat that orc!\n\n")
		sleep(4.5)



# This is the code called from play_game.py.
# It first does a quick check to see if the player has defeated the orc.
# It then lets the player explore the town and use any of the above functions.
# They can also explore the forest, drink potions, check their stats, and save and quit the game.
def town(stat, e_stat):
	while True:
		if stat['orc'] == "Dead":
			return stat

		print(' Where would you like to go?')
		saved = False
		weaponer = stat['magic_weaponer']
		while True:
			print_yellow(' [S]hop    [I]nn    ['+weaponer[0]+']'+weaponer[1:]+'    [E]xplore Forest    [M]ore')
			x = input(' >>> ').lower()
			print()
			if x!='s' and x!='i' and x!=weaponer[0].lower() and x!='e' and x!='m':
				invalid()
			elif x=='s':
				saved = False
				shop(stat)
				break

			elif x=='i':
				saved = False
				inn(stat)
				break

			elif x==weaponer[0].lower():
				saved = False
				magic_maker(stat)
				break

			elif x=='e':
				saved = False
				exploring(stat, e_stat)
				break

			

			elif x=='m':
				while True:

					# These [M]ore statements cycle back and forth into each other.
					print_yellow(' [C]heck Stats    [P]otion ('+str(stat['potions'])+')    [S]ave Game    [Q]uit    [M]ore')
					y = input(" >>> ").lower()
					print()
					if y!='c' and y!='p' and y!='s' and y!='q' and y!='m':
						invalid()
					elif y=='c':
						check_stats(stat)

					elif y=='p':
						
						# Just in case the player no longer has any potions:
						if stat['potions'] == 0:
							print(' Out of potions.\n')
							sleep(.5)

						# Otherwise, restore their health. Tell the player so.
						else:
							saved = False
							stat['potions'] -= 1
							stat['current_HP'] += round(random.randint(4,10)* 4.2)

							if stat['current_HP'] > stat['base_HP']:
								stat['current_HP'] = stat['base_HP']

							print_white(' HP restored to '), print_green(str(stat['current_HP'])+'/'+str(stat['base_HP'])+'\n')

					# I want to specially point out the save function here.
					# It allows the player to save their game to a file called "save_state.txt".
					# The way it does this is by making an empty string called line_to_save and a list called stats_to_save.
					# Those stats are then added to the empty string followed by a comma nd space.
					# That string is then converted into bytes to be coded into base64, so the player can't easily just goin in and change their stats.
					# Those base64 bytes are again converted back into a string so it can be printed to the txt file.
					elif y=='s':
						saved = True
						save_state = Path('save_state.txt')
						line_to_save = ''
						stats_to_save = [stat['p_name'], stat['p_class'], stat['p_LV'], stat['ATT'], stat['ATT_type'],
							stat['p_DEF'], stat['current_HP'], stat['base_HP'], stat['current_exp'], stat['next_level_exp'],
							stat['potions'], stat['p_G'], stat['quest'], stat['magic_weapon'], stat['mwc'],
							stat['magic_weaponer'], stat['magic_item_type'], stat['magic_item'], stat['shield'], stat['rathat'],
							stat['shopbro'], stat['p_left'], stat['fairies'], stat['inn'], stat['orc'], stat['user']]

						for i in stats_to_save:
							line_to_save = line_to_save + str(i) + ", "

						save_state.write_text(str(base64.standard_b64encode(line_to_save[:-2].encode('utf-8')))[2:-1])

						print(" Game saved.\n")


					# This line lets the player quit the game.
					# Littered throughtout the above function has been the variable 'saved'.
					# If the player has done something that would have changed their state, like going to the shops, or drinking potions, their state would be different from when they saved.
					# As such, the player is reminded to if they haven't saved.
					# However, if they have, and have only check their stats or some such, they're state is no different from the last save, to the reminder won't play.
					# I also give a quick prompt just in case they still want to continue, so they can back out of quiting.
					elif y=='q':
						print_white(" Are you sure?")
						if saved == False: print_white(" (Since you haven't saved, data might be lost.)")
						while True:
							print_yellow(' [Y]es    [N]o')
							x = input(' >>> ').lower()
							print()
							if x!='y' and x!='n':
								invalid()
							elif x=='y':
								sys.exit(0)

							elif x=='n':
								break

					elif y=='m':
						break



# The function for testing the town, to make sure everything works.
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
		'potions': 0,
		'p_G': 100,
		'quest': 0,
		'magic_weapon': 'Sun Sword',
		'mwc': False,
		'magic_weaponer': 'Blacksmith',
		'magic_item_type': 'Ore',
		'magic_item': 3,
		'shield': True,
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
		'e_EXP': 0,
		'e_G': 0,
		}

	shop(stat)
	#town(stat, e_stat)