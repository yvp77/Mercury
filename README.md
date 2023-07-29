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
