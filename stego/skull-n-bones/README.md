# Skull'n'Bones

## Условие

Шел я, значит, по улице, и вижу парня: стоит в синей куртке, худой, аж кости видны, и плееры продает уже с музыкой. Ну я парень добрый, купил один и пошел дальше, не драться ж с ним...

На плеере был один единственный трек, зато какой! Но как будто с ним что-то не так. Поможешь выяснить, что конкретно?

Формат флага: `TulaCTF{some_flag}`

## Решение

Формат файла **MID** подразумевает, что флаг скрыт в инструментальных каналах трека.

Исследуем дорожки и видим, что у громкость нот у **4** инструмента странно выглядит: значения громкости сходятся с печатуемыми *(есть вообще такое слово?)* ASCII символами, после некоторого периода значения повторяются.

Переводим громкость в ASCII, выводим в консоль и получаем флаг.
