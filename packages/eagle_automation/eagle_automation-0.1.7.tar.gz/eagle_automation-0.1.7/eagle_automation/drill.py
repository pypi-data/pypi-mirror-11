#!/usr/bin/env python

import re
import sys

def drill():
	lines = 0

	for line in sys.stdin:
		g = re.match(r" (T[0-9][0-9]) *([0-9.]+)(\w+) *", line)
		if g:
			drill, size, unit = g.groups()
			size = float(size)

			if unit == 'inch':
				size = size * 2.54e1
			elif unit == 'mils':
				size = size * 2.54e-2
			elif unit != 'mm':
				raise Exception("Unknown unit: " + unit)

			sys.stdout.write("%s  %.2fmm\n" % (drill, size))

			lines += 1

	if not lines:
		sys.stderr.write("Error: no drills found!\n")
		sys.exit(1)


