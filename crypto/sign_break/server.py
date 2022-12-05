from socketserver import *

import hashlib
import base64

flag = b'CTF{Len8Th_Ext3ns10N_AtT4ck____}'
salt = hashlib.md5(b'MY TAIL IS').digest() + hashlib.md5(b'AMAZING').digest()


def make_sign(m: bytes):
    hmac = hashlib.sha256(salt + m).hexdigest()
    return base64.b64encode(m) + b'&' + hmac.encode('ASCII')


def check_sigh(c: bytes):
    m, h = c.split(b'&')[-2:]
    hmac = hashlib.sha256(salt + base64.b64decode(m)).hexdigest()
    return h.decode('ASCII') == hmac


def test_message(m: bytes):
    return check_sigh(m) and base64.b64decode(m.split(b'&')[-2:][0]).find(b'print(flag)')


# Ну эт я размахнулся, да :)
# арт https://patorjk.com/software/taag/#p=display&h=1&f=Modular&t=SIGN%20BREAK
prompt = b"""
 _______  ___  _______  __    _   _______  ______    _______  _______  ___   _ 
|       ||   ||       ||  |  | | |  _    ||    _ |  |       ||   _   ||   | | |
|  _____||   ||    ___||   |_| | | |_|   ||   | ||  |    ___||  |_|  ||   |_| |
| |_____ |   ||   | __ |       | |       ||   |_||_ |   |___ |       ||      _|
|_____  ||   ||   ||  ||  _    | |  _   | |    __  ||    ___||       ||     |_ 
 _____| ||   ||   |_| || | |   | | |_|   ||   |  | ||   |___ |   _   ||    _  |
|_______||___||_______||_|  |__| |_______||___|  |_||_______||__| |__||___| |_|

Hello, Agent. You are here to solve the task for us.
We provide you this information and exploit. Use it carefully.

We know, that target machine call some sort of python's eval method for received strings after successful checking the sign.
Here is the code for signing messages, that we were able to find out:

import hashlib
import base64
def make_sign(m: bytes):
    hmac = hashlib.sha256(salt + m).hexdigest()
    return base64.b64encode(m) + b'&' + hmac.encode('ASCII')

Also we know, that len(salt) == 32.

Gratefully, we also acquired for you some signed message. Here is the sign for message 'print("HELLO WORLD!", 1+2+3+4+5)':
cHJpbnQoIkhFTExPIFdPUkxEISIsIDErMiszKzQrNSk=&5684f9a13cb97ffc48662cca6d669475a1b7ede3af6fb842387f6e3395320cbc

We know, that target machine have in memory some _flag_. You need to get it. Here is the exploit for you, just put it in any random message in any place, even if the message becomes invalid for eval function: 'print(flag)'

Now you know what to do. Here, use this shell to try some messages. Be careful, you have just one attempt
"""


class Handler(BaseRequestHandler):

    def handle(self) -> None:
        try:
            self.request.sendall(prompt)
            self.request.sendall(b'> ')
            m: bytes = self.request.recv(1024)
            if len(m) == 0 or m.find(b'&') == -1:
                self.request.sendall(b'INCORRECT MESSAGE\n')
                return
            if test_message(m.strip()):
                self.request.sendall(flag + b'\n')
                return
            self.request.sendall(b'CHECK FAIL\n')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # Есть Address already in use? Подожди 1 минуту
    HOST, PORT = 'localhost', 9999
    with ThreadingTCPServer((HOST, PORT), Handler) as server:
        server.serve_forever()
