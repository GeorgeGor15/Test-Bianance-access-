# Test-Bianance-access-
It's a small part of code to connect to API Binance and check balances

Project created on Python 3.10.0, Windows 10

EN: It's a small part of the code that implements:
1. access (data reading) to Binance via API, 
2. Reading personal (your accaunt) and shared data from Binance,
3. Working with tkinter widgets: Label, Button, Text, Treeview, Listbox, Scrollbar;
4. Updating Treeview fields with frequent data updates
5. Creating a timer by running a parallel deamon process
    
Binance module is taken from https://github.com/Bablofil/binance-api with few adds

You should save "Futures Watcher.py" and "binance_api.py" in same directory.<BR>
You should enter in Text correct API_KEY and API_SECRET before press "Start" button.

RU: Это небольшая часть кода в которой реализованы:
1. Доступ (считывание данных) к бирже Binance через API,
2. Считывание личных данных (данных своего аккаунта) и общих данных с биржи Binance,
3. Работа с виджетами Tkinter: Label, Button, Text, Treeview, Listbox, Scrollbar;
4. Обновление полей Treeview при частом обновлении данных,
5. Создание таймера путем запуска параллельного Deamon процесса.
    
Модуль Binance взят из https://github.com/Bablofil/binance-api с небольшими дополнениями

Файлы "Futures Watcher.py" и "binance_api.py" должны быть сохранены в одной папке.<BR>
Следует ввести в соответствующие текстовые поля коректные API_KEY и API_SECRET перед тем, как нажать кнопку "Start".
    
## Code<BR>
#### Architecture:
    
2 files: "binance_api.py" - for requests Binance API, "Futures Watcher.py" - Tkinter gui
    
#### "Futures Watcher.py" architecture:
    
1. import modules<BR>
2. global const<BR>
3. class timer_BTCUSDT: - Deamon Thread as Timer<BR>
    3.1 check is Timer should run or stop<BR>
    3.2 check if Timer just started is APIs correct<BR>
    3.3 if TImers isn't just started then pause (time.sleep(0.5))<BR>
    3.4 Reading BTC/USDT kllines and calculate low and high price for the last 5 minutes<BR>
    3.5 Reading account and balances<BR>
    3.6 Reading Futures positions. Reload data in Listbox. Load/update data in Treeview<BR>
4. def click_button_Timer(): - Click button Start/Stop<BR>
5. class gui: - GUI<BR>
    5.1 def __init__(self, window): -  - Load Tkinter widgets<BR>
    5.2 def Sys_Msg(self,text1): -  - Insert test in to Text box<BR>
6. SET GUI<BR>
7. SET Bot and test connect to Binance<BR>
8. def config(event): - window resize event<BR>
    
#### Inside the code:    
```Python
#dependencies "Futures Watcher.py": 
from tkinter import *
import threading
import time
import datetime

#dependencies "binance_api.py": 
import ssl
import time
import json
import urllib
import hmac, hashlib
import requests

from urllib.parse import urlparse, urlencode
from urllib.request import Request, urlopen
```
<BR>
    
```Python
#Binance API:
    #private const
API_KEY_Str = str(app.text_AK.get(1.0,'end-1c'))
API_SECRET_Str = str(app.text_AS.get(1.0,'end-1c'))

    #reading private data
    #data to display user balances and Futures positions
myListAcc = bot.account()
BnFAcc = bot.futuresBalance()
BnFAcc = bot.futuresAccount()
BnFAcc=bot.userPositionInfo()
    
    #reading non-private data
    #get last 5 1minute klines BTC/USDT Spot pare
myTupSpK =('klines', bot.klines(symbol='BTCUSDT', interval='1m', limit=5)) #Tupl
    #get last 5 1minute klines BTC/USDT Futures pare
myTupFtK = ('futuresKlines', bot.futuresKlines(symbol='BTCUSDT', interval='1m', limit=5)) #tupl
    #get 5 orders from Order Book BTC/USDT Spot pare
myTup_DSp = ('depth', bot.depth(symbol='BTCUSDT', limit=5)) #tupl
    #get 5 orders from Order Book BTC/USDT Futures pare
myTup_DFt = ('FutDepth', bot.futuresDepth(symbol='BTCUSDT', limit=5)) #tupl

```
    
```Python
#Threading:
    #should timer work or not const
PS_BU = True
should_run_BU = True
    #run timer
timer_BU = threading.Thread(target=timer_BTCUSDT,daemon=True)
timer_BU.start()

```
        

## Window<BR>
![window](https://user-images.githubusercontent.com/95641997/144902786-5c11f9d9-83d5-46e6-b925-84c7b127e8d4.jpg)

## Contributions are welcome<BR>
No donation or anything is needed at all, but if you found the code useful, I'll leave a few of my addresses below:<BR>
<BR>
XRP (Ripple): rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh, MEMO: 108338326<BR>
WAVES: 3P3SMBtuJLf5NaNM75sNVYycW2SUUPGhDdp
