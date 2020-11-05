# map.py

from pathlib import Path
from graphics import *
from level_creation_tool import fetch_level
from time import sleep
from objects import *
from random import seed
from random import choice
from PIL import Image as PIL_Image


MAPS = Path(__file__).parent.absolute() / "maps"
OVERLAYS = MAPS / "overlays"
SPRITES = MAPS / "sprites"
FOLDER = "forest"
CHARACTERS = MAPS / "characters"


class Player_Icon:
	def __init__(self, level, level_x, level_y, map, map_x, map_y):
		self.level = level
		self.level_x = level_x
		self.level_y = level_y
		self.map = map
		self.map_x = map_x
		self.map_y = map_y

		self.idx = 0
		self.facing = "right"
		cc = player.character_class
		self.up = [Image(Point(250, 250), CHARACTERS / f"{cc}_up_0.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_up_1.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_up_2.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_up_3.png")]
		self.down = [Image(Point(250, 250), CHARACTERS / f"{cc}_down_0.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_down_1.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_down_2.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_down_3.png")]
		self.left = [Image(Point(250, 250), CHARACTERS / f"{cc}_left_0.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_left_1.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_left_2.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_left_3.png")]
		self.right = [Image(Point(250, 250), CHARACTERS / f"{cc}_right_0.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_right_1.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_right_2.png"), Image(Point(250, 250), CHARACTERS / f"{cc}_right_3.png")]
		self.sprite = self.right[0]
		self.sprite.draw(gw)
		

	def turn_up(self):
		if self.facing == "up": self.idx = (self.idx + 1) % 4
		else: self.facing, self.idx = "up", 1
		self.sprite.undraw()
		self.sprite = self.up[self.idx]
		self.sprite.draw(gw)
	def move_up(self, amt=1):
		self.level.move(0, 48 * amt)
		self.level_y -= 1 * amt
		self.map.move(0, -15 * amt)
		self.map_y -= 1 * amt
		
		
	def turn_down(self):
		if self.facing == "down": self.idx = (self.idx + 1) % 4
		else: self.facing, self.idx = "down", 1
		self.sprite.undraw()
		self.sprite = self.down[self.idx]
		self.sprite.draw(gw)
	def move_down(self, amt=1):
		self.level.move(0, -48 * amt)
		self.level_y += 1 * amt
		self.map.move(0, 15 * amt)
		self.map_y += 1 * amt


	def turn_left(self):
		if self.facing == "left": self.idx = (self.idx + 1) % 4
		else: self.facing, self.idx = "left", 1
		self.sprite.undraw()
		self.sprite = self.left[self.idx]
		self.sprite.draw(gw)
	def move_left(self, amt=1):
		self.level.move(48 * amt, 0)
		self.level_x -= 1 * amt
		self.map.move(-15 * amt, 0)
		self.map_x -= 1 * amt


	def turn_right(self):
		if self.facing == "right": self.idx = (self.idx + 1) % 4
		else: self.facing, self.idx = "right", 1
		self.sprite.undraw()
		self.sprite = self.right[self.idx]
		self.sprite.draw(gw)
	def move_right(self, amt=1):
		self.level.move(-48 * amt, 0)
		self.level_x += 1 * amt
		self.map.move(15 * amt, 0)
		self.map_x += 1 * amt


# This method is used to swap images on gw.
# It is used primarily to swap the map icons.
# 	new_image is the Image() object you will be replacing with.
# 	old_image is the index of gw that you will be replacing.
def swap_image(new_image, old_image):
	icon = gw.items[old_image].clone()
	gw.items[old_image].undraw()
	icon = Image(icon.anchor, new_image)
	icon.draw(gw)
	gw.items.insert(old_image, icon)
	gw.items = gw.items[:-1]


# This method is called every time the player tries to draw on the map.
# 	prior is the number of items that were on gw before exploring() was called.
# 	map_layout is the array that stores what the player's map looks like.
# 	item_id is the index of the index of the map tile that will be changed.
# 	setting is the type of change that will occur.
def change_map(prior, map_layout, item_id, setting):

	# Increment item_id so that when we shift around things on the GraphWin, we grab the right objects.
	item_id += 2 + prior

	# If we are manipulating icons, increment again because the player's icons are in-between the tile and
	#     icon layer.
	if setting not in ["g", "b", "o", "y", "erase_color"]:
		item_id += 1

	# Color the tile:
	if setting == "g":
		gw.items[item_id].setFill(color_rgb(80, 192, 146))
	elif setting == "b":
		gw.items[item_id].setFill(color_rgb(100, 164, 203))
	elif setting == "o":
		gw.items[item_id].setFill(color_rgb(246, 147, 28))
	elif setting == "y":
		gw.items[item_id].setFill(color_rgb(255, 217, 102))
	elif setting == "erase_color":
		gw.items[item_id].setFill("")

	# Change the tile's icon.
	elif setting == "erase_icon":
		swap_image(OVERLAYS / "null_icon.png", item_id)
	elif setting == "s":
		swap_image(OVERLAYS / "star_icon.png", item_id)
	elif setting == "i":
		swap_image(OVERLAYS / "important_icon.png", item_id)
	elif setting == "|":
		swap_image(OVERLAYS / "stairs_up_icon.png", item_id)
	elif setting == "/":
		swap_image(OVERLAYS / "stairs_down_icon.png", item_id)
	elif setting == "u":
		swap_image(OVERLAYS / "up_icon.png", item_id)
	elif setting == "d":
		swap_image(OVERLAYS / "down_icon.png", item_id)
	elif setting == "l":
		swap_image(OVERLAYS / "left_icon.png", item_id)
	elif setting == "r":
		swap_image(OVERLAYS / "right_icon.png", item_id)
	elif setting == "1":
		swap_image(OVERLAYS / "1_icon.png", item_id)
	elif setting == "2":
		swap_image(OVERLAYS / "2_icon.png", item_id)
	elif setting == "3":
		swap_image(OVERLAYS / "3_icon.png", item_id)
	elif setting == "4":
		swap_image(OVERLAYS / "4_icon.png", item_id)
	elif setting == "5":
		swap_image(OVERLAYS / "5_icon.png", item_id)
	elif setting == "6":
		swap_image(OVERLAYS / "6_icon.png", item_id)
	elif setting == "7":
		swap_image(OVERLAYS / "7_icon.png", item_id)
	elif setting == "8":
		swap_image(OVERLAYS / "8_icon.png", item_id)
	elif setting == "9":
		swap_image(OVERLAYS / "9_icon.png", item_id)
	elif setting == "0":
		swap_image(OVERLAYS / "0_icon.png", item_id)

	# Decrement item_id so that when we change the indexed location in map_layout we change the right spot.
	item_id -= 2 + prior

	# Similar to the above increment, decrement again if we are manipulating the icons.
	if setting not in ["g", "b", "o", "y", "erase_color"]:
		item_id -= 1

	# Change the indexed location in map_layout to the new setting.
	if setting == "erase_color" or setting == "erase_icon":
		map_layout[item_id // 30][item_id % 30] = "."
	else:
		map_layout[item_id // 30][item_id % 30] = setting


# This is the main method of the file.
# It is called every time the player enters or changes levels in the forest.
# 	level_num is the numbered level that the player will explore.
# 	higher determines whether the player is heading up or down the forest.
#   	If higher is True, they are heading up, False means they are heading down.
def exploring(level_num, higher=True):

	# Keep track of how many items are on gw before we start drawing new things.
	prior = len(gw.items)

	# Draw a black "mask" that will be placed over the screen to simulate loading.
	load_overlay.draw(gw)
	# gw.autoflush = False

	# Update the global FOLDER to the biome type depending on the level_num.
	# This will tell the code which folder in SPRITES it should look into.
	global FOLDER
	if level_num < 6: FOLDER = "forest"
	elif level_num < 11: FOLDER = "swamp"
	else: FOLDER = "mountain"

	# If the player is waiting for the Weapon Maker to finish their weapon, coming to the forest is a valid way to stall for time.
	if game_stats["magic_weapon_status"] == 2: game_stats["magic_weapon_status"] = 3

	# Both rect and map_setting will be used later
	rect = Rectangle(Point(0, 0), Point(0, 0))
	map_setting = None

	# Using the fetch_level method from level_creation_tool.py, we get the level and save the coordinates of the starting stairs.
	level_layout, map_layout, level_x, level_y = fetch_level(level_num, higher)
	map_x, map_y = level_x - 1, level_y - 1
	level_width, level_height = len(level_layout[0]), len(level_layout)
		

	# Read in the level image and save it as the background layer.
	level_background = Image(Point(249 + (48 * ((level_width // 2) - (level_x))), 259 + (48 * ((level_height // 2) - (level_y)))), (MAPS / f"level_{level_num}.png"))

	# We need to move it to slightly different places depending on the parity of level_x and level_y.
	# By default it is loaded into the position when level_width and level_height are odd, so check everything else:
	if level_width % 2 != 0:
		# If level_width is odd but level_height is even:
		if level_height % 2 == 0:
			level_background.move(0, -24)
	else:
		# If level_width is even but level_height is odd:
		if level_height % 2 != 0:
			level_background.move(-24, 0)
		# If both level_width and level_height are even:
		else:
			level_background.move(-25, -24)
	level_background.draw(gw)
	level_background.lower()

	# Draw in the background for the map.
	map_background = Image(Point(750, 250), OVERLAYS / "map_background.png")
	map_background.draw(gw)
	map_background.lower()

	# Draw the tiles for the map.
	# Simulaneously draw in their colors.
	for i in range(25):
		for j in range(30):
			tile_x, tile_y = (j * 15) + 536, (i * 15) + 35
			map_tile = Rectangle(Point(tile_x, tile_y), Point(tile_x + 15, tile_y + 15))
			map_color = map_layout[i][j]
			map_tile.draw(gw)
			map_tile.lower()
			if map_color != ".":
				change_map(prior, map_layout, (i * 30) + j, map_color)



	# Draw in the player.
	# This happens now so that the icons will be in front of their sprite on the map screen.
	# On the level, they will be in the center of the screen, so we can use predetermined values 
	#     for x and y.
	# On the level, their location changes, so we have to actually calculate x and y values.
	tile_x, tile_y = (map_x * 15) + 536, (map_y * 15) + 35
	map_player = Image(Point(tile_x + 7, tile_y + 7), OVERLAYS / "pointer_up.png")
	map_player.draw(gw)
	map_player.lower()



	# Now draw the icons that sit on top of the tiles and the player's map sprite.
	for i in range(25):
		for j in range(30):
			icon_x, icon_y = (j * 15) + 544, (i * 15) + 43
			map_icon = Image(Point(icon_x, icon_y), OVERLAYS / "null_icon.png")
			map_color = map_layout[i + 25][j]
			map_icon.draw(gw)
			map_icon.lower()
			if map_color != ".":
				change_map(prior, map_layout, (i * 30) + j + 750, map_color)

	# Finally, put the overlay on top.
	overlay = Image(Point(754, 253), OVERLAYS / "map_overlay.png")
	overlay_num = Image(Point(523, 22), OVERLAYS / f"map_{level_num}_overlay.png")
	overlay.draw(gw)
	overlay.lower()
	overlay_num.draw(gw)
	overlay_num.lower()

	map_background.lower()
	level_background.lower()
	load_overlay.undraw()

	# gw.autoflush = True
	# global _root
	# _root.update()


	# Create the player as a Player object so we can keep track of where they are when they move around in the arrays.
	player_icon = Player_Icon(level_background, level_x, level_y, map_player, map_x, map_y)


	# When the player enters the dungeon for the first time, game_stats["level_tutorial"] is set to True.
	# This means they have not completed the tutorial, which should now happen.
	# Afterwards, we change it to False so it won't trigger again.
	if game_stats["level_tutorial"]:
		game_stats["level_tutorial"] = False
		map_tutorial()

	txt = Text(Point(250, 250))
	txt.draw(gw)

	

	# The game loop.
	while True:

		direction = gw.checkKey().lower()
		click = gw.checkMouse()

		# If the player clicked somewhere on the screen:
		if click:
			txt.setText(click)

			x, y = click.getX(), click.getY()

			# If the click was somewhere on the grid:
			if y < 411:

				x = (x - 537) // 15
				y = (y - 36) // 15
				square_id = int((y * 30) + x)

				# Change the map in accordance with the tool.
				if map_setting in ["g", "b", "o", "y", "erase_color"]:
					change_map(prior, map_layout, square_id, map_setting)
				else:
					change_map(prior, map_layout, square_id + 750, map_setting)


			# Else, if the click was on the lower palette:
			else:

				rect.undraw()

				# Tile Color Changer:
				if 513 <= x <= 549:
					if 435 <= y <= 455: map_setting, rect = "g", Rectangle(Point(516, 439), Point(546, 453))
					elif 456 <= y <= 476: map_setting, rect = "o", Rectangle(Point(516, 459), Point(546, 473))
				if 550 <= x <= 585:
					if 435 <= y <= 455: map_setting, rect = "b", Rectangle(Point(552, 439), Point(582, 453))
					elif 456 <= y <= 476: map_setting, rect = "y", Rectangle(Point(552, 459), Point(582, 473))

				# Trashcans:
				if 436 <= y <= 475:
					if 584 <= x <= 623: map_setting, rect = "erase_color", Rectangle(Point(588, 440), Point(619, 471))
					if 627 <= x <= 666: map_setting, rect = "erase_icon", Rectangle(Point(631, 440), Point(662, 471))

				# Upper Row of Placable Icons:
				if 423 <= y <= 457:
					if 663 <= x <= 702: map_setting, rect = "s", Rectangle(Point(667, 424), Point(698, 455))
					if 704 <= x <= 732: map_setting, rect = "i", Rectangle(Point(703, 424), Point(734, 455))
					if 737 <= x <= 776: map_setting, rect = "u", Rectangle(Point(740, 424), Point(771, 455))
					if 771 <= x <= 809: map_setting, rect = "d", Rectangle(Point(776, 424), Point(807, 455))
					if 810 <= x <= 845: map_setting, rect = "1", Rectangle(Point(812, 424), Point(843, 455))
					if 846 <= x <= 881: map_setting, rect = "2", Rectangle(Point(848, 424), Point(879, 455))
					if 882 <= x <= 917: map_setting, rect = "3", Rectangle(Point(884, 424), Point(915, 455))
					if 918 <= x <= 953: map_setting, rect = "4", Rectangle(Point(920, 424), Point(951, 455))
					if 954 <= x <= 990: map_setting, rect = "5", Rectangle(Point(956, 424), Point(987, 455))

				# Lower Row of Placeable Icons:
				if 458 <= y <= 495:
					if 663 <= x <= 702: map_setting, rect = "|", Rectangle(Point(667, 460), Point(698, 491))
					if 704 <= x <= 732: map_setting, rect = "/", Rectangle(Point(703, 460), Point(734, 491))
					if 737 <= x <= 775: map_setting, rect = "l", Rectangle(Point(740, 460), Point(771, 491))
					if 776 <= x <= 809: map_setting, rect = "r", Rectangle(Point(776, 460), Point(807, 491))
					if 810 <= x <= 845: map_setting, rect = "6", Rectangle(Point(812, 460), Point(843, 491))
					if 846 <= x <= 881: map_setting, rect = "7", Rectangle(Point(848, 460), Point(879, 491))
					if 882 <= x <= 917: map_setting, rect = "8", Rectangle(Point(884, 460), Point(915, 491))
					if 917 <= x <= 953: map_setting, rect = "9", Rectangle(Point(920, 460), Point(951, 491))
					if 954 <= x <= 990: map_setting, rect = "0", Rectangle(Point(956, 460), Point(987, 491))

				# Redraw the Rectangle rect to give the simulation of transformation.
				rect.setOutline(color_rgb(59, 204, 255))
				rect.setWidth(3)
				rect.draw(gw)

		# If any key was pressed:
		if direction != "":
			
			# If the key was for moving in a direction:
			if direction in ["up", "w"]:
				player_icon.turn_up()
				if level_layout[player_icon.level_y - 1][player_icon.level_x] in [".", "A", "B", "C", "D", "E", "/", "|"]:
					player_icon.move_up()
				sleep(.1)
				player_icon.turn_up()
			elif direction in ["down", "s"]:
				player_icon.turn_down()
				if level_layout[player_icon.level_y + 1][player_icon.level_x] in [".", "A", "B", "C", "D", "E", "/", "|"]:
					player_icon.move_down()
				sleep(.1)
				player_icon.turn_down()
			elif direction in ["left", "a"]:
				player_icon.turn_left()
				if level_layout[player_icon.level_y][player_icon.level_x - 1] in [".", "A", "B", "C", "D", "E", "/", "|"]:
					player_icon.move_left()
				sleep(.1)
				player_icon.turn_left()
			elif direction in ["right", "d"]:
				player_icon.turn_right()
				if level_layout[player_icon.level_y][player_icon.level_x + 1] in [".", "A", "B", "C", "D", "E", "/", "|"]:
					player_icon.move_right()
				sleep(.1)
				player_icon.turn_right()

			# If the player is trying to open the pause menu:
			elif direction in ["m", "shift_l"]:
				pause_menu(False)
			
			# If the player wants to use a scroll:
			elif direction in ["e"]:
				use_scroll(level_layout, level_num, prior, player, player_icon)

			# If the tile the sqare the player just moved to is not colored on their map:
			if map_layout[player_icon.map_y][player_icon.map_x] == ".":
				# Color the spot green
				change_map(prior, map_layout, (player_icon.map_y * 30) + player_icon.map_x, "g")

			# If the player is standing on a harvestable square:
			if level_layout[player_icon.level_y][player_icon.level_x] == "A":
				dialogue("Discovered some items!")
				level_layout[player_icon.level_y][player_icon.level_x] = choice(["C", "D", "E"])
				raw_background = PIL_Image.open(MAPS / f"level_{level_num}.png")
				flower = PIL_Image.open(SPRITES / FOLDER / "harvest0.png")
				raw_background.paste(flower, (player_icon.level_x * 48, player_icon.level_y * 48))
				raw_background.save(MAPS / f"level_{level_num}.png")
				swap_image(MAPS / f"level_{level_num}.png", prior)
				player_icon.level = gw.items[prior]
				gw.redraw()

			# If the player is standing on the square for the stairs down:
			elif level_layout[player_icon.level_y][player_icon.level_x] == "|":
				if dialogue("Would you like to continue on?", ["Yes", "No"]) == 0:
					save_and_close(level_num, level_layout, map_layout, prior)
					exploring(level_num + 1)
					break

			# Else if the player is standing on the square for the stairs up:
			elif level_layout[player_icon.level_y][player_icon.level_x] == "/":
				if level_num in [6, 11, 15]:
					if dialogue("Do you want to return to town?", ["Yes", "No"]) == 0:
						save_and_close(level_num, level_layout, map_layout, prior)
						return


				if dialogue("Would you like to head down?", ["Yes", "No"]) == 0:
					save_and_close(level_num, level_layout, map_layout, prior)
					if level_num == 1: return
					else: 
						exploring(level_num - 1, False)
						break

# This method is called when the player tries to use a scroll.
# It throws up a selection menu for which scroll the player wants to use, then removes that wall from the level and its background.
# 	level_layout is the array that stores the level
# 	level_num is the level number
# 	prior is the number of objects in the graphwin prior to drawing with explore()
# 	player is the player object
# 	player_icon is the icon of the player
def use_scroll(level_layout, level_num, prior, player, player_icon):

	scrolls = []
	facing, level_x, level_y = player_icon.facing, player_icon.level_x, player_icon.level_y
	level_background = PIL_Image.open(MAPS / f"level_{level_num}.png")


	weapon = "Use Storm Blade" if player.character_class == "Warrior" else "Use Blaze Rod" if player.character_class == "Sorcerer" else "Use Vorpal Daggers"
	if game_stats["magic_weapon_status"] == 4:
		scrolls.append(weapon)

	if player.items["Fire Scroll"] > 0:
		scrolls.append(f"Fire Scroll ({player.items['Fire Scroll']})")
	if player.items["Ice Scroll"] > 0:
		scrolls.append(f"Ice Scroll ({player.items['Ice Scroll']})")
	if player.items["Thunder Scroll"] > 0:
		scrolls.append(f"Thunder Scroll ({player.items['Thunder Scroll']})")

	scrolls.append("Cancel")

	x = dialogue("Which scroll do you want to use?", scrolls, return_arg=True)

	if x == "Cancel":
		return

	if x.count("Use") == 1:
		if x == "Use Storm Blade":
			for i in range(-1, 2):
				print()


		if x == "Use Blaze Rod":
			print("Blaze Rod")

		# Else, the player is using the Vorpal Daggers
		else:

			# x0 and y0 are the base coordinates, while x1 and y1 are how much they'll change by.
			x0, y0, x1, y1 = level_x, level_y, 0, 0
			if facing == "up" and level_layout[y0 - 1][x0] in ["W", "I"]:
				y1 = -1
			elif facing == "down" and level_layout[y0 + 1][x0] in ["W", "I"]:
				y1 = 1
			elif facing == "left" and level_layout[y0][x0 - 1] in ["W", "I"]:
				x1 = -1
			elif facing == "right" and level_layout[y0][x0 + 1] in ["W", "I"]:
				x1 = 1
			# If the player is not facing water or ice, this dialogue will play.
			else:
				dialogue("You are not facing water or ice.")
				return

			# If this is reached, the player is facing water or ice and is able to warp.
			# distance will be how far the player warps.
			distance = 0
			while True:
				x0, y0 = x0 + x1, y0 + y1
				if level_layout[y0][x0] in ["W", "I"]:
					distance += 1
				elif level_layout[y0][x0] in [".", "A", "B", "C", "D", "E"]:
					distance += 1
					break
				else:
					dialogue("There isn't enough space on the other side to warp.")
					return

			if facing == "up":
				player_icon.move_up(amt=distance)
			elif facing == "down":
				player_icon.move_down(amt=distance)
			elif facing == "left":
				player_icon.move_left(amt=distance)
			else:
				player_icon.move_right(amt=distance)

	
	else:

		if x.count("Fire") > 0:
			wall, line = "T", "are no trees"
			player.items["Fire Scroll"] -= 1
			paste = PIL_Image.open(SPRITES/ FOLDER / "stump.png")

		elif x.count("Ice") > 0:
			wall, line = "W", "is no water"
			player.items["Ice Scroll"] -= 1
			paste = PIL_Image.open(SPRITES/ FOLDER / "ice.png")

		else:
			wall, line = "R", "are no rocks"
			player.items["Thunder Scroll"] -= 1
			paste = PIL_Image.open(SPRITES/ FOLDER / "pebbles.png")

		if facing == "up" and level_layout[level_y - 1][level_x] == wall:
			level_layout[level_y - 1][level_x] = "."
			level_background.paste(paste, (level_x * 48, (level_y - 1) * 48))
		elif facing == "down" and level_layout[level_y + 1][level_x] == wall:
			level_layout[level_y + 1][level_x] = "."
			level_background.paste(paste, (level_x * 48, (level_y + 1) * 48))
		elif facing == "left" and level_layout[level_y][level_x - 1] == wall:
			level_layout[level_y][level_x - 1] = "."
			level_background.paste(paste, ((level_x - 1) * 48, level_y * 48))
		elif facing == "right" and level_layout[level_y][level_x + 1] == wall:
			level_layout[level_y][level_x + 1] = "."
			level_background.paste(paste, ((level_x + 1) * 48, level_y * 48))

		else:
			if wall != "T": player.items["Fire Scroll"] += 1
			elif wall != "W": player.items["Ice Scroll"] += 1
			else: player.items["Thunder Scroll"] += 1
			dialogue(f"There {line} there.")
			return
			
		
		level_background.save(MAPS / f"level_{level_num}.png")
		level_background = Image(gw.items[prior].anchor, MAPS / f"level_{level_num}.png")
		swap_image(level_background, prior)
		player_icon.level = gw.items[prior]
		player_icon.level.lower()

	


# This method saves the level and map layouts to file, as well as removes all items from the screen.
# 	level_num is the numbered level that the player was exploring
# 	level_layout is the array that was storing the level
# 	map_layout is the array that was storing the player's map
# 	prior is the number of items that were on the graphwin prior to starting the exploring() method
def save_and_close(level_num, level_layout, map_layout, prior):

	# Remove all the items drawn onto the graphwin when exploring() was called.
	for i in gw.items[prior:]: i.undraw()

	# Open up the level file in writing mode so it can be overwritten.
	file = open(MAPS / f"level_{level_num}.txt", "w")

	# Write in map_layout first because it has a fixed length.
	# Then write in level_layout because it's length is variable.
	file.write("\n".join("".join(i) for i in map_layout))
	file.write("\n")
	file.write("\n".join("".join(i) for i in level_layout))

	# Finally, close the file so everything is changed.
	file.close()


def map_tutorial():
	dialogue("Welcome to the forest!")
	dialogue("This is your first time, so let me explain some things.")
	dialogue("Here on the left is the level, which is randomly generated upon entering")
	dialogue("Over on the right is your map.")
	dialogue("It's up to you to draw it however you see fit.")
	dialogue("Your goal in every level is to find the stairs up as you work your way towards the mountain and the orc's den.")
	dialogue("To return to town, you will have to head back down the Floor 1 stairs.")
	dialogue("If you ever get lost or stuck, talk to the Librarian.")
	dialogue("Good luck!")

if __name__ == "__main__":

	seed(0)

	player = Player("Rouge", "Rogue", 5, 10, 15, 8, 20, 100, 200, 50, 
		{"Shield": 0,
		"Potions": 3,
		"Apples": 3,
		"magic_item": 0,
		"Fire Scroll": 5,
		"Ice Scroll": 4,
		"Thunder Scroll": 2})

	game_stats["magic_weapon_status"] = 4
	game_stats["level_tutorial"] = False
	exploring(1)



	gw.getKey()