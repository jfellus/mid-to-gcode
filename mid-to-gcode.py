#!/usr/bin/env python3

from mido import MidiFile
from audiolazy import lazy_midi
import GRBL
import time
import sys

grbl = GRBL.GRBL(port = "/dev/ttyUSB0")

ZLOW = -1
ZHIGH = 0


XMIN = 0
XMAX = 50
YMIN = 0
YMAX = 50

MAX_MS = 10000

PITCHES = [
    "C2",
    "D2",
    "G2",
    "A2",
    "B2",
    "C3",
    "D3",
    "E3",
    "F3",
    "F#3",
    "G3",
    "G#3",
    "A3",
    "A#3",
    "B3",
    "C4",
    "C#4",
    "D4",
    "D#4",
    "E4",
    "F4",
    "F#4",
    "G4",
    "G#4",
    "A4",
    "A#4",
    "B4",
    "C5",
    "D5",
    "E5",
]

PITCH_TO_NOTE = {
    lazy_midi.str2midi(k):k for k in PITCHES
}
NOTE_TO_PITCH = {
    v:k for k,v in PITCH_TO_NOTE.items()
}

PITCH_TO_Y = {
    NOTE_TO_PITCH[k]:i for i,k in enumerate(PITCHES)
}

def load_midi(f):
    mid = MidiFile(f, clip=True)
    out = []
    for msg in mid.tracks[2]:
        if msg.type == "note_on":
            t, pitch, velo = msg.bytes()
            dt = msg.time
            out.append((dt, pitch))

    if len(sys.argv)>1:
        out = [(100, NOTE_TO_PITCH[k]) for k in PITCHES]
    return out



commands = []

def t2x(t): return t/MAX_MS * (XMAX-XMIN) + XMIN
def p2y(p): 
    try: 
        return PITCH_TO_Y[p]/len(PITCHES) * (YMAX-YMIN) + YMIN
    except: 
        print("WARNING : no such note : ", p, file=sys.stderr)
        return p2y(NOTE_TO_PITCH["C2"])

SPEED = 1000 # mm/min

t = 0
x = t2x(0)
y = p2y(NOTE_TO_PITCH["C2"])
z = ZHIGH
commands.append(f'G01 X{x} Y{y} Z{z} F{SPEED}')


for dt, pitch in load_midi('test.mid'):
    t += dt
    x = t2x(t)
    y = p2y(pitch)
    commands.append(f'G01 X{y} Y{x} Z{z} F{SPEED}')
    z = ZLOW
    commands.append(f'G01 X{y} Y{x} Z{z} F{SPEED}')
    z = ZHIGH
    commands.append(f'G01 X{y} Y{x} Z{z} F{SPEED}')


grbl.cmd("G28")
for c in commands:
    print(c)
    grbl.cmd(c)
    time.sleep(.1)

commands.append(f'G01 X0 Y0 Z0 F{SPEED}')
