to_int = lambda x: int.from_bytes(x, 'big')
xor_ans = 0x165f130d480208
congrats = "You found it!"
add_ans = 0x2d9f2a28056c49
wrong = 'Wrong!!'

def xor(a, b):
    ans = [a1 ^ b1 for a1, b1 in zip(a, b)]
    return to_int(ans)

def add(a, b, c):
    ans = [(c1 + b1) % (a * a) for c1, b1 in zip(c, b)]
    return to_int(ans)

def ext(ret):
    print(wrong)
    exit(ret)

length_wrong = len(wrong)
inp = bytes(input(), 'ascii')
if len(inp) != length_wrong + length_wrong:
    ext(length_wrong)
length_congrats = len(congrats)
left = [inp[i] for i in range(length_wrong)]
right = [inp[i] for i in range(length_wrong, length_wrong + length_wrong)]
inp = xor(left, right)
if inp != xor_ans:
    ext(inp)
inp = add(length_congrats, right, left)
if inp != add_ans:
    ext(inp)
print(congrats)
