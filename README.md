# Mercury
ПО для счетчиков Меркурий 200.2

# Сканер
Сканер адресов счетчиков Меркурий200

Подготовка:<br>
pip install modbus_crc<br>
pip install argparse<br>
pip install pyserial<br>
pip install struct<br>

Запуск linux:<br>
./Mercury200_scan.py /dev/ttyUSB0 9600 23 55<br>
<br>
Запуск в Windows:<br>
./Mercury200_scan.py COM5 9600 23 55<br>

Возмоджные параметры запуска:<br>
./Mercury200_scan.py <КОМ_ПОРТ> <СКОРОСТЬ> <НАЧ_НОМЕР_КВ> <ПОСЛЕДНИЙ_НОМЕР_КВ> <br>

Запуск без параметров сканирует номера от 1 до 1001

# Опрос

Подготовка:<br>
pip install modbus_crc<br>
pip install argparse<br>
pip install pyserial<br>
pip install struct<br>
pip install re<br>
pip install json<br>

Скрипт запускается с параметрами:<br>
./Mercury200.py <КОМ_ПОРТ> <СКОРОСТЬ> <АДРЕС> <ФОРМАТ><br>

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
