from random import shuffle


class Minesweeper:
    def __init__(self, w, h, d, count, inp=None, outp=None):
        self.width = max(w, 1)
        self.height = max(h, 1)
        self.depth = max(d, 1)
        self.alphabet = '0123456789ABCDEFGHIJKLMNOPQ'
        self.field = [[['*' for _ in range(w)] for _ in range(h)] for _ in range(d)]
        self.mines_count = max(min(count, w * h * d - 1), 1)
        self.flags = 0
        self.cursor = (0, 0, 0)
        if not inp:
            self.input = input
        else:
            self.input = lambda: inp()[:-1].decode('ascii')
        if not outp:
            self.output = print
        else:
            self.output = lambda x: outp(bytes(x, encoding='ascii') + b'\n')
        # Modes
        # 0 - after init, need to set mines after first opening
        # 1 - normal mode
        # 2 - lose
        # 3 - win
        self.mode = 0

        self.mines = [[[0 for _ in range(w)] for _ in range(h)] for _ in range(d)]
        self.used = [[[0 for _ in range(w)] for _ in range(h)] for _ in range(d)]
        self.opened = 0

    def move_cursor(self, direction: str, value):
        z, y, x = self.cursor
        value = max(0, value)
        if direction == 'left':
            x = max(0, x - value)
        elif direction == 'right':
            x = min(self.width - 1, x + value)
        elif direction == 'up':
            y = max(0, y - value)
        elif direction == 'down':
            y = min(self.height - 1, y + value)
        elif direction == 'out':
            z = max(0, z - value)
        elif direction == 'in':
            z = min(self.depth - 1, z + value)
        self.cursor = (z, y, x)

    def set_cursor(self, cursor):
        x, y, z = cursor
        x = max(min(self.width-1, x), 0)
        y = max(min(self.height-1, y), 0)
        z = max(min(self.depth-1, z), 0)
        self.cursor = (z, y, x)


    def flag(self):
        z, y, x = self.cursor
        if self.field[z][y][x] == '*':
            self.field[z][y][x] = '!'
            self.flags += 1
        elif self.field[z][y][x] == '!':
            self.field[z][y][x] = '*'
            self.flags -= 1

    def show(self):
        z, y, x = self.cursor
        self.output(f"Mines left: {self.mines_count - self.flags}")
        self.output(f'depth: {z}')

        self.output(' ' * (x + 2) + 'v')
        self.output(' ' + '-' * (self.width + 2))
        for n, line in enumerate(self.field[z]):
            if y == n:
                temp = '>|' + ''.join(line) + '|<'
            else:
                temp = ' |' + ''.join(line) + '| '
            self.output(temp)
        self.output(' ' + '-' * (self.width + 2))
        self.output(' ' * (x + 2) + '^')

    def generate(self):
        mines = [(z, y, x) for x in range(self.width) for y in range(self.height) for z in range(self.depth)]
        mines.remove(self.cursor)
        shuffle(mines)
        for z, y, x in mines[:self.mines_count]:
            self.mines[z][y][x] = 1

    def check_mines_and_flags(self, z, y, x):
        mines = 0
        flags = 0
        for z1 in range(max(0, z - 1), min(self.depth, z + 2)):
            for y1 in range(max(0, y - 1), min(self.height, y + 2)):
                for x1 in range(max(0, x - 1), min(self.width, x + 2)):
                    if (z1, y1, x1) == (z, y, x):
                        continue
                    if self.mines[z1][y1][x1] == 1:
                        mines += 1
                    if self.field[z1][y1][x1] == '!':
                        flags += 1
        return mines, flags

    def open(self):
        if self.mode == 0:
            self.generate()
            self.mode = 1

        z, y, x = self.cursor
        queue = []
        if self.field[z][y][x] == '*':
            queue.append(self.cursor)
        elif self.field[z][y][x] != '!':
            mines_count, flags_count = self.check_mines_and_flags(z, y, x)
            if mines_count - flags_count == 0:
                for z1 in range(max(0, z - 1), min(self.depth, z + 2)):
                    for y1 in range(max(0, y - 1), min(self.height, y + 2)):
                        for x1 in range(max(0, x - 1), min(self.width, x + 2)):
                            if self.used[z1][y1][x1] == 0:
                                queue.append((z1, y1, x1))

        while len(queue) > 0:
            z, y, x = queue.pop(0)
            self.used[z][y][x] = 1
            if self.field[z][y][x] == '*':
                if self.mines[z][y][x] == 1:
                    self.mode = 2
                    self.field[z][y][x] = '#'
                    break
                else:
                    self.opened += 1
                    mines_count, flags_count = self.check_mines_and_flags(z, y, x)
                    self.field[z][y][x] = self.alphabet[mines_count]
                    if self.depth * self.width * self.height - self.mines_count == self.opened:
                        self.mode = 3
                        break
                    if mines_count == 0:
                        for z1 in range(max(0, z - 1), min(self.depth, z + 2)):
                            for y1 in range(max(0, y - 1), min(self.height, y + 2)):
                                for x1 in range(max(0, x - 1), min(self.width, x + 2)):
                                    if self.used[z1][y1][x1] == 0:
                                        queue.append((z1, y1, x1))

    def play(self):
        self.output(f"Field size: {self.width}x{self.height}x{self.depth}")
        while self.mode != 2 and self.mode != 3:
            self.show()
            try:
                action = self.input().lower()
                if action.split()[0] in ['left', 'right', 'up', 'down', 'in', 'out']:
                    if len(action.split()) == 1:
                        self.move_cursor(action, 1)
                    else:
                        self.move_cursor(action.split()[0], int(action.split()[1]))
                if action.split()[0] == 'cursor':
                    self.set_cursor([int(i) for i in action.split()[1:4]])
                elif action == 'flag':
                    self.flag()
                elif action == 'open':
                    self.open()
            except:
                pass

        self.show()
        if self.mode == 2:
            self.output('You lose!')
            return False
        else:
            self.output('You win!')
            return True


if __name__ == "__main__":
    m = Minesweeper(9, 9, 1, 10)
    if not m.play():
        exit(0)

    m = Minesweeper(5, 5, 5, 10)
    if not m.play():
        exit(0)

    m = Minesweeper(30, 30, 30, 900)
    if not m.play():
        exit(0)

    print('aboba_template')
