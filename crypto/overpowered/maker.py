import sympy
import random
import time

n = sympy.randprime(256 ** 32, 256 ** 32 * 2)
f = n - 1
flag = b'CTF{Un1iMltE6_P0w6R_15_Y0uR5!!!}'.zfill(32)
m = int.from_bytes(flag, 'big')

# pow(c, pow(p0, p1, f), n) == m
# pow(m, pow(pow(p0, p1, f), -1, n), n) == c

q0, q1 = 32, 32
while True:
    try:
        p0, p1 = random.randint(256 ** q0 // 2, 256 ** q0), random.randint(256 ** q1 // 2, 256 ** q1)
        d = pow(p0, p1, f)
        e = pow(d, -1, f)
        c = pow(m, e, n)
        # p2 = pow(p0, p1)
        break
    except ValueError:
        pass

# _d, d = d, p2
# print(f'{p2.bit_length() = }')
# t0 = time.time()
# m = pow(c, d, n)
# t1 = time.time()

# print(t1 - t0, 'seconds')
print(m.to_bytes(32, 'big'))
with open('out.py', 'w') as f:
    f.write(f'{n = }\n')
    f.write(f'{c = }\n')
    f.write(f'{p0 = }\n')
    f.write(f'{p1 = }\n')
    f.write(f"print(pow(c, pow(p0, p1), n).to_bytes(32, 'big'))\n")

# while True:
#     try:
#         e = random.randint(n // 2, n - 2)
#         d = pow(e, -1, f)
#         if d * e % f == 1:
#             break
#     except ValueError:
#         pass
#
# k = 100
# t = random.randint(256 ** k, 256 ** k * 2)
# d = t * f + d
# assert d * e % f == 1
#
# c = pow(int.from_bytes(flag, 'big'), e, n)
# t0 = time.time()
# m = pow(c, d, n)
# t1 = time.time()
#
# print(t1 - t0, 'seconds')
# print(m.to_bytes(32, 'big'))
# with open('out.py', 'w') as f:
#     f.write(f'{n = }\n')
#     f.write(f'{c = }\n')
#     f.write(f'{d = }\n')
#     f.write(f"print(pow(c, d, n).to_bytes(32, 'big'))\n")
