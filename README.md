# Mercury
ПО для счетчиков Меркурий

# Сканер
Сканер адресов счетчиков Меркурий200

Подготовка:<br>

<code>pip install modbus_crc<br>
pip install argparse<br>
pip install pyserial<br>
pip install struct<br></code>

Запуск linux:

./Mercury200.py /dev/ttyUSB0 9600 23 55

Запуск в Windows:

./Mercury200.py COM5 9600 23 55

# Опрос

Подготовка:

pip install modbus_crc<br>
pip install argparse<br>
pip install pyserial<br>
pip install struct<br>
pip install re<br>
pip install json<br>

Скрипт запускается с параметрами

<КОМ_ПОРТ> /dev/ttyUSB0 или для Windows COM1<br>
<СКОРОСТЬ> стандартные скорости портов, по умолчанию 9600<br>
<АДРЕС> адрес счетчика по умолчанию - 0 , можно указывать следующие форматы, 6 последних цифр серийного номера, в формате Наладчик+ kv123<br>
<ФОРМАТ> в каком формате выдавать данные csv или json, по умолчанию json<br>

Запуск linux:

./Mercury200.py /dev/ttyUSB0 9600 512230<br>
./Mercury200.py /dev/ttyUSB0 9600 kv125<br>
./Mercury200.py /dev/ttyUSB0 9600 kv125 csv<br>
./Mercury200.py /dev/ttyUSB0 9600 kv125 json<br>


Запуск в Windows:

./Mercury200.py COM1 9600 512230<br>
./Mercury200.py COM1 9600 kv125<br>
./Mercury200.py COM1 9600 kv125 csv<br>
./Mercury200.py COM1 9600 kv125 json<br>
