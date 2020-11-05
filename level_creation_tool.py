#level_creation_tool.py

from pathlib import Path
from PIL import Image, ImageDraw
from random import randint, sample, choice, seed
import numpy as np

MAPS = Path(__file__).parent.absolute() / "maps"
TILES = MAPS / "tiles"
SPRITES = MAPS / "sprites"
FOLDER = "forest"


# This method attempts to retrieve the level array from the "maps" folder.
# If it is not found, the code generates a new array and a new background map using generate_level() and draw_level()
# 	level_num is the level of the mountain that needs to be retrieved or generated.
# 	higher determines whether the player is entering this level from a lower floor or a higher floor.
# 		higher=True means that the player is traveling higher, i.e. they entered from a lower floor.
def fetch_level(level_num, higher=True):

	level_arr = []
	start_x = 0
	start_y = 0

	try:
		# Grab the level file from the MAPS folder if it exists.
		file = Path(MAPS / f"level_{level_num}.txt").read_text().split("\n")

		# The first 50 lines are guaranteed to be for the map.
		# The rest of the lines are for the level.
		map_arr = file[:50]
		level_arr = file[50:]

		# If the player is supposed to travel higher, the starting location will be where there is a "/" in level_arr.
		# Else the player is entering the floor from a higher level, and the starting location should be at the "|"
		start = "/" if higher else "|"

		# Loop over level_arr.
		# Each line starts out as a string.
		# If the starting icon calculated above is in that line of level_arr, assign its location to start_x and start_y
		# Additionally, convert the string into a list of characters and save that back into level_arr.
		for i in range(len(level_arr)):
			if start in level_arr[i]:
				start_x, start_y = level_arr[i].index(start), i
			level_arr[i] = list(level_arr[i])

		# Similar to above, every line of map_arr is a string that needs to be converted to a list of characters.
		for i in range(len(map_arr)):
			map_arr[i] = list(map_arr[i])

	except:
		
		# This would have triggered if the level file was not found in the MAPS folder.
		# Each level has a predetermined number of tiles that will make up the width and height of the level.
		# Those values are stored here in level_width and level_height.
		level_width =  [0,  3, 4, 3, 4, 4,  5, 3, 5, 4, 5,  5, 6, 6, 6, 6]
		level_height = [0,  3, 3, 4, 4, 4,  3, 4, 4, 5, 5,  5, 4, 5, 5, 5]

		# Call generate_level(), which will as expected generate the array that makes up the level.
		# It also returns the location of the starting stairs.
		level_arr, start_x, start_y = generate_level(level_num, level_width[level_num], level_height[level_num])

		# Next, generate a blank array for the map.
		# The location of the starting stairs is automatically placed on the map, so save that location as well.
		map_arr = [["." for j in range(30)] for i in range(50)]
		map_arr[start_y + 24][start_x - 1] = "/"

		# Finally, create the image for the level's background that the player will explore.
		draw_level(level_arr, level_num)

	# Return the level, map, and starting coordinates.
	return level_arr, map_arr, start_x, start_y


# This method generates and populates the random level the player will explore.
# 	level_num is the level of the mountain that needs to be retrieved or generated.
# 	x is the number of horizontal tiles that will make up the level.
# 	y is the number of vertical tiles that will make up the level.
def generate_level(level_num, x, y):

	# Generate a generic array arr[] of x's that will be filled in later.
	# Add an extra 2 rows and columns to act as padding so the player cannot "escape" the array.
	arr = np.full(((y * 5) + 2, (x * 5) + 2), "x")

	# Initialize the walls[] and paths[] arrays.
	# These will be used to save which indecese of arr[] are walls and which are walkable paths for later.
	walls = []
	paths = []

	# The mountain is split up into three different "biomes" depending on which floor of the mountain the player is on.
	# Each biome has a specific type of wall that is most common, second most common, and least common to that biome.
	# They are the Primary Wall, Secondary Wall, and Tertiary Wall determined here.
	if level_num < 6: primary_wall, secondary_wall, tertiary_wall = "T", "W", "R"
	elif level_num < 11: primary_wall, secondary_wall, tertiary_wall = "W", "R", "T"
	else: primary_wall, secondary_wall, tertiary_wall = "R", "T", "W"

	# Iterate over x and y to grab the desired number of tiles for the map
	for i in range(y):
		for j in range(x):

			# Load in a random tile from the TILES folder.
			# Then, rotate the tile 90 degrees some number of times and/or vertically flip the tile.
			random_tile = np.loadtxt((TILES / f"{randint(1, 23)}.txt"), str)
			random_tile = np.rot90(random_tile, randint(0, 3))
			if randint(0, 1) == 1:
				random_tile = np.fliplr(random_tile)

			# Loop over the tile so that its layout can be saved to arr[].
			for k in range(5):
				for l in range(5):

					# If the index of random_tile is "X":
					if random_tile[k][l] == "X":

						# Save the coordinates of this spot to walls[].
						walls.append((i * 5 + k + 1, j * 5 + l + 1))
						
						# Change the wall to the Primary Wall determined above.
						random_tile[k][l] = primary_wall
						
					# Else the index is a walkable path, so its coordinates need to be saved into paths[]
					else: paths.append((i * 5 + k + 1, j * 5 + l + 1))

					# Update the index of arr[] with the index of random_tile[].
					arr[i * 5 + k + 1][j * 5 + l + 1] = random_tile[k][l]


	# Now, we place in the Secondary and Tertiary Walls where there were starting walls.
	# Start with the Tertiary Walls, as there is a potential for whichever goes first to be overwritten by the second dfs() call.
	# Create a random-length list of starting nodes selected from walls[].
	# Then loop over that list, performing a limited depth-first search using wall_dfs().
	tertiary_walls = sample(walls, randint(2, 4))
	for i in tertiary_walls:
		wall_dfs(arr, i[1], i[0], tertiary_wall, 2, 3)

	# Do the same as above for the Secondary Walls, again after in case any of the seeds where the walls are created overlap..		
	secondary_walls = sample(walls, randint(3, 6))
	for i in secondary_walls:
		wall_dfs(arr, i[1], i[0], secondary_wall, 2)

	# The levels will also have locations where items can be harvested.
	# These harvest locations need to be walkable, so grab a few random spots from paths[].
	# A harvestable location is denoted by an "A"
	harvest = sample(paths, randint(1, 2))
	for i in harvest:
		arr[i[0]][i[1]] = "A"

	# Finally, select spots where the stairs down and up are.
	# This is encompassed in a while loop because the stairs should be at least 7 spaces in the x or y direction away from each other.
	stairs = []
	while True:
		stair_down = choice(paths)
		stair_up = choice(paths)

		# If the selected stairs are far enough way, save them into stairs[] and break out of the loop.
		if abs(stair_down[0] - stair_up[0]) >= 7 or abs(stair_down[1] - stair_up[1]) >= 7:
			stairs.append(stair_down)
			stairs.append(stair_up)
			break

	# The first item in stairs[] is the starting stairs, and therefore needs the "/" designation.
	# Similarly, the second item in stairs[] is the ending stairs and need the "|" designation.
	arr[stairs[0][0]][stairs[0][1]] = "/"
	arr[stairs[1][0]][stairs[1][1]] = "|"

	# If the player is on the first 2 floors, the stairs must be reachable from each other
	# This is because the player will not have unlocked the ability to buy scrolls and destory walls yet.
	while level_num < 3 and not stairs_bfs(arr, stairs[0]):
		arr[stairs[1][0]][stairs[1][1]] = "."
		stairs[1] = choice(paths)
		arr[stairs[1][0]][stairs[1][1]] = "|"	
	
	# Return the array arr[] as well as the coordinates for the starting stairs.
	return arr, stairs[0][1], stairs[0][0]


# This method performs a limited depth-first-search in order to vary the types of walls in the level.
# 	arr is the array generated by generate_level() that will be explored.
# 	x is the x coordinate of the space in arr that needs to be checked.
# 	y is the y coordinate of the space in arr that needs to be checked.
# 	wall is the type of wall that will be replacing the space dictated by x and y.
# 	num is how much more the wall will continue to spread out from the space dictated by x and y.
# 	spread_factor is used to randomly decide if a wall should spread out an extra amount or not.
def wall_dfs(arr, x, y, wall, num, spread_factor=4):

	# Start by immediately overwriting the space in arr with the provided wall type.
	arr[y][x] = wall

	# If num is greater than 1, than also perform wall_dfs() on the four cardinal points adjacent to arr[y][x].
	if num > 1:

		# Randomly generate a number between 1 and spread_factor.
		# If this number is 1, than the same num is passed into the next call of wall_dfs().
		# If it is not, instead pass in num - 1.
		if arr[y - 1][x] not in [".", "x", wall]: wall_dfs(arr, x, y - 1, wall, num if randint(1, spread_factor) == 1 else num - 1, spread_factor)
		if arr[y][x + 1] not in [".", "x", wall]: wall_dfs(arr, x + 1, y, wall, num if randint(1, spread_factor) == 1 else num - 1, spread_factor)		
		if arr[y + 1][x] not in [".", "x", wall]: wall_dfs(arr, x, y + 1, wall, num if randint(1, spread_factor) == 1 else num - 1, spread_factor)
		if arr[y][x - 1] not in [".", "x", wall]: wall_dfs(arr, x - 1, y, wall, num if randint(1, spread_factor) == 1 else num - 1, spread_factor)


# This method verifies that the ending stairs are accessible from the starting stairs.
# 	It will only run on the first 2 levels.
# 	It return True if they are reachable, otherwise False.
# 	arr is the array generated by generate_level() that will be explored.
# 	coord is a tuple consisting of the x and y coordinates of the starting stairs.
def stairs_bfs(arr, coord):
	
	# I use breadth first search here to find the stairs, because I can.
	# Thus, we need to initalize an array of visited nodes as well as a queue.
	visited = []
	queue = [coord]
 
	# While there are still nodes in queue that need to be checked:
	while queue:

		# Pop the first node in queue[].
		node = queue.pop(0)

		# If that popped node is the stairs up, return True.
		if arr[node[0]][node[1]] == "|":
			return True

		# Else if the node is not a wall, and isn't already in visited:
		elif arr[node[0]][node[1]] in [".", "/"] and node not in visited:

			# Add the node to visited, then add all its cardinally adjacent spaces to queue[]
			visited.append(node)
			queue.append((node[0] - 1, node[1]))
			queue.append((node[0], node[1] + 1))
			queue.append((node[0] + 1, node[1]))
			queue.append((node[0], node[1] - 1))

	# If we reach here, all the spaces radiating out from the starting stairs were explored and the stairs up weren't found.
	# We then should return False.
	return False


# This method draws the level background that the player will see.
# 	level_arr is the array generated by generate_level().
# 	level_num is the floor of the mountain the player is about to explore.
def draw_level(level_arr, level_num):

	# Initialize square size to 48, and map_width and map_height to the horizontal length and vertical height of level_arr[][].
	square_size = 48
	map_width = len(level_arr[0])
	map_height = len(level_arr)

	# Initialize the size of the image the player will see, and set the background to the RGB value (0, 0, 0) i.e. black.
	image = Image.new("RGB", (square_size * map_width, square_size * map_height), (0, 0, 0))

	# Update the SPRITES path to the right biome folder depending on the level_num
	global FOLDER
	if level_num < 6: FOLDER = "forest"
	elif level_num < 11: FOLDER = "swamp"
	else: FOLDER = "mountain"

	# Initialize the various square types and save them into arrays.
	# path, tree, and rock are arrays so that a random image from them can be chosed to add visual variety.
	path = [Image.open(SPRITES / FOLDER / "path0.png"),
			Image.open(SPRITES / FOLDER / "path1.png"),
			Image.open(SPRITES / FOLDER / "path2.png")]
	tree = [Image.open(SPRITES / FOLDER / "tree0.png"),
			Image.open(SPRITES / FOLDER / "tree1.png"),
			Image.open(SPRITES / FOLDER / "tree2.png")]
	water = Image.open(SPRITES / FOLDER / "water.png")
	rock = [Image.open(SPRITES / FOLDER / "rock0.png"),
			Image.open(SPRITES / FOLDER / "rock1.png")]
	harvest = Image.open(SPRITES / FOLDER / "harvest1.png")

	# Loop over all of level_arr[][].
	for i in range(map_height):
		for j in range(map_width):

			# square is the indexed space in level_arr[][] being checked.
			# x and y are the coordinates on image of the upper-left corner where the squares should go.
			square = level_arr[i][j]
			x = (j * square_size)
			y = (i * square_size)
			
			# If square is a wall, place in the correct type of wall.
			if square == "T":
				image.paste(tree[randint(0, 2)], (x, y))
			elif square == "W":
				image.paste(water, (x, y))
			elif square == "R":
				image.paste(rock[randint(0, 1)], (x, y))

			# If the square is a harvestable spot, add in the harvest image.
			elif square == "A":
				image.paste(harvest, (x, y))

			# If the square is the stair up or down, add in those images.
			elif square == "|":
				image.paste(Image.open(SPRITES / FOLDER / "stairs_up.png"), (x, y))
			elif square == "/":
				image.paste(Image.open(SPRITES / FOLDER / "stairs_down.png"), (x, y))
			
			# If the square is supposed to be part of the walkable path.
			elif square == ".":
				image.paste(path[randint(0, 2)], (x, y))

	# The image is saved.
	image.save((MAPS / f"level_{level_num}.png"))			



if __name__ == "__main__":
	
	seed(0)
	fetch_level(6, True)
	
	