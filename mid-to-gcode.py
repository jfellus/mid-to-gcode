from mido import MidiFile

def load_midi(f):
    mid = MidiFile(f, clip=True)
    out = []
    for msg in mid.tracks[2]:
        if msg.type == "note_on":
            t, pitch, velo = msg.bytes()
            dt = msg.time
            out.append((dt, pitch))
    return out


commands = []

def t2x(t): return t * 0.2
def p2y(p): return p * 10

SPEED = 400 # mm/min

t = 0
x = 0
y = 0
z = 0
commands.append(f'G01 X{x} Y{y} Z{z} F{SPEED}')


for dt, pitch in load_midi('test.mid'):
    print(dt, pitch)
    t += dt
    x = t2x(t)
    y = p2y(pitch)
    commands.append(f'G01 X{x} Y{y} Z{z} F{SPEED}')
    z = 1
    commands.append(f'G01 X{x} Y{y} Z{z} F{SPEED}')
    z = 0
    commands.append(f'G01 X{x} Y{y} Z{z} F{SPEED}')

print("\n".join(commands))