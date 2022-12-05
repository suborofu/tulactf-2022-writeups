from time import sleep
from random import choice
morse = ".--- .---- -. -.... .-.. ...-- ..--.- ...-- .-. .-. ----- .-. ..--.- -... ...-- .-.. .-.. ....."
time_unit = 0.1
random_errors = [
    "RuntimeError: Failed to open database",
    "TypeError: unsupported operand type(s) for /: 'str' and 'str'",
    "TypeError: unsupported operand type(s) for /: 'biba' and 'boba'",
    "Import error: No module named numpy",
    "Import error: No module named aboba",
    "TypeError: 'numpy.ndarray' object is not callable",
    "TypeError: 'amogus.kill' object is not callable",
    "ValueError: The truth value of an array with more than one element is ambiguous",
    "NameError: Here we go again...",
]
for char in morse:
    if char == '.':
        print(choice(random_errors), '\a')
        sleep(2 * time_unit)
    
    elif char == '-':
        print(choice(random_errors), '\a')
        sleep(4 * time_unit)
    
    elif char == ' ':
        sleep(7 * time_unit)
