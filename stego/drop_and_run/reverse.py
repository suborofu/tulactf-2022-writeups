from PIL import Image
gif = Image.open('video.gif')
original = gif.copy().convert('L')
original_data = list(original.getdata())
try:
    while True:
        gif.seek(gif.tell()+1)
        gif_data = gif.convert('L').getdata()
        for i in range(len(original_data)):
            original_data[i] = original_data[i] ^ gif_data[i]
except EOFError:
    pass

original.putdata(original_data)
original.show()
original.save('reversed.jpg')
