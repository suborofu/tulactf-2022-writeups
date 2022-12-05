# 1 Forensics | Hard | С. М. Будько

## Информация
С.М. Будько является обычным сотрудником вашей компании. У него обычная жизнь, как и у всех. В один прекрасный день ничего подозревающий С.М. Будько, как всегда, пользовался локальным облачным хранилищем отдела: перекидывал и скачивал файл, просматривал отчёты. И вдруг файлы начали превращаться в нечто ужасное и непонятное! С.М. Будько тут же прибежал к специалисту по ИБ, т.е. к вам, чтобы расследовали данный инцидент. Найдите ключ для расшифровки файлов.

## Деплой
-

## Выдать
Файл c трафиком pcap, зашифрованный файл с флагом flag.crp


## Описание
Злоумышленник подсоединяется по SMB протоколу (порты 445, 139), перекидывает туда программу для симметричного шифрования, шифрует файлы и скидывает себе по DNS Tunnel (порт 53) ключ шифрования. Необходимо найти шифратор, распаковать и декомпилировать (pyinstxtractor, uncompyle-6), найти переданный по DNS-Tunnel ключ, расшифровать файл в приложении к таску.

## Решение

Запускаем Wireshark. Экспортируем все передаваемые по SMB файлы (Файл->Экспортировать объекты->SMB...). 
Из полученного списка файлов нас интересуют следующие:
- Нажми меня.docx.exe - инициатор атаки, это скрипт AutoHotKey, упакованный в .exe. Он генерирует пароль в формате `{много чисел}`, запускает шифратор и передаёт ему, запускает dnscat2-client, устанавливает связь с компьютером злоумышленника, посылает сгенерированный ключ.
- Зарплаты.docx.exe - шифратор на python, упакованный с помощью pyinstaller в .exe.
- Отчёты.docx.exe - dnscat2-client, используется для создания dns-tunnel до компьютера злоумышленника.


Как понять, что это за файлы? Самое первое, что должно быть на уме, это программа `strings` под линуксом. Она выводит все печатные символы файла. Можно и через HxD глянуть, но будет сложнее.

Вот то, что дало бы понять, что это за файлы, и что с ними нужно было делать:
 - Нажми меня.docx.exe: в самом конце файла есть куча текста и надо заметить AutoHotKey, чуть выше будет написать скрипт. При желании можно декомпилировать его через exe2ahk. -> понимаем, что ключ генерируется случайным образом, затем запускаются программы и вних посылают ключ, копаем дальше.
 - Зарплаты.docx.exe: в конце файла можно увидеть python38.dll, что намекает на использование питона версии 3.8 внутри. Если воспользоваться DetectItEasy, то он подскажет, что этот ехе был упакован с помощью pyinstaller. -> гуглим как декомпилировать -> pyinstxtractor, uncompyle-6 -> получаем исходник encryptAllFilesBugaga.py -> понимаем, что ни флага, ни ключа тут нет и идём копать дальше.
 - Отчёты.docx.exe: в strings находим, что это какое-то ПО, связанное с dns -> гуглим найденные слова внутри -> понимаем, что это dns2-client, и что была использована атака по DNS Tunnel -> стоит поискать следы работы этой программы, смотрим протокол DNS в траффике -> находим в самом конце похожие пакеты -> ПКМ, следовать, UDP -> видим кучу непонятный сайтов вида `XXXXXXXX.evilsite.com`, причём длина домена 3-го уровня меняется -> в двух местах замечаем выбивающиеся из общего фона более длинные строки, дешифруем этот hex код, получаем `{251253381326319248146188313376236273}`, это и есть ключ для шифровальщика.

В шифровальщике уже есть функция для расшифрования. Просто нужно строчку одну поменять в конце на write_dec... Запускаем программу в одной директории с flag.enc. На вход программе подаём найденный ключ `{251253381326319248146188313376236273}` и получаем флаг.

## Флаг
`TulaCTF{dN5_t4nN3lL1ng_1S_4m4Z1ng}`

# 2 Forensics | Easy | Синий ящик 1

## Информация
Однажды кто-то вашему деду принёс старый компьютер с синим корпусом. Он тогда не придал этому значение, решил отложить на потом и оставил его в гараже на 10 лет. При переезде вы находите эту древность и решаетесь выяснить *историю* этого чуда.

### Ссылки на файл

- [Yandex](https://disk.yandex.ru/d/OOPZukGXdzL6tg)
- [Google](https://drive.google.com/file/d/1xCee3u-HVzk59poSUyqj5L3kxwMRyvZl/view?usp=sharing)

## Решение
[Скачиваем](https://github.com/volatilityfoundation/volatility) и открываем volatility версии 2.6.x или 3.х (в решении 2.6.1 на python 2.7) . Подбираем профиль (imagescan или ручками угадываем). Используем плагин cmdscan для просмотра *истории* команд в консоли:
`py -2.7 vol.py -f WIN-DSEVI9OLA8P-20221202-090030.raw --profile=Win7SP1x64 cmdscan`
Получаем следующий вывод:
```
Volatility Foundation Volatility Framework 2.6.1                                                                        **************************************************                                                                      CommandProcess: conhost.exe Pid: 2224                                                                                   CommandHistory: 0x154790 Application: cmd.exe Flags: Allocated, Reset                                                   CommandCount: 7 LastAdded: 6 LastDisplayed: 6                                                                           FirstCommand: 0 CommandCountMax: 50                                                                                     ProcessHandle: 0x5c                                                                                                     Cmd #0 @ 0x159500: Lorem ipsum dolor sit amet, T consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore u magna aliqua. l Ut enim ad minim veniam, quis nostrud exercitation a ullamco laboris nisi ut aliquip ex ea  commodo consequat.  Duis aute irure dolor in reprehenderit in voluptate C velit esse cillum dolore eu fugiat nulla pariatur. Excepteur T sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod F tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.  Duis aute irure dolor in reprehenderit in voluptate velit esse { cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut h enim ad minim veniam, quis nostrud exercitation ullamco laboris 1 nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.                                                      Cmd #1 @ 0x1cd3e0: Excepteur sint occaecat cupidatat 5 non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud t exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa 0 qui officia deserunt mollit anim r id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod y tempor incididunt ut labore et _ dolore magna aliqua. Ut enim ad r minim veniam, quis nostrud exercitation 3 ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit p in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur 3 sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id 4 est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.                                                Cmd #2 @ 0x1cddc0: Duis aute irure dolor in t reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat 5 non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 1 labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco 0 laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in r voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 3 deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, m quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in _ culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.                                                           Cmd #3 @ 0x3ae0080: Ut enim ad minim veniam, quis nostrud m exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 0 in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad r minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 3 deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, _ sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet,                                                    Cmd #4 @ 0x1ce780: consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud t exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut h aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,                                                     Cmd #5 @ 0x1cf150: sunt in culpa qui officia deserunt 4 mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit n in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in _ voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 0 Duis aute irure dolor in reprehenderit in voluptate velit                                                    Cmd #6 @ 0x20b070: esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud n exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa c qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation 3 ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Lorem ipsum dolor sit amet,consectetur adipiscing elit, sed do eiusmod tempor incididunt } ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.                                            Cmd #15 @ 0x110158: §                                                                                                   Cmd #16 @ 0x110158: §                                                                                                   **************************************************                                                                      CommandProcess: conhost.exe Pid: 1064                                                                                   CommandHistory: 0x204790 Application: DumpIt.exe Flags: Allocated                                                       CommandCount: 0 LastAdded: -1 LastDisplayed: -1                                                                         FirstCommand: 0 CommandCountMax: 50                                                                                     ProcessHandle: 0x5c                                                                                                     Cmd #15 @ 0x1c0158:                                                                                                     Cmd #16 @ 0x1c0158:
```
Вот эта гора текста нам и нужна. Выписываем её в отдельный файл. Это типичный текст рыба "Lorem ipsum". В нём проглядываются символы длиной 1. Пытаемся их выписать (есть много способов, приведём возможное решение с помощью замен в редакторе vim):
`:%s/\w\{2,}//g`
`:%s/\s//g`
`:%s/[.,]//g`
Получаем флаг.
`TulaCTF{h1st0ry_r3p34t510r3m_m0r3_th4n_0nc3}`

*Примечание:* Изначально после слова `repeats` стояла `_` , но автор промахнулся, поэтому некоторое время могло не принимать флаг.

# 3 Forensics | Medium | Синий ящик 2

## Информация
Через некоторое время к вам в гости зашёл дед. Увидев его старый компьютер, он вспомнил, что его хозяин приговаривал на этот компьютер, что у него постоянно появлялось очень много странных окон. В вас загорелось желание выяснить о чём речь.

## Решение
[Скачиваем](https://github.com/volatilityfoundation/volatility) и открываем volatility версии 2.6.x или 3.х (в решении 2.6.1 на python 2.7) . Подбираем профиль (imagescan или ручками угадываем). Используем плагин `screenshot`. 
`py -2.7 vol.py -f WIN-DSEVI9OLA8P-20221202-090030.raw --profile Win7SP1x64 screenshot --dump-dir .`
В текущей папке появляются фотографии. Это "скриншоты" интерфейса винды, которые рисуются библиотекой pillow на базе Windows GDI.

![[session_1.WinSta0.Default.png]]
Видим много открытых окошек, выписываем флаг:
`TulaCTF{d0_y0u_533_th353_w1nd0w5}`

Почему `screenshot`? В таске идёт речь про много открытых окон. Самое простое, что хочется сделать, посмотреть на них.

Есть другие способы решения, которые вели к неверному флагу `TulaCTF{d0_yu0_533_th353_w1nd0w5}`, который можно найти в списке названий запущенных файлов. Впоследствии было решено считать это за флаг, т.к. это косяк автора.

Также вы могли заметить в дампе флаг `TulaCTF{d0_y0u_533_th15_w1nd0w5_4s_1_533}`, который по ошибке был завезён туда. Впоследствии было решено считать это за флаг, т.к. это тоже косяк автора.



# 4 Forensics | Hard | Синий ящик 3

## Информация
Одним прекрасным вечером, почитывая книжку под названием `Sherlock Holmes`, вы слышете стук в дверь. Это снова ваш дед решил заглянуть к вам на чай. Заметив книгу, на него снизошло озарение, что тот человек был писателем и очень любил это произведение. Правда дальше продвинутого блокнота он не смог уйти, потому что тогда ещё не было таких мощностей и финансов.

## Решение
[Скачиваем](https://github.com/volatilityfoundation/volatility) и открываем volatility версии 2.6.x или 3.х (в решении 2.6.1 на python 2.7) . Подбираем профиль (imagescan или ручками угадываем). Используем плагин `pslist`. 
`py -2.7 vol.py -f WIN-DSEVI9OLA8P-20221202-090030.raw --profile Win7SP1x64 pslist`
Получаем:
```
Volatility Foundation Volatility Framework 2.6.1                                                                                                                                             Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                                                                      ------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------                                            0xfffffa8001890b00 System                    4      0     96      487 ------      0 
...................................
0xfffffa8001ca0190 notepad++.exe          1516   1700      2       78      1      0                                                                             
..........................
```
Слова "продвинутый блокнот" должны натолкнуть на процесс `notepad++.exe`. Дампим его.
`py -2.7 vol.py -f WIN-DSEVI9OLA8P-20221202-090030.raw --profile Win7SP1x64 memdump -p 1516 --dump-dir .`
Получаем на выходе дамп памяти процесса. Ищем в нём слова `Sherlock Holmes`. Находим вот такую строчку:
![[Pasted image 20221204235836.png]]
Если поискать слова, стоящие после `Sherlock Holmes`, можно найти точно такой же блок данных, но "более полный".
![[Pasted image 20221205000012.png]]
Среди этого текста можно заметить зашифрованный флаг: `ZSNAHZL{E3M3MB3E_ZP4Z_T0Z3C4J_N34D3Q_ZE4H3Q}`
Понимаем, что это шифрование подстановкой, т.к. первые 7 букв можно легко восстановить в TULACTF. 
С помощью [CipherCracker](https://github.com/StevePaget/CipherCracker) получаем ключ `ABHJKLOPUIYNMTVCXEQZSDFRWG`.
`TulaCTF{r3m3mb3r_th4t_n0t3p4d_l34v3s_tr4c3s}`
