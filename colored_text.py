# colored_text.py
# A function that is called by all of the other programs that I'll be using.
# It allows me to print specific colored text to the console, for dialogue.
# Also a test to figure out how to make a module. Or library. Or whatever it's called.
# In order to use it correctly, you need to use a string of these print functions, swapping between white and whatever other color.
# Make sure variables are put in as print_<color>(str(<variable>))

# Importing the module that I'll be using for color. By default, it won't reset the color at the end of the line, so an exception has been made.
import os
import sys
from time import sleep



def print_red(text):
	for i in text:
		sys.stdout.write("\033[31m" + i)
		sys.stdout.flush()
		sleep(0.03)

def print_green(text):
	for i in text:
		sys.stdout.write("\033[32m" + i)
		sys.stdout.flush()
		sleep(0.03)

def print_yellow(text):
	sys.stdout.write("\033[33m" + text)
	sys.stdout.flush()

def print_blue(text):
	for i in text:
		sys.stdout.write("\033[34m" + i)
		sys.stdout.flush()
		sleep(0.03)

def print_magenta(text):
	for i in text:
		sys.stdout.write("\033[35m" + i)
		sys.stdout.flush()
		sleep(0.03)

def print_cyan(text):
	for i in text:
		sys.stdout.write("\033[36m" + i)
		sys.stdout.flush()
		sleep(0.03)

def print_white(text):
	for i in text:
		sys.stdout.write("\033[37m" + i)
		sys.stdout.flush()
		sleep(0.03)

def invalid():
	print_white(" That's an invalid action.\n")
	sleep(1)
	


# Testing to make sure all of the colors work in the console.
if __name__ == '__main__':

	os.system("cls")

	print_green("Did it work?\n")
	print_yellow("Wait, really?!\n")
	print_blue("God, I'm ecstatic.\n")
	print_magenta("You have no idea how long I've worked on this.\n")
	print_cyan("Now, to somehow make this a module.\n")
	print_white("Back to work!\n")
	print_red("Jeff from the future here, telling you that you no longer need colorama!")