import random

from secret import flag


def xor(a: bytes, b: bytes):
    return bytes([t0 ^ t1 for t0, t1 in zip(a, b)])


banana = 256 ** 200
avocado = random.randint(banana // 2, banana)


def bar(x: float):
    x = 1 - x
    s = 0
    for i in range(1, banana):
        s += pow(x, i) / i
    return -s


def faz():
    s = 0
    for i in range(1, banana):
        if i % 2 == 0:
            s += 1 / i
        else:
            s -= 1 / i
    return s


def baz(x: float):
    a, n, p = abs(x), 0, 1
    while p < a:
        p <<= 1
        n += 1
    zaf = -faz()
    return n * zaf + bar(a / p)


def foo(x: float):
    foo_10 = baz(10)
    n, a = 0, abs(x)
    while a > 1:
        n += 1
        a /= 10
    return n * foo_10 + bar(a)


def main():
    print(f'{banana = }')
    print(f'{avocado = }')
    mask = 0
    for i in range(1, avocado + 1):
        mask += foo(i)
    mask = mask.to_bytes(mask.bit_length() // 8 + 1, 'big')
    c = xor(flag, mask)
    print(f'{c = }')


if __name__ == '__main__':
    main()
