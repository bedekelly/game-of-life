#!/usr/bin/python3
import random
import os

x, y = os.get_terminal_size().columns, os.get_terminal_size().lines


with open("input", "w") as f:
	for _ in range(y - 1):
		for _ in range(x - 1):
			f.write(random.choice(["@", "-"]))
		f.write("\n")
