# Внимание! Кушает много памяти (у меня получилось 1.7 ГБ оперативы на выходе)

import random

from PIL import Image

frames = []

frame = Image.open('original.jpg').convert('RGB')
size = frame.size
back = Image.open('back.png').convert('RGB')
f_data = list(back.getdata())

for i in range(150):
    if i % 10 == 0:
        print(i//10)
    f = Image.new('RGB', size, 0)
    data = list(frame.getdata())
    for j in range(len(data)):
        data[j] = data[j] if data[j][0] > 128 and random.random() <= 0.007 else f_data[j]
    f.putdata(data)
    frames.append(f)

frames[0].save(
    'video.gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=100,
    loop=0
)
