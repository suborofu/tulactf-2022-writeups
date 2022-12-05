from socketserver import *
from minesweeper import Minesweeper

flag = b'TulaCTF{aboba_template}'
prompt = br'''
          ____                                                              
        ,'  , `.                                                            
     ,-+-,.' _ |  ,--,                                                      
  ,-+-. ;   , ||,--.'|         ,---,                                        
 ,--.'|'   |  ;||  |,      ,-+-. /  |                                       
|   |  ,', |  ':`--'_     ,--.'|'   |   ,---.                               
|   | /  | |  ||,' ,'|   |   |  ,"' |  /     \                              
'   | :  | :  |,'  | |   |   | /  | | /    /  |                             
;   . |  ; |--' |  | :   |   | |  | |.    ' / |                             
|   : |  | ,    '  : |__ |   | |  |/ '   ;   /|                             
|   : '  |/     |  | '.'||   | |--'  '   |  / |                             
;   | |`-'      ;  :    ;|   |/      |   :    |                             
|   ;/          |  ,   / '---'        \   \  /                              
'---'            ---`-'                `----'                               
  .--.--.                                                                   
 /  /    '.                                   ,-.----.                      
|  :  /`. /          .---.                    \    /  \             __  ,-. 
;  |  |--`          /. ./|                    |   :    |          ,' ,'/ /| 
|  :  ;_         .-'-. ' |   ,---.     ,---.  |   | .\ :   ,---.  '  | |' | 
 \  \    `.     /___/ \: |  /     \   /     \ .   : |: |  /     \ |  |   ,' 
  `----.   \ .-'.. '   ' . /    /  | /    /  ||   |  \ : /    /  |'  :  /   
  __ \  \  |/___/ \:     '.    ' / |.    ' / ||   : .  |.    ' / ||  | '    
 /  /`--'  /.   \  ' .\   '   ;   /|'   ;   /|:     |`-''   ;   /|;  : |    
'--'.     /  \   \   ' \ |'   |  / |'   |  / |:   : :   '   |  / ||  , ;    
  `--'---'    \   \  |--" |   :    ||   :    ||   | :   |   :    | ---'     
               \   \ |     \   \  /  \   \  / `---'.|    \   \  /           
  .--,-``-.     '---"       `----'    `----'    `---`     `----'            
 /   /     '.      ,---,                                                    
/ ../        ;   .'  .' `\                                                  
\ ``\  .`-    ',---.'     \                                                 
 \___\/   \   :|   |  .`\  |                                                
      \   :   |:   : |  '  |                                                
      /  /   / |   ' '  ;  :                                                
      \  \   \ '   | ;  .  |                                                
  ___ /   :   ||   | :  |  '                                                
 /   /\   /   :'   : | /  ;                                                 
/ ,,/  ',-    .|   | '` ,/                                                  
\ ''\        ; ;   :  .'                                                    
 \   \     .'  |   ,.'                                                      
  `--`-,,-'    '---'                                                                                                                                    

Welcome to MineSweeper3D.
You have to win three times to get the flag. Each next level is more difficult than the previous one.
The rules of the game:

- The field has 3 dimensions.
- The cursor is at the [0;0;0] coordinate at the start.
- To move the cursor left or right by N cells use the 'left [N]' and 'right [N]' commands.
- To move the cursor up or down by N cells use the 'up [N]' and 'down [N]' commands.
- To move the cursor inward or outward by N cells use the 'in [N]' and 'out [N]' commands.
- To move the cursor to the specific cell use the 'cursor [X] [Y] [Z]' command.
- The '!' character means a flag. The flag means that there should be a mine in the cell. This cell cannot be opened.
- To set/unset the flag at the cursor use the 'flag' command.
- The '*' character means an unopened cell.
- To open a cell at the cursor use the 'open' command. You can also use this command at an opened cell. In this case, the cells next to this cell are opened if numbers of flags and mines next to it are the same. 
- The '0-9A-Q' characters means that there are 0-26 mines near the cell.
- The '#' character means a mine.
- You lose when you open a cell with a mine.
- You win if all unopened cells contain mines.

'''


class Handler(BaseRequestHandler):

    def handle(self):
        self.request.sendall(prompt)
        self.request.sendall(b'Round 1!\n\n')
        m = Minesweeper(9, 9, 1, 10, inp=lambda: self.request.recv(1024), outp=self.request.sendall)
        if not m.play():
            return

        self.request.sendall(b'Round 2!\n\n')
        m = Minesweeper(5, 5, 5, 10, inp=lambda: self.request.recv(1024), outp=self.request.sendall)
        if not m.play():
            return

        self.request.sendall(b'Round 3!\n\n')
        m = Minesweeper(30, 30, 30, 900, inp=lambda: self.request.recv(1024), outp=self.request.sendall)
        if not m.play():
            return

        self.request.sendall(b'You did it! Nice! Here the flag: ' + flag)


if __name__ == '__main__':
    # Есть Address already in use? Подожди 1 минуту
    HOST, PORT = 'localhost', 9999

    with ThreadingTCPServer((HOST, PORT), Handler) as server:
        print('listen on', HOST, PORT)
        server.serve_forever()
