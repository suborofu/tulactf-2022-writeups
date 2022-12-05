from pwn import *

HOST, PORT = 'localhost', 9999
r = connect(HOST, PORT)

m = r.recvall()
print(''.join([chr(b) for b in (m[345 + 23 * i] for i in range(20))]))
