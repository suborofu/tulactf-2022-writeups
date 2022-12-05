from pwn import *

HOST, PORT = 'localhost', 9999

t0 = int(time.time())
guesses = []
for i in range(t0 - 60, t0 + 60):
    rnd = random.Random(i)
    guesses.append([rnd.randint(1, 100) for _ in range(16)])

guess_line = [1]
for _ in range(16):
    r = connect(HOST, PORT)
    for guess in guess_line:
        r.recvuntil(b'Your guess: ')
        r.send(str(guess).encode('utf-8'))
        # reaction = r.recvuntil([b'YES!', b'NO! MY NUMBER IS ']).strip()
        # if reaction.startswith(b'YES!'):
    reaction = r.recvuntil([b'YES!', b'NO! MY NUMBER IS ', b'}']).strip()
    if not reaction.startswith(b'YES!'):
        if not reaction.startswith(b'NO!'):
            print(reaction)
            break
        guess_line[-1] = (int(r.recvuntil(b'\n').decode('utf-8')))
        good = []
        for gl in guesses:
            g = True
            for a, b in zip(gl, guess_line):
                g &= a == b
            if g:
                good.append(gl)
        guesses = good
        if len(good) == 1:
            guess_line = good[0]
            r = connect(HOST, PORT)
            for g in guess_line:
                r.send(str(g).encode('utf-8'))
                print(g)
                sleep(1)
            print(r.recvall().splitlines()[-1])
            break
    else:
        good = []
        for gl in guesses:
            g = True
            for a, b in zip(gl, guess_line):
                g &= a == b
            if g:
                good.append(gl)
        if len(good) == 1:
            guess_line = good[0]
            r = connect(HOST, PORT)
            for g in guess_line:
                r.send(str(g).encode('utf-8'))
            print(r.recvall())
            break
        else:
            guess_line.append(1)

    print(guess_line)
