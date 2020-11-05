from pathlib import Path
from random import randint
import numpy as np

ROOT = Path(__file__).parent.absolute()

if __name__ == "__main__":

	i = 0

	while i < 100:
		i += 1
		filename = (str(i) + '.txt')

		try:
			print(f"File: {filename}\n{(ROOT / filename).read_text()}\n")
		except:
			pass

		