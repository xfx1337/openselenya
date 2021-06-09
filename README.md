# openselenya

PROJECT IS DEPRECATED
ПРОЕКТ ЗАБРОШЕН



[EN]

Open Source version of selenya(trashazart) project. This project was created for csgorun casino game. It opens run in selenium browser implementation and actives promocodes from telegram channels. 

History: First version of project was released on win32api, but it was very awful and unstable, and in most time I use Linux that doesn't support win32api. And we started to work on selenya(selenium russia word-joke). And we just got tired of everyday fixing this code, because csgorun wasn't made for it. Everyday something was getting wrong like one account didn't active code. And we decided to share it in open-source.

Usage: it runs on python3. Requirements are: firefox web browser, selenium library and geckodriver(firefox implementation). All requirements are in file "requirements.txt".
For first: create file like *name*.csv. In that you write accounts data. It looks like:

username, password
verygoodacc,verygoodpasss
anotheracc,anotherpass

Create an application in telegram and create config file like test.cfg.

Run from sources: python selenya.py CONFIG ACCOUNTS

Run from windows build: selenya.exe CONFIG ACCOUTNS


And you can see some misc and other. dbg.py(dbg.exe) - program that can run when selenya is already started. You can execute python commands in real time for debugging.

debugger:
go COMMAND_HERE - return value of instruction
ex COMMAND_HERE - just execute command
sc X - screenshot browser, where X - number.

COMMAND_HERE - python code.

manual.py(manual.exe) - just give you to force active promocode in any time(e.g. you found promo not in telegram channel)

[RU]

Open Source версия Селени(trashazart). Этот проект был сделан для "казино" csgorun. Он работает через selenium(имплементация браузера для кода) и активирует промокоды из телеграмм каналов.

История: Первая версия проекта была сделана на win32api, но она была чертовски хуёвой и не стабильной, и в большинстве времени я использую линукс, который не поддерживает win32api. Мы начали работать над Селеней(созвучная шутка с selenium). И нам просто надоело каждый день чинить эту парашу, потому что играть на сайтах через webscrap - идиотизм. Каждый день что то шло не по плану. И мы решили выложить его в открытый доступ с исходным кодом.

Использование: работает на 3 питоне. "требования": firefox браузер, seleinum библиотека и geckodriver(firefox имплементация). Все названия библиотек и тд в файле "requirements.txt"
Для начала: создайте файл в стиле *название*.csv. В нём нужно указать данные аккаунтов. Выглядит так:

username, password
логин,пароль
логин2,пароль2

Создайте приложение в телеграмме и создайте конфиг как test.cfg.

Запуск из исходников: python selenya.pyt CONFIG ACCOUNTS

Запуск билда для винды - selenya.exe CONFIG ACCOUNTS


Также есть дополнения. dbg.py(dbg.exe) - дебаггер. Когда селеня уже запущен вы можете открывать его и исполнять любой код в том же потоке.

команды дебаггера:
go COMMAND_HERE - получить значение которое вернётся после исполнения
ex COMMAND_HERE - просто выполнить питон код без возращения значений
sc X - скриншот браузера, где X - его номер

COMMAND_HERE - питон код

manual.py(manual.exe) - позволяет вызвать активацию промокода в любое время(например если промо не скинули, но вы его знаете)
