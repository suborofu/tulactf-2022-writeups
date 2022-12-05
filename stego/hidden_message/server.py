from socketserver import *
import random

flag = b'CTF{_bUY_G0Ld_DuD3_}'
start, distance = 345, 23


class Handler(BaseRequestHandler):

    def handle(self) -> None:
        m = bytearray(random.randbytes(1024))
        for i in range(len(flag)):
            m[start + distance * i] = flag[i]
        self.request.sendall(m)


if __name__ == '__main__':
    # Есть Address already in use? Подожди 1 минуту
    HOST, PORT = 'localhost', 9999
    with ThreadingTCPServer((HOST, PORT), Handler) as server:
        print('listen on', HOST, PORT)
        server.serve_forever()
