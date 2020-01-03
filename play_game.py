# play_game.py
# This is the file the player will call to play the game.

import os
import sys
import random
import base64
from time import sleep
from pathlib import Path
from graphics import *
from colored_text import *
from town import town

# Introducing: Console Quest!
os.system('clear')
print("""\033[32m
  _____
 |  _  |       ___   ___   _   _    ____   ___   _     ____        / \ 
 | |_| |      /  _| | _ | |  \| |  |  __| | _ | | |   | ___|      / //
 |_____|\     | |_  ||_|| | |\  |  _\ \   ||_|| | |_  | __|      / //
      \  \    \___| |___| |_| \_| |___/   |___| |___| |____|    / //
       \  \    --------------------------------------------    / //
        \  \        ___    _  _   ____    ____   _____        / //
         \  \      | _ |  | || | | ___|  |  __| |_   _|    __/_//
          \  \     ||_||_ | || | | __|   _\ \     | |     /___  \ 
           \  \    |____/ |____| |____| |___/     |_|      /\/\_|
            \  \    ----------------------------------    /\/
             \__\                                        /_/


""")

sleep(1)

# Initiate to dictionary that holds all the variables.
# This gets overwritten when the player creates a new character or loads one in.
# There is also a dictionary for the enemy stats.
stat = {
	'p_name': 'None',
	'p_class': 'None',
	'p_LV': 3,
	'ATT': 0,
	'ATT_type': 'None',
	'p_DEF': 0,
	'current_HP': 0,
	'base_HP': 0,
	'current_exp': 0,
	'next_level_exp': 4,
	'potions': 0,
	'p_G': 0,
	'quest': 0,
	'magic_weapon': "None",
	'mwc': False,
	'magic_weaponer': 'Blacksmith',
	'magic_item_type': 'Ore',
	'magic_item': 0,
	'shield': False,
	'rathat': False,
	'shopbro': -1,
	'p_left': 0,
	'fairies': 0,
	'inn': 0,
	'orc': False,
	'user': 'None'
	}

e_stat = {  
	'e_type': "None",
	'e_DEF': 0,
	'e_HP': 0,
	'e_LV': 1,
	'e_EXP': 0,
	'e_G': 0,
	}


# The tutorial that introduces the player to the "system" and hold to play the game.
def tutorial(stat):

	# If the player had a previous save state, or has completed the game, they have the option to skip the tutorial.
	if Path('Hall of Fame.txt').exists() or Path('save_state.txt').exists():
		print_white(" Skip tutorial?")
		while True:
			print_yellow(" [Y]es    [N]o\n")
			x = input(' >>> ').lower()
			print()
			if x!='y' and x!='n':
				invalid()

			elif x=='y':
				return

			else:
				break

	# Else, meet "System".
	print_white("\n Hello!\n")
	sleep(1)
	print_white(" I am the game system.\n")
	sleep(1)
	print_white(" I'll be with you every step of the way as you play this game.\n")
	sleep(1.3)
	print_white(" First, what's your name?\n")
	stat['user'] = input(" >>> ")
	print_white(" Hi there, "+stat['user']+".\n")
	sleep(1.5)
	print_white("\n Text color will be pretty important throughout this game.\n")
	sleep(2)
	print_white("\n White text like mine indicates stuff that I'm directly telling you,\n")
	print_white(" and cannot be heard or seen by anybody else in game.\n")
	sleep(1.75)
	print_white("\n Other colors exist for other purposes, like differentiating who's\n")
	print_white(" talking at a given time.\n")
	sleep(2)

	print_white(" For example, the Innkeep will always speak in ")
	print_green("green")
	print_white(",\n while the Shopkeep will always speak in ")
	print_cyan("cyan")
	print_white(".\n")
	sleep(2.4)

	print_white(" I'll also occasionally borrow other colors for effect, like just now.\n")
	sleep(3)
	print_white(" Got it?\n")
	print_yellow(" [Y]eah.\n")
	print(" >>> ")
	sleep(.5)
	print_white("\n Oh, that's right, you as the player will always speak in \n")
	for i in " yellow":
		sys.stdout.write("\033[33m" + i)
		sys.stdout.flush()
		sleep(.03)
	print_white(".\n")
	sleep(3)
	print_white(" You'll often be prompted to provide an answer to a question.\n")
	sleep(2)
	print_white(" Just type the first letter of the input you'd like to procede.\n")
	sleep(2)
	print_white(" Do you understand?\n")

	# These loops are what allow the player to input their actions.
	# It accounts for both upper and lower case, and prevents the player from inputing an invalid action.
	# There are a few like this one in this document, so I will only explain how it works here.
	while True:
		# What the player can input. Note that they can only use [Y] or [N].
		print_yellow(" [G]ot it.    [N]ope, not at all.\n")
		x = input(' >>> ').lower()
		print()

		# If the player tries to use something that isn't [Y] or [N]:
		if x!='g' and x!='n':
			invalid()

		# Everything that follows after is the meat of what happens when the player inputs their action.
		elif x=='g':
			print_white(" Coolio.\n")
			sleep(1.8)
			break

		else:
			print_white(" Are you sure? Because you're doing it just fine right now.\n")
			sleep(1)

	os.system('clear')
	print_white("\n Alright, let's get the game underway.")
	sleep(3)



# In this portion, the player chooses what class the want to play, as well as their names.
def player_select(stat):
	
	while True:
		print_white("\n What class would you like to play?\n")
		sleep(.5)
		print(" Warrior:        Sorcerer:       Rogue:")
		print(" HP:  "+"\033[32m"+"Higher     "+"\033[37m"+"HP:  "+"\033[32m"+"Higher     "+"\033[37m"+"HP:  "+"\033[31m"+"Lower\n",end="")
		print(" ATT: Average    ATT: "+"\033[31m"+"Lower      "+"\033[37m"+"ATT: "+"\033[32m"+"Higher\n",end="")
		print(" DEF: Average    DEF: "+"\033[32m"+"Higher     "+"\033[37m"+"DEF: "+"\033[31m"+"Lower\n",end="")
		print()
		while True:
			print_yellow(" [W]arrior       [S]orcerer      [R]ogue\n")
			x = input(' >>> ').lower()
			print()
			if x!='w' and x!='s' and x!='r':
				invalid()

			# The Warrior class. Has higher HP, average attack, and average defense.
			elif x=='w':
				stat['p_name'] = 'Grog'
				stat['p_class'] = 'Warrior'
				stat['ATT'] = 5
				stat['ATT_type'] = 'slashes at'
				stat['p_DEF'] = 9
				stat['current_HP'] = 17
				stat['base_HP'] = 17
				stat['potions'] = 2
				stat['p_G'] = 2
				stat['magic_weapon'] = 'Damascus Sword'
				stat['p_left'] = 4
				break

			# The sorcerer class. Has higher HP, lower attack, and higher defense.
			elif x=='s':
				stat['p_name'] = 'Magnus'
				stat['p_class'] = 'Sorcerer'
				stat['ATT'] = 4
				stat['ATT_type'] = 'fires magic at'
				stat['p_DEF'] = 10
				stat['current_HP'] = 20
				stat['base_HP'] = 20
				stat['potions'] = 2
				stat['p_G'] = 2
				stat['magic_weapon'] = "Warlock Staff"
				stat['p_left'] = 4
				stat['magic_weaponer'] = 'Wizard'
				stat['magic_item_type'] = 'Wood'
				break

			# The Rogue class. Has lower HP, higher attack, and lower defense.
			elif x=='r':
				stat['p_name'] = 'Feif'
				stat['p_class'] = 'Rogue'
				stat['ATT'] = 6
				stat['ATT_type'] = 'stabs'
				stat['p_DEF'] = 7
				stat['current_HP'] = 15
				stat['base_HP'] = 15
				stat['potions'] = 0
				stat['p_G'] = 10
				stat['magic_weapon'] = 'Vorpal Daggers'
				stat['p_left'] = 6
				break

		# The player chooses their character's name.
		# Each class has a default name to choose, if they want to.
		print_white(" Sweet. Now, what's your character's name?\n")
		sleep(1.5)
		print_white(" By default, it's "+stat['p_name']+".\n")
		sleep(1.5)
		print_white(" If you want to leave it that way, just hit [Enter].\n")
		sleep(1.5)
		print_white(" Otherwise, type in a name! (Max Character Limit 8)\n")

		while True:
			x = input(" >>> ")
			if len(x)>8:
				print_white("\n That name is too long!")
				sleep(1)
			elif x == "":
				print()
				break
			else:
				stat['p_name'] = x
				print()
				break

		print_white(" You will play as ")

		print_magenta(stat['p_name'] + "the" + stat['p_class'])

		print_white("!\n")
		sleep(2)
		print_white(" Are you sure this is who you want to play as?\n")
		while True:
			print_yellow(" [Y]es    [N]o\n")
			x = input(' >>> ').lower()
			print()
			if x!='y' and x!='n':
				invalid()

			elif x=='y':
				return stat
			else:
				os.system('clear')
				print()
				break

	
# The story potion introduces the player to the world and vaguely outlines what they need to do.
def story():
	os.system('clear')
	print_white("\n Alright, here's the lowdown.")
	sleep(1.5)
	print_white(" You work at the Adventurer's Guild in the city of Krocus.")
	sleep(2.25)
	print_white(" After gaining some experience completing small quests, you've decided")
	print_white(" to go on your first major one.\n")
	sleep(2)
	print_white(" A small village in the backcountry has been forced to pay tributes to")
	print_white(" an orc for several years.")
	sleep(2)
	print_white(" It regulaly moves around, so other adventures have had trouble")
	print_white(" finding and slaying it.")
	sleep(2)
	print_white(" Up until now, the villagers have been able to keep the orc satisfied.")
	sleep(3)
	print_white(" But recently, it's been asking for ever larger sums, and the villagers")
	print_white(" won't be able to keep paying for much longer.")
	sleep(2)
	print_white(" Your task is to find the orc, and kill him before he attacks and kills")
	print_white(" everybody.\n")
	sleep(2)
	print_white(" You just arrived in town the other day, so many of the villagers only")
	print_white(" know rumors of you.")
	sleep(2.25)
	print_white(" Feel free to introduce yourself, or head straight out into the forest")
	print_white(" to start your search for the orc!\n")
	sleep(3)




# The actual 'game' per se starts here.
# If the player has a previous save state, they have the option of loading it it skip the introduction, player creation, and story.
if Path('save_state.txt').exists():
	new_game_break = False
	while True:
		print_yellow(" [N]ew Game    [L]oad Game    [C]lose\n")
		x = input(' >>> ').lower()
		print()
		if x!='n' and x!='l' and x!='c':
			invalid()

		# New Game
		# If the player wants to start from scratch, they can do so here.
		# I wanted to make sure they knew what they were doing, and are asked one more time to make sure.
		elif x=='n':
			print_white(" Are you sure?")
			while True:
				print_yellow(" [Y]es    [N]o\n")
				x = input(' >>> ').lower()
				print()
				if x!='y' and x!='n':
					invalid()

				elif x=='y':
					new_game_break = True
					tutorial(stat)
					player_select(stat)
					story()
					break

				else:
					break

		# Load Game
		# THe player will load from the save file, titled "save_state.txt".
		# It is encoded in base64, so they can't just change their stats if they want to.
		# As such, the program has to pull the string, convert it to bytes, decode the bytes, and convert it back into a list of strings.
		elif x=='l':
			save_state = Path('save_state.txt')
			save = str(base64.decodebytes(save_state.read_text().encode('utf-8')).decode())
			save = save.split(", ")

			stat['p_name'] = str(save[0])
			stat['p_class'] = str(save[1])
			stat['p_LV'] = int(save[2])
			stat['ATT'] = int(save[3])
			stat['ATT_type'] = str(save[4])
			stat['p_DEF'] = int(save[5])
			stat['current_HP'] = int(save[6])
			stat['base_HP'] = int(save[7])
			stat['current_exp'] = int(save[8])
			stat['next_level_exp'] = int(save[9])
			stat['potions'] = int(save[10])
			stat['p_G'] = int(save[11])
			stat['quest'] = int(save[12])
			stat['magic_weapon'] = str(save[13])
			stat['mwc'] = save[14] == 'True'
			stat['magic_weaponer'] = str(save[15])
			stat['magic_item_type'] = str(save[16])
			stat['magic_item'] = int(save[17])
			stat['shield'] = save[18] == 'True'
			stat['rathat'] = save[19] == 'True'
			stat['shopbro'] = int(save[20])
			stat['p_left'] = int(save[21])
			stat['fairies'] = int(save[22])
			stat['inn'] = int(save[23])
			stat['orc'] = save[24] == 'True'
			stat['user'] = str(save[25])
			break

		else:
			sys.exit(0)

		if new_game_break == True: break


# If the player has never played before, this runs the three introduction functions.
else:
	sleep(1)
	tutorial(stat)
	player_select(stat)
	story()


# The main body of the program is stored in another function, called town in the town.py file.
town(stat, e_stat)

# Once the player has beaten the orc, town return the control back to here, to end the game.
os.system('clear')
print()
if stat['current_HP'] < (stat['base_HP']/4):
	print_white(" After a close battle, you've defeated the orc!")
	sleep(2)
else:
	print_white(" At long last, the village is free from its enemy.")
	sleep(2)

print_white(" When you return with the news, you are showered with gratitude.")
sleep(3)
print_white(" A big party is put on in your honor!")
sleep(2)
print_white(" Afterwards, you fall asleep in the inn, perhaps for the last time.")
sleep(3)
print("\n Z",end=""), sleep(.8), print("z",end=""), sleep(.8), print("z",end=""), sleep(.8), print(".",end=""), sleep(.8), print(".",end=""), sleep(.8), print(".\n\n",end=""), sleep(1.2)
print_white(" Upon waking up, you decide to say some final goodbyes before leaving.\n")
sleep(2.75)

# The player is given the option to talk to some, all, or none of the important villagers they've met to say some final goodbyes.
shopkeep = False
innkeep = False
weaponer = False
w = stat['magic_weaponer']
while True:
	if shopkeep == False: print_yellow(" [S]hopkeep")
	else: print(" [S]hopkeep", end="")

	if innkeep == False: print_yellow("    [I]nnkeep")
	else: print("    [I]nnkeep", end="")

	if weaponer == False: print_yellow("    ["+w[0]+']'+w[1:])
	else: print("    ["+w[0]+']'+w[1:], end="")

	print_yellow("    [L]eave\n")
	x = input(' >>> ').lower()
	print()
	if x!='s' and x!='i' and x!=w[0].lower() and x!='l':
		invalid()


	elif x=='s':
		if shopkeep == False:
			shopkeep = True
			print_cyan(" Gotta say, you've been one fine customer, "+stat['p_name']+".\n")
			sleep(3)
			print_cyan(" We'll all forever be in you're gratitude.\n")
			sleep(3)

			if stat['shopbro'] == 1 or stat['shopbro'] == 3:
				print_cyan("\n Me especially, the handsomer brother.\n")
				sleep(2.75)
				print_cyan(" We both know I'm more handsome.\n")
				sleep(2)
				print_cyan(" No, I clearly am.\n")
				sleep(2)
				print_cyan(" Nu uh!\n")
				sleep(1)
				print_cyan(" Ya huh!\n")
				sleep(1)
				print_cyan(" Nu uh!\n")
				sleep(1)
				print_cyan(" Ya huh!\n")
				sleep(1)
				while True:
					print_cyan(" Nu uh!\n")
					sleep(1)
					print_yellow(' [G]uys!\n')
					x = input(' >>> ').lower()
					print()
					if x=='g':
						break
					print_cyan(" Ya huh!\n")
					sleep(1)
					print_yellow(' [G]uys!\n')
					x = input(' >>> ').lower()
					print()
					if x=='g':
						break
				print_cyan(" Sorry.") 
			print_cyan(" Thanks again for everything. Don't be a stranger!\n\n")
			sleep(4)

		else:
			print_white(" You've already said your goodbyes to the Shopkeep.\n")
			sleep(1)


	elif x=='i':
		if innkeep == False:

			innkeep = True
			print_green(" Thanks for everything, "+stat['p_name']+"!\n")
			sleep(2.5)
			print_green(" Hey, did you ever find those fairies?\n")
			while True:
				print_yellow(" [I] did!    [N]ope, never.\n")
				x = input(' >>> ').lower()
				print()
				if x!='i' and x!='n':
					invalid()

				elif x=='i':
					print_green(" Really? I guess my dad really was telling the truth.\n")
					sleep(2)
					print_green(" I've been thinking about going out on my own adventure to look for\n")
					print_green(" them myself.\n")
					sleep(4.5)
					print_green(" Now that I know they're out there, I want to see them with my own eyes.\n")
					sleep(4)
					break

				else:
					print_green(" Well, I still hold out hope they're out there.\n")
					sleep(3)
					print_green(" I've actually been preparing for my own excursion into the forest.\n")
					sleep(3)
					print_green(" Now that the orc's gone, I want to try to find those fairies myself.\n")
					sleep(3)
					print_green(" You've inspired me to go out and prove my father's tale was true.\n")
					sleep(3)

					break

			print_green(" Anyways, if you ever find yourself in the neighborhood, let me put\n")
			print_green(" you up for the night!\n\n")
			sleep(4)

		else:
			print_white(" You've already said your goodbyes to the Innkeep.\n")
			sleep(1)


	elif x==w[0].lower():
		if weaponer == False:
			weaponer = True
			print_magenta(" Welcome back, "+stat['p_name']+"!\n")
			sleep(2)
			print_magenta(" Last night was some party, huh?\n")
			sleep(2)
			if stat['mwc'] == True:
				if stat['magic_weapon'] == "Vorpal Daggers": print_magenta(" Listen, I've been thinking, and I think I have a theory on how to make\n those")
				else: print_magenta(" Listen, I've been thinking, and I think I have a theory on how to make\n that")
				print_magenta(" "+stat['magic_weapon']+" even better.\n")
				sleep(4.5)
				print_magenta(" I'll need a lot more time to research about it, though.\n")
				sleep(3)
				print_magenta(" Come back in a few years, and I know I'll have something good!\n\n")
				sleep(3)
			else:
				print_magenta(" I'm still working on figuring out that new weapon.\n")
				sleep(3)
				print_magenta(" If you ever find youself back here, drop on by.\n")
				sleep(3)
				print_magenta(" It might finally be done then!\n\n")
				sleep(3)
			
		else:
			print_white(" You've already said your goodbyes to the ", w, ".\n")
			sleep(1)


	else:
		if innkeep == False and shopkeep == False and weaponer == False:
			print_white(" Deciding not to trouble the villagers any longer,", stat['p_name'], "suits up and")
			print_white(" heads off for the next adventure!")
		else:
			print_white(" Having said their final goodbyes, the villagers wave as", stat['p_name'], "heads on")
			print_white(" to the next adventure!")
		
		break

print("\n ------------------------------------------------------------------------\n")
sleep(6)


# If this is the second, third, or nth time playing the game, this dialogue directly from me will play.
if Path('Hall of Fame.txt').exists():
	print_white(" Hey, it's Jeffrey again!")
	sleep(3)
	print_white(" I can't believe you cared so much that you'd play my game start to")
	print_white(" finish again.")
	sleep(5)
	print_white(" I don't really have anything special for you this time around.")
	sleep(4)
	print_white(" Oh! How about this?")
	sleep(1)

	# Here, I give the player a gold star with the graphics library.
	win = GraphWin("Star", 1000, 1000)
	win.setBackground('grey')
	win.setCoords(-3.0, -3.0, 3.0, 3.0)

	p1 = Point(0, 2.618)
	p2 = Point(0.5878, 0.809)
	p3 = Point(2.4899, 0.809)
	p4 = Point(0.9511, -0.309)
	p5 = Point(1.5388, -2.118)
	p6 = Point(0, -1)
	p7 = Point(-1.5388, -2.118)
	p8 = Point(-0.9511, -0.309)
	p9 = Point(-2.4899, 0.809)
	p10 = Point(-0.5878, 0.809)

	star = Polygon(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)
	star.setWidth(5)
	star.setFill('yellow')
	star.draw(win)
	
	print_white(" It's a gold star for your efforts!")
	sleep(3)
	print_white(" I hope it made this all worthwhile.")
	sleep(3)
	print("\n .", end=''), sleep(1.5), print(".", end=''), sleep(1.5), print(".\n\n", end=''), sleep(1.5)
	print_white(" So... when I said to go out on your own adventure, I didn't mean to")
	print_white(" just start a new game.")
	sleep(4)
	print_white(" Go out and DO something.")
	sleep(2)
	print_white(" Personally, as a Boy Scout, I recommend camping.")
	sleep(3)
	print_white(" Get some friends to go with you, and it can be a great experience.")
	sleep(3.5)
	print_white(" What are you waiting for?")
	sleep(3)
	print_white(" The world is an oyster, and it's your job to crack it open!")
	sleep(5)


# If this is the first time the player has beaten the game, this dialogue from me will play.
else:
	print_white(" Thanks for playing this game, ", stat['user'], ".")
	sleep(4)
	print_white(" I'm the creator, Jeffrey.")
	sleep(2)
	print_white(" Making this game has been a real experience for me, and I'm so happy I")
	print_white(" got to share it with you.")
	sleep(5)
	print_white(" This started out as a small project for one of my classes, and spiraled")
	print_white(" WAY out of control!")
	sleep(5)
	print_white(" I just want to thank you for taking the time to play all of it.")
	sleep(3.75)
	print_white(" If you want to dive into the code, I have a ton of comments that make up")
	print_white(" a running commentary of my experiences.")
	sleep(6)
	print_white(" Oh, and before I forget, in the folder this is contained in, there'll be")
	print_white(" a file that contains ", stat['p_name'], "'s stats after beating the orc.")
	sleep(6)
	print_white(""" It's in 'Hall of Fame.txt' """)
	sleep(4)
	print_white(" There,", stat['p_name'], "will be immortalized, for as long as this folder")
	print_white(" exists and you don't go changing it.")
	sleep(5)
	print_white(" Anyways, this is truly good bye.")
	sleep(3)
	print_white(" I hope you have a wonderful rest of the day, as you head on to you're")
	print_white(" own next adventure!")
	sleep(5.5)

# When the player beats the game for the first time, a file titled "Hall of Fame.txt" is created that saves the character data.
# All the stats as of the end of the orc battle, like potions and whatnot, are saved.
# It is opened with 'a' so the previous wins are not overwritten.
halloffame = open(Path('Hall of Fame.txt'),'a')


while len(stat['p_name']) <8:
    stat['p_name'] = stat['p_name']+" "

y = "Lv. "+str(stat['p_LV'])
while len(y)<6:
	y = " "+y

z = stat['p_class']
while len(z)<15:
	z = z+" "
	if len(z)<15:
		z = " "+z

a = str(stat['current_exp'])+"/"+str(stat['next_level_exp'])
while len(a) <5:
    a = " "+a
b = str(stat['current_HP'])+"/"+str(stat['base_HP'])
while len(b) <5:
    b = " "+b
c = str(stat['p_DEF'])
while len(c) <2:
    c = " "+c
d = str(stat['potions'])
if len(d) <2:
    d = " "+d
e = str(stat['p_G'])
if len(e) <2:
    e = " "+e
    
if stat['magic_weapon'] == 'Damascus Sword': f =" Dam. Sword: "
elif stat['magic_weapon'] == "Warlock Staff": f =" War. Staff: "
else: f = " V. Daggers: "

if stat['mwc'] == True: g = "X"
else: g = "-"

if stat['shield'] == True: h = "X"
else: h = "-"

if stat['rathat'] == True: i = "X"
else: i = "-"

if stat['shopbro'] == 1 or stat['shopbro'] == 3: j = "X"
else: j = "-"

if stat['fairies'] > 1: k = "X"
else: k = "-"

halloffame.write(
"  _________________________________________________________\n"+
" |                                                         |\n"+
" |  "+stat['p_name']+" "+y+"    Inventory"+"         Side Quests       |"+
"\n |  ---------------    --------------    ----------------- |"+
"\n |  "+z+"    Potion:     "+d+"    Beat Reginald?  "+i+" |"+
"\n |  EXP:      "+a+"    Gold:       "+e+"    Saved Daniel?   "+j+" |"+
"\n |  HP:       "+b+"    "+str(stat['magic_item_type'])+":	    "+str(stat['magic_item'])+"    Found Fairies?  "+k+" |"+
"\n |  ATT:         "+str(stat['ATT'])+"   "+f+" "+g+"                      |"+
"\n |  DEF:         "+c+"    Shield:      "+h+"                      |"+
"\n |_________________________________________________________|\n\n")

stat['p_name'] = stat['p_name'].replace(" ", "")
halloffame.close()

# After everything, the old save file is deleted so the player can start a new game.
# Since "Hall of Fame.txt" now exists, the player can skip the tutorial and go straight into character creation.
try:
	os.remove(Path('save_state.txt'))

except FileNotFoundError:
	pass