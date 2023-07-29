# Mercury
ПО для счетчиков Меркурий

# Сканер
Сканер адресов счетчиков Меркурий200

Подготовка:

pip install modbus_crc

pip install argparse

pip install pyserial

pip install struct

Запуск linux:

./Mercury200.py /dev/ttyUSB0 9600 23 55

Запуск в Windows:

./Mercury200.py COM5 9600 23 55

# Опрос
Скрипт запускается с параметрами,
<КОМ_ПОРТ> /dev/ttyUSB0 или для Windows COM1
<СКОРОСТЬ> стандартные скорости портов, по умолчанию 9600
<АДРЕС> адрес счетчика по умолчанию - 0 , можно указывать следующие форматы, 6 последних цифр серийного номера, в формате Наладчик+ kv123 
<ФОРМАТ> в каком формате выдавать данные csv или json, по умолчанию json 

Запуск linux:

 ./Mercury200.py /dev/ttyUSB0 9600 512230
 
 ./Mercury200.py /dev/ttyUSB0 9600 kv125
 
 ./Mercury200.py /dev/ttyUSB0 9600 kv125 csv
 
 ./Mercury200.py /dev/ttyUSB0 9600 kv125 json


Запуск в Windows:

 ./Mercury200.py COM1 9600 512230
 
 ./Mercury200.py COM1 9600 kv125
 
 ./Mercury200.py COM1 9600 kv125 csv
 
 ./Mercury200.py COM1 9600 kv125 json
