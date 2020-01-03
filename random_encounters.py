# random_encounters.py
# This is where the different random encounters the player can find in the forest are stored.
# It also contains exploring(stat)

import os
import sys
import random
from time import sleep
from colored_text import *
from battle_system import *
from leveling_system import check_stats


# When the player has already completed a one-time encounter, these messages will play.
def complete(stat):
	x = random.randint(1,4)

	if x == 1:
		print_white("\n A wind blows gently through the trees.")
		sleep(1.5)

	elif x == 2:
		print_white("\n Birds chirp quietly in the background.")
		sleep(1.5)

	elif x == 3: 
		print_white("\n The sunlight warms your body and soul.")
		if stat['current_HP'] < stat['base_HP']:
			stat['current_HP'] += 1
		sleep(1.5)

	elif x == 4:
		print_white("\n The forest is so peaceful, you take a nap.")
		if stat['current_HP'] < stat['base_HP']:
			stat['current_HP'] += 1
		sleep(3)

	return stat





# The "Caravan" event nets the player some extra gold and potions.
# It is the only source of potions if they fail the shopbro() event.
def caravan(stat):
	os.system('clear')
	print("\n As you wander, you happen upon the remains of a caravan.")
	sleep(2.5)
	print(" It seems that some bandits attacked and stole most of the valuables.\n")
	sleep(2.5)
	p = random.randint(0,3)
	stat['potions'] += p
	g = random.randint(9,13)
	stat['p_G'] += g
	print(" However, leafing through the remains, you're still able")
	if p == 0:
		print(" to find", g, "gold.\n")
	elif p == 1:
		print(" to find", p, "potion and", g, "gold.\n")
	else:
		print(" to find", p, "potions and", g, "gold.\n")
	sleep(2)



# The "Magic Item" event lets the player find a Magic Ore for the Blacksmith sidequest or Magic Wood for the Sage sidequest.
# It is also used as currency for the fairies to run their stat roulette.
def magic_item(stat):

	os.system('clear')
	print("\n Next to the path, you notice something glimmering in the sunlight.")
	sleep(3)
	print(" It appears to be Magic ", stat['magic_item_type'], ".", sep="")
	sleep(1.5)

	if stat['quest'] == 1:
		print(" This must be what the", stat['magic_weaponer'], "was talking about!")
		sleep(2)
	elif stat['fairies'] == 2:
		print(" The fairies wanted it for their potions.")
		sleep(1.25)
	else:
		print(" It might have some importance later.")
		sleep(1.25)

	stat['magic_item'] += 1
	print("\n You gained 1 Magic ", stat['magic_item_type'], ".\n", sep="")
	sleep(1.5)

	return stat



# The "Rat with Hat" event is the first of 3 one time encounters, and happens in phase 1.
# The player meets Reginald the Rat, the leader of a swarm of monsters.
def rat_w_hat(stat, e_stat):
	os.system('clear')

	# If the player has already met Reginald, play any of the completed(stat) messages from above.
	if stat['rathat'] == True:
		complete(stat)
		return

	# Event start!
	stat['rathat'] == True
	print("\n A rat wearing a top hat and monocle walks up.")
	sleep(3)
	print(" It seems to be holding a cane with its tail.\n")
	sleep(3)

	# I like to imagine Reginald has a British accent here.
	print_red(" Pip pip cheerio old chap! Wonderful weather we have this\n")
	print_red(" noon, wouldn't you say?\n")

	# These loops are what allow the player to input their actions.
	# It accounts for both upper and lower case, and prevents the player from inputing an invalid action
	# There are a ton like this one in this document, so I will only explain how it works here.
	while True:
		# What the player can input. Note that they can only use [Y] or [N].
		print_yellow(" [Y]es    [N]o\n")
		x = input(' >>> ').lower()
		print()

		# If the player tries to use something that isn't [Y] or [N]:
		if x!='y' and x!='n':
			invalid()

		# Everything that follows after is the meat of what happens when the player inputs their action.
		elif x=='y':
			break
		elif x=='n':
			print_red(" Ah, you're a glass half empty fellow, I see.\n")
			sleep(3)
			break

	print_red(" If I may ask, good sir, what is your name?\n")

	# I wanted the player to be able to provide Reginald their name, or a couple of fake names.
	name = stat['p_name']

	# In order for it to look right, string slicing and concatenation is needed.
	# I have to account for the case where the player name starts with "R", hence the two input types and extra variable.
	if name[0].lower()=='r':
		while True:
			print_yellow(" [1] "+name+"    [R]att Slayir    [D]ave\n")
			x = input(' >>> ').lower()
			print()

			if x!='1' and x!='r' and x!='d':
				invalid()
			elif x=='1': break
			elif x=='r': name = "Ratt"; break
			elif x=='d': name = "Dave"; break

	else:
		while True:
			print_yellow(" ["+name[0]+"]"+name[1:]+"    [R]att Slayir    [D]ave\n")
			x = input(' >>> ').lower()
			print()

			if x!=name[0].lower() and x!='r' and x!='d':
				invalid()
			elif x==name[0].lower(): break
			elif x=='r': name = "Ratt"; break
			elif x=='d': name = "Dave"; break


	if name == stat['p_name']:
		print_red(" "+name+", eh? What a splendid name.\n")
		name = stat['p_name']
		sleep(2)

	elif name == "Ratt":
		print(" The rat visibly sudders.\n")
		sleep(1.5)
		print_red(""" Ratt Slayir? Tis an, uh, "interesting" name.\n""")
		sleep(2)

	elif name == "Dave":
		print_red(""" Huh. I've never had the pleasure of meeting a "Dave" before.\n""")
		sleep(3)


	# Here the player learns Reginald's name, and gets an inkling of his nefarious goals.
	print_red(" My friends call me Reginald.\n")
	sleep(2)
	print_red(" Say, you wouldn't happen to know where the nearest town is, would you?\n\n")
	sleep(3)
	print(" Reginald twirls his(?) cane and smiles menacingly.\n")
	sleep(4)

	print_red(""" I need a place to feed- er, "rest", after such a long day of travel.\n""")
	while True:
		print_yellow(" [A]ren't you a talking rat?    [R]ight down this path.\n")
		x = input(' >>> ').lower()
		print()
		if x!='a' and x!='r':
			invalid()

		# If the player decides to end the joke:
		elif x=='a':
			print_red(" No, no, I am most definitely a human.\n\n")
			sleep(2)
			break

		# On the off chance the player hasn't picked up on the cues, or is just chaotic evil and
		# wants to see what happens, they'll lose the game if they tell Reginald when the town is.
		# This is the only time the player can loose the early game.
		# I didn't want to put something like this later, because it is somewhat easy to fail,
		# and it would suck if the player looses the game after spending 20 minutes playing just beause of 1 choice.
		elif x=='r':
			print_red(" Oh really, that close? Thank you dearly!\n")
			sleep(3)
			print_red(" I do hope we have the chance to run into each other again some day, "+name+".\n")
			sleep(3)
			print_red(" And now, I bid you adieu.\n\n")
			sleep(2)
			print(" After exploring the forest for a while longer, you return to the village.")
			sleep(3)
			print(" Strangly, several monster corpses line the road.")
			sleep(3)
			print(" Additionally, the village Chief takes you to the jail and locks you up.\n")
			sleep(3)
			print_green(" We're placing you under arrest for aiding monsters.\n")
			while True:
				print_yellow(" [W]hat?\n")
				x = input(" >>> ").lower()
				print()
				if x!='w':
					invalid()
				elif x=='w':
					break
			print_green(" A talking rat came by leading a swarm, saying you led them here.\n")
			sleep(3)
			print_green(" We have already sent a messenger to Krocus.\n")
			sleep(3)
			print_green(" They'll bring a new adventurer to take out the Orc.\n")
			sleep(3)
			print_green(" You disgust me.\n")
			sleep(3)
			print_red("\n Game Over.\n")
			sleep(3)
			sys.exit(0)

	print(" Reginald's tail flicks around.")
	while True:
		print_yellow(" [Y]ou look like a rat to me.\n")
		x = input(" >>> ").lower()
		print()
		if x!='y':
			invalid()
		elif x=='y':
			break

	print_red(" Please, "+ name +". That's rather rude of you.\n\n")
	sleep(2)

	print(" The hat droops a little.")

	# I thought this might be a fun chance to reference Little Red Riding Hood.
	while True:
		print_yellow(" [B]ut Reginald, what round ears you have!\n")
		x = input(" >>> ").lower()
		print()
		if x!='b':
			invalid()
		elif x=='b':
			break

	print_red(" The better to hear you with.\n\n")
	sleep(2)
	while True:
		print_yellow(" [B]ut Reginald, what beady eyes you have!\n")
		x = input(" >>> ").lower()
		print()
		if x!='b':
			invalid()
		elif x=='b':
			break

	print_red(" The better to see you with.\n\n")
	sleep(2)
	while True:
		print_yellow(" [B]ut Reginald, what gnarled teeth you have!\n")
		x = input(" >>> ").lower()
		print()
		if x!='b':
			invalid()
		elif x=='b':
			break

	# Reginald finally gives up, and the battle begins.
	print_red(" The better to... bah! Forget it!\n")
	sleep(1.5)
	print_red(" Saw through my ingenious disguise, eh?\n")
	sleep(2.6)
	print_red(" Well, you're not leaving here alive! Muahaha!\n\n")
	sleep(2.75)
	print(" Reginald brandishes the cane.")
	sleep(4)
	reginald(e_stat)
	battle(stat, e_stat)



# The shopbro event occurs in the 2nd phase of the game.
# It gives the player the chance to save the Shopkeep's brother, Daniel.
# If they fail it, the Shopkeep will only have 4 potions left in stock before his supply runs out.
# The only other way to get potions is through the Caravan event.
# If they do succeed, however, the Shopkeep's potions are forever discounted.
def shopbro(stat):

	os.system('clear')
	
	# If the player has already met Daniel, play any of the completed(stat) messages.
	if stat['shopbro'] != 0:
		complete(stat)

	else:
		print("\n As you walk through the forest, you notice a handsome man riddled with")
		print(" arrows.")
		sleep(2.5)
		print(" His blood lines the side of the road.")
		sleep(2)
		print(" Beside him is a large basket full of plant leaves.\n")
		sleep(2)

		# Of course, who wouldn't stike up a conversation with a complete stanger on their deathbed?
		print_cyan(" Good day, fellow traveler. What brings you out here?\n")
		while True:
			print_yellow(" [E]xploring the Forest    [F]ighting the Orc    [N]unya business.\n")
			x = input(' >>> ').lower()
			print()
			if x!='e' and x!='f' and x!='n':
				invalid()
			elif x=='e':
				print_cyan(" It IS a nice day.\n")
				sleep(1.5)
				print_cyan(" Well, was.\n")
				sleep(1)
				break
			elif x=='f':
				print_cyan(" You're the adventurer? Thank goodness we have one.\n")
				sleep(2.5)
				break
			elif x=='n':
				print_cyan(" Sorry, I don't mean to pry.\n") 
				sleep(1)
				print_cyan(" Apparently, I get a little chatty when I'm about to kick the bucket.\n")
				sleep(3)
				break

		print_cyan(" Hey, don't suppose you can... help a fellow out?\n")
		while True:
			print_yellow(" [W]ho are you?\n")
			x = input(" >>> ").lower()
			print()
			if x!='w':
				invalid()
			elif x=='w':
				break

		# I don't know when I decided that there had to be a feud between the two brothers over who is more handsome.
		# I do know that it makes me really happy, for no reason.
		# Also, I thought it would be fun to add some lore here.
		# Most games don't really go into where stores get their merchandise, so I provided my own explanation.
		print_cyan(" I'm the handsomer brother of the shopkeep. Make his potions myself.\n")
		sleep(2.25)

		print_cyan(" Speaking of, you wouldn't happen to have something to fix all of...\n")
		print_cyan(" this, would you?\n")
		while True:
			print_yellow(" [W]hat can I do?    [S]orry, I have things to do.\n")
			x = input(" >>> ").lower()
			print()
			if x!='w' and x!='s':
				invalid()
			elif x=='w':
				break
			elif x=='s':
				stat['shopbro'] = 2
				print_cyan(" Oh, I guess we all have our troubles.\n")
				sleep(1.5)
				print_cyan(" Sorry to take up your time.\n")
				sleep(1.5)
				print_cyan(" Please forget about me.\n\n")
				sleep(1.5)
				print(" You walk away from the dying man, trying not to see the tears")
				print(" rolling down his face.")
				sleep(4)
				return stat

		# At this point, hopefully the player has two potions always stocked.
		# If not, Daniel will die here.
		print_cyan(" Oh, I dunno, if you had a spare potion, that'd be pretty nifty.\n")
		while True:
			print_yellow(" [Y]eah, take this: Potion ("+str(stat['potions'])+")    [F]resh out.    [N]o, these are mine.\n")
			x = input(' >>> ').lower()
			print()
			if x!='y' and x!='f' and x!='n':
				invalid()
			elif x=='y':
				if stat['potions'] < 2:
					print(" You don't have a potion to give.\n")
					sleep(1)
				else:
					stat['potions'] -= 2
					stat['shopbro'] = 1
					break

			# The moment you tell Daniel that he's going to die.
			# I'm sorry, Daniel.
			elif x=='f':
				stat['shopbro'] = 2
				print_cyan(" Really? Just my luck.\n")
				sleep(1)

				print_cyan(" Can you at least stay here, so I don't die alone?\n")
				while True:
					print_yellow(" [O]f course.\n")
					x = input(" >>> ").lower()
					print()

					if x!='o':
						invalid()

					elif x=='o':
						print(" Once the man draws his last breathe, you continue somberly")
						print(" on your way.\n")
						sleep(3)
						return stat

			# If the player wants to be a huge jerk, I did give them this option.
			elif x=='n':
				stat['shopbro'] = 2
				print_cyan(" Well then. Please leave now, Mr. Better Than Thou.\n") 
				sleep(3)
				print_cyan(" I don't want such toxic company when I die.\n\n")
				sleep(3)
				print(" You leave the shopkeep's brother alone and continue on your merry way.")
				sleep(3)
				return stat

		# Should the player succeed, everything afterwards is just conversation, with no bearing on the rest of the game.
		if stat['shopbro'] == 1:
			print_cyan(" Thanks so much, friend.\n\n")
			sleep(1)
			print(" The man drinks the potion as you pull out the arrows.\n")
			sleep(2)
			print_cyan(" I'm going to just rest up here for now. Thank you for the help.\n")

			print_cyan(" The name's Daniel, by the way.\n")
			n = stat['p_name']
			while True:
				print_yellow(" My name's...\n")
				print_yellow(" ["+n[0]+"]"), print_yellow(n[1:]), print_yellow("    [N]ever mind.\n")
				x = input(' >>> ').lower()
				print()
				if x!=n[0].lower() and x!='n' :
					invalid()
				elif x==n[0].lower():
					name = stat['p_name']
					print_cyan(" Well, nice to meet you, "+name+".\n")
					sleep(3.5)
					break
				elif x=='n':
					print_cyan(""" Well, thanks again for your help, "Never Mind".\n""")
					sleep(3.25)
					break
			print_cyan(" I should be fine here on my own.\n")
			sleep(1.5)
			print_cyan(" Hope I see you around the village!\n\n")
			sleep(1.5)
			print(" You leave Daniel in high spirits.\n")
			sleep(3)
			return stat



# The Fairy Fountain Event happens in Phase 3 of the game.
# In it, the player has the option of trading their excess magical resources for a chance to raise their stats.
# However, fairies are mischeivous, and have a 1:4 chance of lowering the stat as well.
# At least the player can choose which stat they want to wager, right?
# This one was the most difficult to plot out, as you have to first hear about the Fountain from the Inn, then find it in the forest.
# After that, I wanted the player to be able to come back at any time while exploring the forest.
# However, the player can decline to drink the first offered potion, so I had to come up with a way that would let them redrink it, if they wanted.
# The way the exploration system is set up, I had to also have a complete(stat) message if they ever stumbled back onto in when exploring the forest.
# And all this is stupidly done through 1 variable, because I felt that the dictionary was getting too long.
# That's basically how everything else in the game happened though: I'd start off with a medium sized item, then get ideas and expand it.
# 5 hours later, I'd finally be done coding all the odds and ends I thought the game needed.
# Anyways, rant over. On to the code.
def fairies(stat):

	# If the player has already found the Fountian while exploring the forest, play any of the complete(stat) messages.
	if stat['fairies'] == 5:
		complete(stat)
		return stat

	# This part is for when the player has found the Fountain for the first time.
	elif stat['fairies'] == 1:
		os.system('clear')

		print("\n A gentle song fills your ears from a nearby cave.")
		sleep(2.5)
		print(" Following it, you find a fountain with several fairies.")
		sleep(2.5)
		print(" One of them flitters up to you, speaking quickly:\n")
		sleep(2.5)
		print_magenta(" Hi welcome to our fountain wanna drink?!\n\n")
		sleep(2)

		print(" The fairy proffers up a small bowl with blue liquid.")
		while True:
			print_yellow(" [D]rink    [B]ad idea.\n")
			x = input(' >>> ').lower()
			print()
			if x!='d' and x!='b':
				invalid()

			# If the player decides not to drink the Kool Aid:	
			elif x=='b':
				stat['fairies'] = 2
				print(" In a wise decision, you decide not to drink the sketchy juice given")
				print(" to you by some hyperactive rando you just met in the woods.\n")
				sleep(4.5)
				return

			# Else if they do:
			elif x=='d':
				stat['fairies'] = 3
				print(" Readying yourself, you gulp it down in one swig.")
				sleep(2)
				print(" Suddenly, your body feels as though it is on fire!")
				sleep(2.25)
				print(" .",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!\n"), sleep(1)
				
				# Here, you can see the gambling at work.
				# I chose DEF to be the stat effect the first time, since there are the least consequences if the player looses it.
				# As previously mentioned, there 3:1 chance of gaining:losing stats.
				# Overall, I'd say it's still worth the risk.
				if random.randint(0,3)==0:
					t = random.randint(3,5)
					stat['p_DEF'] -= t
					print_white(" Your DEF just "), print_red("dropped by "+str(t)+"!\n\n")
					sleep(1.5)
					break
				else:
					if random.randint(1,3) == 3: t = 2
					else: t = 1
					stat['p_DEF'] += t
					print_white(" Your DEF just "), print_green("rose by "+str(t)+"!\n\n")
					sleep(1.5)
					break

		print_magenta(" We have more if you want!\n")
		sleep(1.5)
		print_magenta(" Enough for all stats!\n")
		sleep(2)
		print_magenta(" Just bring magic stuff!\n")
		sleep(1.5)
		print_magenta(" Okay bye now.\n\n")
		sleep(1)
		stat['fairies'] == 3


	# This section plays when the player returns to the Fountain via the exploration menu having not yet drunk their first potion.
	elif stat['fairies'] == 2:

		os.system('clear')
		print(" The fairy from before comes up, holding the same strange blue liquid.\n")
		sleep(2.75)

		print_magenta(" Oh you came back wanna drink now?!\n")
		sleep(1.5)
		while True:
			print_yellow(" [D]rink    [S]till a bad idea.\n")
			x = input(' >>> ').lower()
			print()
			if x!='d' and x!='s' :
				invalid()

			# The player can still deny drinking the potion. If they ever come back, it'll just loop throught this part again.
			elif x=='s':
				stat['fairies'] = 2
				print(" You decide that taking drugs'd be a bad call.")
				sleep(1.5)
				print_magenta(" Okay well see you later!\n\n")
				sleep(1.5)
				return

			# Once they finally do drink, though, thee player can finally progress through this... sidequest?
			elif x=='d':
				stat['fairies'] = 3
				print(" Readying yourself, you gulp it in one swig.")
				sleep(2)
				print(" Suddenly, your body feels as though it is on fire!")
				sleep(2.25)
				print(" .",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!\n"), sleep(1)
				if random.randint(0,3)==0:
					t = random.randint(3,5)
					stat['p_DEF'] -= t
					print_white(" Your DEF just "), print_red("dropped by "+str(t)+"!\n\n")
					sleep(1.5)
					break
				else:
					if random.randint(1,3) == 3: t = 2
					else: t = 1
					stat['p_DEF'] += t
					print_white(" Your DEF just "), print_green("rose by "+str(t)+"!\n\n")
					sleep(1.5)
					break

		print_magenta(" We have more if you want!\n")
		sleep(1.5)
		print_magenta(" Enough for all stats!\n")
		sleep(2)
		print_magenta(" Just bring magic stuff!\n")
		sleep(1.5)
		print_magenta(" Okay bye now.\n\n")
		sleep(1)
		stat['fairies'] == 3

	# And this is the part for when the player has finally caved. At this point, they can wager any of their stats.
	# The random level up chance is rarer, as the benefits are more beneficial.
	elif stat['fairies'] == 3:
		os.system('clear')

		print_magenta("\n Welcome back wadaya want?!\n")
		while True:

			print_white(" You currently have: "), print_green(str(stat['magic_item'])+" "+ stat['magic_item_type'])
			print()
			print_yellow("\n [A]TT Juice    [D]EF Juice    [H]P Juice    [L]evel Juice    [N]one")
			y = input("\n >>> ").lower()
			print()
			if y!='l' and y!='h' and y!='a' and y!='d' and y!='n':
				invalid()

			# This part is for if the player wants to raise only their ATT stat.
			# It mirrors the DEF raising section below.
			elif y=='a':
				print(" The fairy hands you a red liquid.")
				sleep(1.75)
				print(" Are you sure you want to drink it?")
				while True:
					print_yellow(" [Y]es    [N]o")
					u = input("\n >>> ").lower()
					print()
					if u!='y' and u!='n':
						invalid()
					elif u=='n':
						print(" You hand back the liquid.\n")
						sleep(1)
						break
					elif u=='y':
						stat['magic_item'] -= 1
						print(" After readying yourself, you take a large gulp.")
						sleep(2)
						print(" The familiar fire burns within your body.")
						sleep(2.25)
						print(" .",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!\n"), sleep(1)
						if random.randint(0,3)==0:
							t = random.randint(3,5)
							stat['ATT'] -= t
							print_white(" Your ATT just"), print_red(" dropped by "+str(t)+"!\n")
							sleep(1.5)
						else:
							if random.randint(1,3) == 3: t = 2
							else: t = 1
							stat['ATT'] += t
							print_white(" Your ATT just"), print_green(" rose by "+str(t)+"!\n")
							sleep(1.5)
						print()
						break

			# This part is for if the player wants to raise only their DEF stat.
			# It mirrors the ATT raising section above.
			elif y=='d':
				print(" The fairy hands you a blue liquid.")
				sleep(1.75)
				print(" Are you sure you want to drink it?")
				while True:
					print_yellow(" [Y]es    [N]o")
					u = input("\n >>> ").lower()
					print()
					if u!='y' and u!='n':
						invalid()
					elif u=='n':
						print(" You hand back the liquid.\n")
						sleep(1)
						break
					elif u=='y':
						stat['magic_item'] -= 1
						print(" After readying yourself, you take a large gulp.")
						sleep(2)
						print(" The familiar fire burns within your body.")
						sleep(2.25)
						print(" .",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!\n"), sleep(1)
						if random.randint(0,3)==0:
							t = random.randint(3,5)
							stat['p_DEF'] -= t
							print_white(" Your DEF just"), print_red(" dropped by "+str(t)+"!\n")
							sleep(1.5)
						else:
							if random.randint(1,3) == 3: t = 2
							else: t = 1
							print_white(" Your DEF just"), print_green(" rose by "+str(t)+"!\n")
							sleep(1.5)
						print()
						break

			# This part is for if the player wants to raise only their HP.
			# It works like a potion in that it raises both the base and the current the same amount at the same time.
			# Or lowers, if the player has bad luck.
			elif y=='h':
				print(" The fairy hands you a green liquid.")
				sleep(1.75)

				print(" Are you sure you want to drink it?")
				while True:
					print_yellow(" [Y]es    [N]o")
					u = input("\n >>> ").lower()
					print()
					if u!='y' and u!='n':
						invalid()
					elif u=='n':
						print(" You hand back the liquid.\n")
						sleep(1)
						break
					elif u=='y':
						stat['magic_item'] -= 1
						print(" After readying yourself, you take a large gulp.")
						sleep(2)
						print(" The familiar fire burns within your body.")
						sleep(2.25)
						print(" .",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!\n"), sleep(1)
						if random.randint(0,3)==0:
							t = random.randint(6,10)
							stat['current_HP'] -= t
							stat['base_HP'] -= t
							print_white(" Your base HP just"), print_red(" dropped by "+str(t)+"!\n")
							sleep(1.5)
						else:
							t = random.randint(5,7)
							stat['current_HP'] += t
							stat['base_HP'] += t
							print_white(" Your base HP just"), print_green(" rose to "+str(stat['base_HP'])+"!\n")
							sleep(1.5)
						print()
						break

			# If they want to try to get an easy level up:
			# Note that this uses a truncated version of the leveling system from leveling_system.py on Line 660 and 684.
			elif y=='l':
				print(" The fairy hands you a yellow liquid.")
				sleep(1.75)

				print(" Are you sure you want to drink it?")
				while True:
					print_yellow(" [Y]es    [N]o")
					u = input("\n >>> ").lower()
					print()
					if u!='y' and u!='n':
						invalid()

					# This part lets the player return the potion in case they didn't mean to pick this one, or is having second thoughts.
					elif u=='n':
						print(" You hand back the liquid.\n")
						sleep(1)
						break

					elif u=='y':
						stat['magic_item'] -= 1
						print(" After readying yourself, you take a large gulp.")
						sleep(2)
						print(" The familiar fire burns within your body.")
						sleep(2.25)
						print(" .",end=""), sleep(1), print(".",end=""), sleep(1), print(".",end=""), sleep(1), print("!\n"), sleep(1)
						if random.randint(0,1)==0:
							stat['p_LV'] -= 1
							print_red(" You lost a level!\n")
							sleep(1.5)
							stat['current_exp'] = 0
							stat['next_level_exp'] = round((6 * (stat['p_LV']**.769))-7.182)
							stat['ATT'] -= random.randint(1, 2)
							HP = random.randint(1, 2)
							stat['current_HP'] -= HP
							stat['base_HP']  -= HP
							x = random.randint(1, 8)
							if x == 7:
								stat['p_DEF'] -= 1
								x = -1

							print_white(" HP"), print_red(" dropped to: "+str(stat['base_HP']))
							print()
							print_white(" ATT"), print_red(" dropped to: "+str(stat['ATT']))
							print()
							if x == -1:
								print_white(" DEF"), print_red(" dropped to: "+str(stat['p_DEF']))
								print()
							sleep(1.5)
						
						else:
							stat['p_LV'] += 1
							print_green(" You gained a level!\n")
							sleep(1.5)
							stat['current_exp'] = 0
							stat['next_level_exp'] = round((6 * (stat['p_LV']**.769))-7.182)
							stat['ATT'] += random.randint(1, 2)
							HP = random.randint(1, 2)
							stat['current_HP'] += HP
							stat['base_HP']  += HP
							x = random.randint(1, 8)
							if x == 7:
								stat['p_DEF'] += 1
								x = -1

							print_white(" HP"), print_green(" rose to: "+str(stat['base_HP']))
							print()
							print_white(" ATT"), print_green(" rose to: "+str(stat['ATT']))
							print()
							if x == -1:
								print_white(" DEF"), print_green(" rose to: "+str(stat['p_DEF']))
								print()
							sleep(1.5)
						print()
						break

			# Once the player is ready to leave, or they no longer have any magic resources to trade with, they can head back out into the forest.
			if y=='n' or stat['magic_item'] == 0:
				print_magenta(" Thanks bye bye!\n\n")
				sleep(.75)
				return stat

			# If the player has stocked up on magic resources, and wants to try again with the same or a different stat:
			if y=='l' or y=='h' or y=='a' or y=='d':
				print_magenta("\n Wanna drink another?!\n")
				while True:
					print_yellow(" [Y]es ("+str(stat['magic_item'])+")    [N]o")
					y = input("\n >>> ").lower()
					print()
					if y!='y' and y!='n':
						invalid()
					elif y=='y':
						os.system('clear')
						print()
						break
					elif y=='n':
						print_magenta(" Thanks bye bye!\n\n")
						sleep(.75)
						return stat
						
# This is the last single time encouter.
# It is very short, as it simply dictates that the player has found the orc, and can now go battle it at any time.
def orc_battle(stat):
	if stat['orc'] == True:
		complete(stat)
		return stat

	else:
		stat['orc'] = True
		os.system('clear')
		print("\n You break out into a clearing. At the far side is a cave entrance.")
		sleep(3)
		print(" Large footprints have trampled the ground all around.")
		sleep(2.8)
		print(" This and the various animal corpses strewn about, lead to one conclusion.")
		sleep(3)
		print(" At long last, you have discovered the orc.")
		sleep(4)
		print(" After marking down this location, you leave to prepare for the upcoming")
		print(" fight.\n")
		sleep(4)
		return stat


# The exploring function is what is called from town.py to explore the forest.
# There are three Phases, depending on the player's level, dictating the three parts of the game.
# Each part has ever harder enemies, and a higher chance of finding magic items to complete that sidequest.
# Caravans become rarer, as the player has more money to decide whether or not they want potions or to sleep in the inn.
def exploring(stat, e_stat):

	# This is for the final part of the Magic Weapon Quest.
	# The player has to go do something else to give the weaponer some time to make the weapon.
	if stat['quest'] == 2: stat['quest'] = 3

	while True:
		
		# Phase 1
		if stat['p_LV'] <= 7:
			x = random.randint(1, 18)
			if 1<=x<=5:
				print(" A goblin appeared!")
				sleep(2)
				goblin(e_stat)
				battle(stat, e_stat)
			elif 6<=x<=9:
				print(" It's a rat!")
				sleep(2)
				rat(e_stat)
				battle(stat, e_stat)
			elif 10<=x<=13:
				print(" A slime squelches up!")
				sleep(2)
				slime(e_stat)
				battle(stat, e_stat)
			elif 14<=x<=16:
				rat_w_hat(stat, e_stat)
			elif x == 17:
				caravan(stat)
			elif x == 18:
				magic_item(stat)

		# Phase 2
		elif stat['p_LV'] <= 12:
			x = random.randint(1, 26)
			if 1<=x<=6:
				print(" A wolf howls!")
				sleep(1.25)
				wolf(e_stat)
				battle(stat, e_stat)
			elif 7<=x<=12:
				print(" Webs are everywhere. It's a giant spider!")
				sleep(2)
				large_spider(e_stat)
				battle(stat, e_stat)
			elif 13<=x<=18:
				print(" Sneaking up behind you, a snake appears!")
				sleep(3)
				snake(e_stat)
				battle(stat, e_stat)
			elif 19<=x<=21:
				shopbro(stat)
			elif x==22:
				caravan(stat)
			elif 23<=x<=26:
				magic_item(stat)

		# Phase 3
		else:
			x = random.randint(1, 18)
			if 1<=x<=3:
				print(" An enraged bear crashes throught the trees!")
				sleep(3)
				bear(e_stat)
				battle(stat, e_stat)
			elif 4<=x<=6:
				print(" With armor and sword in hand, a gobin attacks!")
				sleep(3)
				goblin_warrior(e_stat)
				battle(stat, e_stat)
			elif 7<=x<=8:
				print(" A goblin shaman fires magic at you!")
				sleep(3)
				goblin_shaman(e_stat)
				battle(stat, e_stat)
			elif 9<=x<=10:
				print(" Riding a wolf, a goblin fires his bow!")
				sleep(3)
				goblin_rider(e_stat)
				battle(stat, e_stat)
			elif 11<=x<=12:
				f = stat['fairies']
				if stat['fairies'] != 1:
					stat['fairies'] = 5
				fairies(stat)
				stat['fairies'] = f
			elif x==13:
				caravan(stat)
			elif 14<=x<=15:
				magic_item(stat)
			elif 16<=x<=18:
				orc_battle(stat)
		
		# Once the player has completed their first exporation of the forest, they have a few options.
		# They can explore more, check their stats, drink a potion in safety, or head back to town.
		# And if they've found the fairies, or the orc's den, the player can search there as well.
		# Note that [M]ore will only appear if they've discovered those locations, which is why it looks weirder than most of the other input sections.
		print(" Continue exploring? Or head back to town?")
		while True:
			print_yellow(" [E]xplore    [C]heck Stats    [P]otion ("+str(stat['potions'])+")    [H]ead Back")

			# Because [M]ore should only display when you've encountered the fairies or orc, I had to mess around with the normal input formula to make sure the user couldn't advance to those areas too soon.
			if stat['fairies'] == 2 or stat['fairies'] == 3 or stat['orc'] == True: more = True
			else: more = False

			if more == True:
				print_yellow("    [M]ore")

			y = input("\n >>> ").lower()
			print()
			if y!='e' and y!='c' and y!='p' and y!='h' and y!='m':
				invalid()

			elif y=='e':
				break

			elif y=='c':
				check_stats(stat)
				print()

			elif y=='p':
						
				# Just in case the player no longer has any potions:
				if stat['potions'] == 0:
					print(' Out of potions.\n')
					sleep(.5)

				# Otherwise, restore their health. Tell the player so.
				else:
					stat['potions'] -= 1
					stat['current_HP'] += round(random.randint(4,10)* 4.2)

					if stat['current_HP'] > stat['base_HP']:
						stat['current_HP'] = stat['base_HP']

					print_white(' HP restored to '), print_green(str(stat['current_HP'])+'/'+str(stat['base_HP'])+'\n')

			elif y=='h':
				os.system('clear')
				return

			elif y=='m':
				if more == False: invalid()

				else:

					while True:
						if stat['orc'] == True:
							print_yellow(" [O]rc Fight   ")
						if stat['fairies'] == 2 or stat['fairies'] == 3:
							print_yellow(" [F]airy Fountain   ")
						print_yellow(" [M]ore\n")
						y = input(" >>> ").lower()
						print()
						if y!='o' and y!='f' and y!='m':
							invalid()

						elif stat['orc'] == True and y=='o':
							print(" You return to the clearing, to finally bring this adventure to a close!")
							sleep(3.5)
							orc(e_stat)
							battle(stat, e_stat)
							return stat

						elif 'fairies'!= 0 and y=='f':
							fairies(stat)
							break

						elif y=='m':
							break



# Testing for all the different random encounters.
# It also lets me see if the one time encounters are working.
if __name__ == '__main__':

	stat = {
		'p_name': 'Roberson',
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
		'orc': True
		}

	e_stat = {
		'e_type': "Raq Coon, Bane of Chickens",
		'e_DEF': 10000,
		'e_HP': 10000,
		'e_LV': 30,
		'e_EXP': random.randint(1,2),
		'e_G': random.randint(1,2)
		}

	#caravan(stat)
	rat_w_hat(stat, e_stat)
	#magic_item(stat)
	#shopbro(stat)
	#shopbro(stat)
	#print(stat['shopbro'])
	#print(stat['potions'])
	#fairies(stat)
	#rat_w_hat(stat)
	#magic_item(stat)
	#orc_battle(stat)
	#orc_battle(stat)

	#exploring(stat, e_stat)