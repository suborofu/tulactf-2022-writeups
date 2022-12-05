import random

flag = b'CTF{WE_CAN_USE_SOME_MATH_HERE_HEHEHEHE}' + b'padding' * 23


def xor(a: bytes, b: bytes):
    return bytes([t0 ^ t1 for t0, t1 in zip(a, b)])


banana = 256 ** 200
# avocado = random.randint(banana // 2, banana)
avocado = 30509105688209796349403290272913582021701996645788396344687950406592729279726815111245700575485714074565944341786585273817564312332267035624272213437098975440558711603035819378941319321408176108755972065963402229753925975843393636691854008164636253410781089675117326751203385912367095094495650291639175526348513085411313862919145780205712224274377506301331483517661662547591766944311719388293446393182654294967172047550045639796068850545684562595945291836183655202877431931833604690


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


from decimal import *


def main():
    print(f'{banana = }')
    print(f'{avocado = }')
    # mask = avocado * (foo(avocado) - 1) + 1
    # mask = mask.to_bytes(mask.bit_length() // 8 + 1, 'big')
    # c = xor(flag, mask)
    with localcontext() as ctx:
        ctx.prec = 256 * 10
        mask = int(ctx.multiply(avocado, (ctx.ln(avocado) - 1)) + 1)
        mask = mask.to_bytes(mask.bit_length() // 8 + 1, 'big')
        c = xor(xor(flag, mask), mask)
    print(f'{c = }')



if __name__ == '__main__':
    main()

# banana = 44462416477094044620016814065517364315819234512137839319418223093753683069769152238984782576173969417485953521141049383745107056455283979316385016701612810119562585078620415976730705698345087039035930761275083827265405596065418173652685035788898113991627042329246850314029877161622487411877779578892097029690461532001915311366862468942148892205997883828265721290296220249202674740669814705818564765009960300389641843321936008416473775144511929246788246559538970957296160626364645376
# avocado = 30509105688209796349403290272913582021701996645788396344687950406592729279726815111245700575485714074565944341786585273817564312332267035624272213437098975440558711603035819378941319321408176108755972065963402229753925975843393636691854008164636253410781089675117326751203385912367095094495650291639175526348513085411313862919145780205712224274377506301331483517661662547591766944311719388293446393182654294967172047550045639796068850545684562595945291836183655202877431931833604690