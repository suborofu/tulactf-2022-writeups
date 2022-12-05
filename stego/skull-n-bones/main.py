from mido import MidiFile

mid = MidiFile('source.mid', clip=True)

flag = "tulactf{megalovania_under_tale}"

counter = 0
for msg in mid.tracks[3]:
    if msg.type == 'note_on':
        msg.velocity = ord(flag[counter])
        counter = (counter + 1) % len(flag)

mid.save('generated.mid')
