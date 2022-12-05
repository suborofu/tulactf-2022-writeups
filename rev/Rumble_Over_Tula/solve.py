import string
import re
XOR = 0x165f130d480208
ADD = 0x2d9f2a28056c49

flag = [[] for i in range(7)]
for n in range(7):
    x = XOR & 0xFF
    a = ADD & 0xFF
    XOR >>= 8
    ADD >>= 8
    for i in string.printable:
        temp1 = ord(i)
        temp2 = temp1 ^ x
        if (temp1 + temp2) % 169 == a and chr(temp2) in string.printable:
            flag[n].append((temp1, temp2))

flag = list(reversed(flag))

for a0, b0 in flag[0]:
    for a1, b1 in flag[1]:
        for a2, b2 in flag[2]:
            for a3, b3 in flag[3]:
                temp = ''.join([chr(i) for i in [a0, a1, a2, a3]])
                if temp != 'flag':
                    continue
                for a4, b4 in flag[4]:
                    for a5, b5 in flag[5]:
                        for a6, b6 in flag[6]:
                            temp = ''.join([chr(i) for i in [a0,a1,a2,a3,a4,a5,a6,b0,b1,b2,b3,b4,b5,b6]])
                            if re.findall(r'flag\{[\w+]{8}\}', temp):
                                print(temp)
