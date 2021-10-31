#!/usr/bin/env python3
import GRBL
import sys

cmd = {"X":0,"Y":0,"Z":0}
grbl = GRBL.GRBL(port = "/dev/ttyUSB0")

grbl.cmd("G28")
axis = "X"

for line in map(str.rstrip, sys.stdin):
    line = line.upper()
    if not line: line = lastline
    if line == "X": axis = "X"
    elif line == "Y": axis = "Y"
    elif line == "Z": axis = "Z"
    else: 
        val = float(line)
        cmd[axis] += val
        print(f'''{axis} += {val}''')
        grbl.cmd(f'''G01 X{cmd['X']} Y{cmd['Y']} Z{cmd['Z']} F1000''')
    lastline = line
