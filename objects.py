# objects.py
from math import exp, inf
from graphics import *
from time import sleep
from random import randint
from pathlib import Path
import base64

MAPS = Path(__file__).parent.absolute() / "maps"
OVERLAYS = MAPS / "overlays"


class Player:
	def __init__(self, name, character_class, lv, ATT, DEF, current_HP, base_HP, current_EXP, next_EXP, gold, 
		items={"Shield": 0, "Potions": 0, "Apples": 0, "Herbs:": 0, "magic_item": 0,
				"Fire Scroll": 0, "Thunder Scroll": 0, "Ice Scroll": 0}
	):
		self.name = name
		self.character_class = character_class
		self.lv = lv
		self.ATT = ATT
		self.DEF = DEF
		self.current_HP = current_HP
		self.base_HP = base_HP
		self.current_EXP = current_EXP
		self.next_EXP = next_EXP
		self.gold = gold
		self.items = items

	def print_player(self):
		print(f"""
Name:	{self.name}
Class:	{self.character_class}
Level:	{self.lv}
ATT:	{self.ATT}
DEF:	{self.DEF}
HP:	{self.current_HP}/{self.base_HP}
EXP:	{self.current_EXP}/{self.next_EXP}
Gold:	{self.gold}
Items:
{self.items}""")




class Enemy:

	def __init__(self, type, LV, HP, DEF, EXP, gold):
		self.type = type
		self.LV = LV
		self.HP = HP
		self.DEF = DEF
		self.EXP = EXP
		self.gold = gold


class GoldBox:
	def __init__(self, gold):
		self.gold = gold

		self.items = []
		self.items.append(Rectangle(Point(1, 2), Point(390, 45)))
		self.items[0].setFill(color_rgb(50, 50, 50))
		self.items[0].setWidth(3)

		self.items.append(Text(Point(11, 11), f"You currently have: {self.gold}G"))
		self.items[1].setAnchor("nw")
		self.items[1].setTextColor("yellow")


	def show(self):	
		for i in self.items:
			i.draw(gw)

	def update(self, gold):
		sleep(.3)
		self.gold = gold
		self.items[1].setText(f"You currently have: {self.gold}G")
		sleep(1)

	def hide(self):
		for i in self.items:
			i.undraw()


class Bar:

	def __init__(self, numerator, denominator, color, p1, p2):
		self.numerator = numerator
		self.denominator = denominator
		self.color = color
		self.p1 = p1
		self.p2 = p2

		self.length = p2.x - p1.x
		self.height = p2.y - p1.y
		self.center = Point(self.p1.x + (self.length / 2), self.p1.y + (self.height / 2))
		
		self.items = []

		self.items.append(Rectangle(p1, Point(self.p1.x + (self.length * self.numerator / self.denominator), self.p2.y)))
		self.items[0].setFill(self.color)
		self.items.append(Rectangle(p1, p2))
		self.items[1].setWidth(2)
		self.items.append(Text(self.center, f"{self.numerator}/{self.denominator}"))
		self.items[2].setAnchor("c")
		self.items[2].setSize(int(self.height - 8))
		


	def show(self):
		for i in self.items:
			i.draw(gw)

	def update(self, numerator, denominator):

		for i in self.items:
				i.undraw()

		self.numerator = numerator
		self.denominator = denominator

		self.items[0] = Rectangle(self.p1, Point(self.p1.x + (self.length * self.numerator / self.denominator), self.p2.y))
		self.items[0].setFill(self.color)
		self.items[0].setWidth(3)

		self.items[2].setText(f"{self.numerator}/{self.denominator}")

		for i in self.items:
			i.draw(gw)		


	def hide(self):
		for i in self.items:
			i.undraw()



player = Player("Fief", "Rogue", 5, 10, 15, 8, 20, 100, 200, 50, {
	"Shield": 1,
	"Potions": 3,
	"Apples": 3,
	"magic_item": 1,
	"Herbs": 4,
	"Fire Scroll": 3,
	"Thunder Scroll": 2,
	"Ice Scroll": 3
})

game_stats = {
	"magic_weapon_status": 0,
	'rathat': False,
	'shopbro': -1,
	'p_left': 0,
	'fairies': 0,
	'inn_stays': -1,
	'orc': "Alive",
	'user': 'None',
	"town_tutorial": True,
	"level_tutorial": True,
	"librarian": 0	
}

load_overlay = Image(Point(500, 250), OVERLAYS / "load_overlay.png")


# def mousemotion(evt):
# 	'''Callback for mouse motion in the GUI.'''
# 	if evt.widget.mouseX is not None and evt.widget.mouseY is not None:
# 		print("Mouse Clicked")
# 		evt.widget.mouseX = evt.x
# 		evt.widget.mouseY = evt.y


# def mouserelease(evt):
# 	'''Callback for releasing a mouse click.'''
# 	print("Mouse Released")
# 	evt.widget.mouseX = None
# 	evt.widget.mouseY = None

gw = GraphWin("Console Quest.py", 1000, 500)
gw.setBackground("black")
# gw.bind("<Motion>", mousemotion)
# gw.bind("<ButtonRelease-1>", mouserelease)


def dialogue(line, choices = [], color = "white", return_arg = False, right = False):

	# Initialize variables that will be used later.
	start = 500 if right else 0
	selection = 0
	


	# Create the dialogue box
	dialogue_box = Rectangle(Point(start + 11, 403), Point(start + 489, 488))
	dialogue_box.setFill(color_rgb(50, 50, 50))
	dialogue_box.setWidth(3)
	dialogue_box.draw(gw)

	# Create the Text object that will display dialogue.
	dialogue_text = Text(Point(start + 25, 418), "") 
	dialogue_text.setTextColor(color)
	dialogue_text.setSize(20)
	dialogue_text.setAnchor("nw")
	dialogue_text.draw(gw)

	

	question = ""
	line_length = 0
	line = line.split()
	for i in line:
		len_i = len(i)
		if line_length + len_i + 1 > 29:
			question += f"\n{i} "
			line_length = len_i + 1
		else:
			question += f"{i} "
			line_length += len_i + 1

	# Gradually print text to the dialogue box.
	overflow = 0
	skip = False
	for i in range(len(question)):

		key = gw.checkKey().lower()
		if key in ["return", "space", "escape"]:
			skip = True

		if question[i] == "\n":
			overflow += 1
		if overflow >= 2:
			dialogue_text.setText(dialogue_text.getText()[dialogue_text.getText().index("\n") + 1:])
			overflow = 1
		dialogue_text.setText(dialogue_text.getText() + question[i])
		if not skip:
			sleep(.02)


	


	# If the array of choices that is passed in isn't empty, the player is supposed to make a
	#	 selection.
	length_choices = len(choices)
	center = 374 - (30 * (length_choices - 1))
	selector = Polygon(Point(start + 478, center - 6), Point(start + 478, center + 6), Point(start + 461, center))
	selector.setFill("red")

	if length_choices > 0:
		answer = ""
		longest_answer = 0
		for i in choices:
			answer += f"{i}\n"
			longest_answer = max(longest_answer, len(i))
		answer = answer[:-1]

		choice_box = Rectangle(Point(start + 473 - (16 * (longest_answer + 2)), 382 - (30 * length_choices)), Point(start + 489, 395))
		choice_box.setFill(color_rgb(50, 50, 50))
		choice_box.setWidth(3)
		choice_box.draw(gw)


		choice_text = Text(Point(start + 453, 390), "")
		choice_text.setAnchor("se")
		choice_text.setJustification("right")
		choice_text.setSize(20)
		choice_text.draw(gw)

		

		choice_text.setText(answer)
		selector.draw(gw)

		
	while True:
		key = gw.checkKey().lower()

		if key != "":
			if key in ["space", "return"]:
				break

			elif key in ["escape"]:
				while selection < length_choices - 1:
					selector.move(0, 30)
					selection += 1

			elif key in ["m", "shift_l"]:
				pause_menu(not right)


			elif length_choices > 0:
				if key in ["up", "w", "left", "a"]:
					selection = (selection - 1) % length_choices
					if selection != length_choices - 1:
						selector.move(0, -30)
					else:
						selector.move(0, 30 * (length_choices - 1))


				elif key in ["down", "s", "right", "d"]:
					selection = (selection + 1) % length_choices
					if selection != 0:
						selector.move(0, 30)
					else:
						selector.move(0, -30 * (length_choices - 1))



		

	if length_choices == 0:	on_gw = 2
	else: on_gw = 5
	for i in range(on_gw):
		gw.items[-1].undraw()

	if length_choices == 0: return -1
	elif return_arg == True: return choices[selection].split(":")[0]
	else: return selection
	
def selling(item, cost):
	pass


def inventory():
	string = ""

	# Because the items are stored in a dictionary, to display all the player's items we need to run through all possible items step by step.
	if game_stats["magic_weapon_status"] == 4:
		weapon = "Storm Blade" if player.character_class == "Warrior" else "Blaze Rod" if player.character_class == "Sorcerer" else "Vorpal Daggers"
		string += weapon + "\t "
	if player.items["Shield"] != 0:
		string += "Shield"
	if string != "": string += "\n"

	if player.items["Potions"] != 0:
		string += f"Potions: {str(player.items['Potions']).rjust(6)}  "
	if player.items["Apples"] != 0:
		string += f"Apples: {str(player.items['Apples']).rjust(8)}"
	if string.count("Potions") != 0 or string.count("Apples") != 0:
		string += "\n"

	if player.items["magic_item"] != 0:
		string += f'{"Magic Wood" if player.character_class == "Warrior" else "Magic Ore"}: {str(player.items["magic_item"]).rjust(4)}  '
	if player.items["Herbs"] != 0:
		string += f"Herbs: {str(player.items['Herbs']).rjust(9)}"
	if string.count("Magic") != 0 or string.count("Herbs") != 0:
		string += "\n"


	if player.items["Fire Scroll"] != 0:
		string += f"Fire Scrolls: {str(player.items['Fire Scroll']).rjust(19)}\n"
	if player.items["Ice Scroll"] != 0:
		string += f"Ice Scrolls: {str(player.items['Ice Scroll']).rjust(20)}\n"
	if player.items["Thunder Scroll"] != 0:
		string += f"Thunder Scrolls: {str(player.items['Thunder Scroll']).rjust(16)}\n"

	return string


def pause_menu(right):

	start = 500 if right else 0
	prior = len(gw.items)

	pause_overlay = Image(Point(500, 250), MAPS / "overlays" / "pause_overlay.png")
	pause_overlay.draw(gw)


	# Everything for the Character Information
	info_box = Rectangle(Point(551 - start, 100), Point(959 - start, 400))
	info_box.setFill(color_rgb(50, 50, 50))
	info_box.setWidth(3)
	info_box.draw(gw)

	# The Character Icon
	info_icon = Image(Point(613 - start, 163), MAPS / "characters" / f"{player.character_class}_portrait.png")
	info_icon.draw(gw)

	# Shows the Header that includes the player's name and level.
	info_header = Text(Point(572 - start, 179))
	info_header.setAnchor("w")
	info_header.setSize(22)
	info_header.setText(f"      {player.name + f'LV: {player.lv}'.rjust(16)[len(player.name):]}\n      HP:\n      EXP:\nItems:")
	info_header.draw(gw)

	# Draw the HP bar.
	hp_bar = Bar(player.current_HP, player.base_HP, "red", Point(750 - start, 149), Point(948 - start, 173))
	hp_bar.show()


	# Draws the EXP bar
	exp_bar = Bar(player.current_EXP, player.next_EXP, "green", Point(750 - start, 179), Point(948 - start, 203))
	exp_bar.show()

	# Lists off the player's current inventory.
	info_header_underline = Line(Point(573 - start, 240), Point(937 - start, 240))
	info_header_underline.setWidth(1)
	info_header_underline.setOutline("white")
	info_header_underline.draw(gw)
	info_footer = Text(Point(573 - start, 246))
	info_footer.setAnchor("nw")
	info_footer.setSize(14)
	info_footer.setText(inventory())
	info_footer.draw(gw)

	
	# Lists off the pause menu options.
	choice_box = Rectangle(Point(start + 125, 165), Point(start + 370, 335))
	choice_box.setFill(color_rgb(50, 50, 50))
	choice_box.setWidth(3)
	choice_box.draw(gw)

	choice_text = Text(Point(start + 260, 250))
	choice_text.setAnchor("c")
	choice_text.setSize(20)
	choice_text.setText("Resume\nDrink Potion\nEat Apple\nSave Game\nQuit Game")
	choice_text.draw(gw)
	

	selector = Polygon(Point(start + 137, 183), Point(start + 137, 195), Point(start + 154, 189))
	selector.setFill("red")
	selector.draw(gw)

	selection = 0
	saved = False

	while True:
		
		while True:
			key = gw.checkKey().lower()

			if key != "":
				if key in ["space"]:
					break

				elif key in ["escape"]:
					while selection > 0:
						selector.move(0, -30)
						selection -= 1


				if key in ["up", "w", "left", "a"]:
					selection = (selection - 1) % 5
					if selection != 4:
						selector.move(0, -30)
					else:
						selector.move(0, 120)


				elif key in ["down", "s", "right", "d"]:
					selection = (selection + 1) % 5
					if selection != 0:
						selector.move(0, 30)
					else:
						selector.move(0, -120)

		# Resume Game
		if selection == 0:
			for i in gw.items[prior:]: i.undraw()
			return

		# Drink Potion
		if selection == 1:
			if player.items["Potions"] == 0:
				dialogue("You have no more potions to drink.", right=right)
			elif player.current_HP == player.base_HP:
				dialogue("You are already at max HP", right=right)
			else:
				player.items["Potions"] -= 1
				player.current_HP += round(randint(4, 10) * 4.2)
				if player.current_HP > player.base_HP:
					player.current_HP = player.base_HP
				hp_bar.update(player.current_HP, player.base_HP)

		# Eat Apple
		if selection == 2:
			if player.items["Apples"] == 0:
				dialogue("You have no more apples to eat.", right=right)
			elif player.current_HP == player.base_HP:
				dialogue("You are already at max HP", right=right)
			else:
				player.items["Apples"] -= 1
				player.current_HP += randint(1, 4)
				if player.current_HP > player.base_HP:
					player.current_HP = player.base_HP
				hp_bar.update(player.current_HP, player.base_HP)

		# Save Game
		if selection == 3:
			saved = True
			save_state = open(Path(__file__).parent.absolute() / "save_state.txt", "w")  
			
			stats_to_save = [player.name, player.character_class, player.lv, player.ATT, player.DEF, 
				player.current_HP, player.base_HP, player.current_EXP, player.next_EXP, player.gold, 
				player.items, game_stats
			]

			line_to_save = ''
			for i in stats_to_save:
				line_to_save = line_to_save + str(i) + "\n"
			
			# print(line_to_save)
			# save_state.write(str(line_to_save[:-1]))
			save_state.write(str(base64.standard_b64encode(line_to_save[:-1].encode('utf-8')))[2:-1])

			dialogue("Game saved.", right=right)

		# Quit Game
		if selection == 4:


			# If prior is > 1000, than the player is trying to quit in the forest.
			# If that is the case, play this warning.
			if prior > 1000:
				dialogue("You are not in the town. If you quit, it will be as though you died.")

			# If the player hasn't saved recently, play this warning.
			# If the previous line of dialogue triggered, add an "also" for grammar.
			if not saved:
				dialogue(f"You{' also' if prior > 1000 else ''} have not saved recently.")

			if dialogue("Are you sure you want to quit?", ["Yes", "No"], right=right) == 0:
				exit()

		info_footer.setText(inventory())


if __name__ == "__main__":

	gw.setBackground("gray")

	# name, character_class, lv, ATT, DEF, current_HP, base_HP, current_EXP, next_EXP, gold, items
	

	game_stats["magic_weapon_status"] = 4


	pause_menu(True)
	gw.getKey()
	# print(dialogue("This is for testing the left-side dialogue box.", ["Hello", "Selection 2", "Test 3"], "green"))
	# print(dialogue("This is supposed to be a line of dialogue that is not one, not two, but four lines long!"))
	# dialogue("-------- max length -------- -------- max length --------")
	# print(dialogue("This is for testing the right-side dialogue box.", ["----", "Text", "More Text", "Something New", "Suuuuper Long Text", "Shorter Text", "Option 6"], right=True))
