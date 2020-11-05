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

def print_red(text, wait = 0, newline = False):
	sys.stdout.write("\033[31m")
	for i in text:
		sys.stdout.write(i)
		sys.stdout.flush()
		sleep(0.03)
	print("\033[37m") if newline else print("\033[37m", end = "")
	sleep(wait)

def print_green(text, wait = 0, newline = False):
	sys.stdout.write("\033[32m")
	for i in text:
		sys.stdout.write(i)
		sys.stdout.flush()
		sleep(0.03)
	print("\033[37m") if newline else print("\033[37m", end = "")
	sleep(wait)

def print_yellow(text, newline = False):
	sys.stdout.write("\033[33m" + text)
	sys.stdout.flush()
	print("\033[37m") if newline else print("\033[37m", end = "")

def print_blue(text, wait = 0, newline = False):
	sys.stdout.write("\033[34m")
	for i in text:
		sys.stdout.write(i)
		sys.stdout.flush()
		sleep(0.03)
	print("\033[37m") if newline else print("\033[37m", end = "")
	sleep(wait)

def print_magenta(text, wait = 0, newline = False):
	sys.stdout.write("\033[35m")
	for i in text:
		sys.stdout.write(i)
		sys.stdout.flush()
		sleep(0.03)
	print("\033[37m") if newline else print("\033[37m", end = "")
	sleep(wait)

def print_cyan(text, wait = 0, newline = False):
	sys.stdout.write("\033[36m")
	for i in text:
		sys.stdout.write(i)
		sys.stdout.flush()
		sleep(0.03)
	print("\033[37m") if newline else print("\033[37m", end = "")
	sleep(wait)

def print_white(text, wait = 0, newline = False):
	sys.stdout.write("\033[37m")
	for i in text:
		sys.stdout.write(i)
		sys.stdout.flush()
		sleep(0.03)
	print("\033[37m") if newline else print("\033[37m", end = "")
	sleep(wait)

def invalid():
	print_white(" That's an invalid action.\n")
	sleep(1)
	


# Testing to make sure all of the colors work in the console.
if __name__ == '__main__':

	os.system("clear")
	print_green("Did it work?")
	print_yellow("Wait, really?!")
	print_blue("God, I'm ecstatic.\n")
	print_magenta("You have no idea how long I've worked on this.")
	print_cyan("Now, to somehow make this a module.")
	print_white("Back to work!")
	print_red("Jeff from the future here, telling you that you no longer need colorama!")