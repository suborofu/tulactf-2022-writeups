from mido import MidiFile

mid = MidiFile('music.mid', clip=True)

for msg in mid.tracks[3]:
    if msg.type == 'note_on':
        print(chr(msg.velocity), end='')
