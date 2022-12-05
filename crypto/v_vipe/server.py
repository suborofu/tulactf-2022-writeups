from socketserver import *
import time
import random

flag = b'CTF{C451n0_R4nD0m_W1N5_wH3N_1T_W4NT5_t0}'
time0 = time.time()
prompt = b'''
 _____   ___   _____  _____  _   _  _____  
/  __ \ / _ \ /  ___||_   _|| \ | ||  _  | 
| /  \// /_\ \\\\ `--.   | |  |  \| || | | | 
| |    |  _  | `--. \  | |  | . ` || | | | 
| \__/\| | | |/\__/ / _| |_ | |\  |\ \_/ / 
 \____/\_| |_/\____/  \___/ \_| \_/ \___/  
                                            
______   ___   _   _ ______  _____ ___  ___
| ___ \ / _ \ | \ | ||  _  \|  _  ||  \/  |
| |_/ // /_\ \|  \| || | | || | | || .  . |
|    / |  _  || . ` || | | || | | || |\/| |
| |\ \ | | | || |\  || |/ / \ \_/ /| |  | |
\_| \_|\_| |_/\_| \_/|___/   \___/ \_|  |_/
                                           
                 WELCOME, WELCOME, WELCOME!
                  CASINO RANDOM GREETS YOU!
                NEW PRIZES EVERY 60 SECONDS

Traceback (most recent call last):
  File "/casino_random/task/server.py", line 33, in <module>
    start_all_fun()
  File "/casino_random/task/server.py", line 31, in start_all_fun
    m = money * r.seed(int(time0)).randint(1, 100) / (len(prizes) - 1)
ZeroDivisionError: division by zero

Oh boi, the error has risen. Well, i guess we can play in other way.
Here! I will guess a number [1,100], and you will guess. If you will
succeed 16 times I will give the PRIZE. It is fair, right?

'''


class Handler(BaseRequestHandler):

    def handle(self) -> None:
        self.request.sendall(prompt)
        time1 = time.time()
        seed = int(time0) + 60 * int((time1 - time0) / 60)
        r = random.Random(seed)

        for _ in range(16):
            n = r.randint(1, 100)
            self.request.sendall(b'I have a number. Your guess: ')
            try:
                m = self.request.recv(10)
                guess = int(m.decode('utf-8'))
                if guess == n:
                    self.request.sendall(b'YES!\n')
                else:
                    self.request.sendall(b'NO! MY NUMBER IS ' + str(n).encode('utf-8') + b'\n')
                    self.request.sendall(b'BYE!\n')
                    return None
            except Exception:
                self.request.sendall(b'Oh boi, the error has risen. Again. Bye!\n')
                return None
        self.request.sendall(flag)


if __name__ == '__main__':
    # Есть Address already in use? Подожди 1 минуту
    HOST, PORT = 'localhost', 9999

    with ThreadingTCPServer((HOST, PORT), Handler) as server:
        print('listen on', HOST, PORT)
        server.serve_forever()
