# Sign Break

## Условие

Тут одна компания, попросившая себя не называть, ищет то ли криптонца, то ли криптида для важного дела. Короче, взломать им надо что-то. Ну и тут я предложил твою кандидатуру. Подробности они сами расскажут.

Формат флага: `TulaCTF{some_flag}`

## Решение

В задаче имеем дело с этой функцией:

```python
import hashlib
import base64


def make_sign(m: bytes):
    hmac = hashlib.sha256(salt + m).hexdigest()
    return base64.b64encode(m) + b'&' + hmac.encode('ASCII')
```

И имеем сообщение, полученное от этой функции:

```
cHJpbnQoIkhFTExPIFdPUkxEISIsIDErMiszKzQrNSk=&5684f9a13cb97ffc48662cca6d669475a1b7ede3af6fb842387f6e3395320cbc
```

Функция `make_sign` уязвима к атаке Length Extension. Т.е. hmac от сообщения вычисляется как `sha256(salt | m | padding_A)`. Имея это значение мы можем вычислить хэш для любой другой строки вида `sha256(salt | m | padding_A | your_exploit | padding_B)`

Смотри файлы `le_attack.py` и `sha256.py` для примера.
