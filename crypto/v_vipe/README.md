# V VIP'e?

## Условие

Нашел тут одно подпольное  местечко. Все законно, не подумай. Вот только все равно дурят людей. Ну как в запечатанной пачке могут быть разложены по-другому карты?

Может быть, хоть ты их обыграешь? Выиграй у них все, что сможешь, и побыстрее возвращайся.

Формат флага: `TulaCTF{some_flag}`

## Решение

Числа меняются каждую минуту, поэтому достаточно за одну минуту обратиться к серверу **17** раз:

- за **16** попыток узнаем все числа, вводя правильные числа, полученные на прошлых шагах;
- на **17** шаге вводим все **16** чисел и получаем флаг;
- ???
- **PROFIT!**

При чем тут крипта - я не знаю, но что есть, то есть.
