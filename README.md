# Mercury
Скрипт для опроса счетчиков Меркурий 200.2<br>

git clone https://github.com/yvp77/Mercury.git


# Сканер
Сканер адресов CAN шины счетчиков Меркурий200 зашифрованных ПО Наладчик+

Подготовка:<br>
pip install modbus_crc<br>
pip install argparse<br>
pip install pyserial<br>
pip install struct<br>

Запуск linux:<br>
./Mercury200_scan.py -h<br>
./Mercury200_scan.py /dev/ttyUSB0 9600 23 55<br>
<br>
Запуск в Windows:<br>
./Mercury200_scan.py -h<br>
./Mercury200_scan.py COM5 9600 23 55<br>

Возможные параметры запуска:<br>
./Mercury200_scan.py -h<br>
./Mercury200_scan.py <КОМ_ПОРТ> <СКОРОСТЬ><br>
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

./Mercury200.py /dev/ttyUSB0 9600 123321<br>
./Mercury200.py /dev/ttyUSB0 9600 kv125<br>
./Mercury200.py /dev/ttyUSB0 9600 kv125 csv<br>
./Mercury200.py /dev/ttyUSB0 9600 kv125 json<br>


Запуск в Windows:

./Mercury200.py COM1 9600 123321<br>
./Mercury200.py COM1 9600 kv125<br>
./Mercury200.py COM1 9600 kv125 csv<br>
./Mercury200.py COM1 9600 kv125 json<br>

# Zabbix

Mercury200.py копируем в /etc/zabbix/scripts<br>
Файл mercury200.conf копируем в папку агента, пезепускаем агент

Импортируем шаблон, в шаблоне есть макросы:<br>
{$MODEM} - по умолчанию /dev/ttyUSB0<br>
{$SPEED} - по умолчанию 9600<br>
{$ADDRESS} - по умолчанию kv0<br>
{$FORMAT} - по умолчанию json<br>

обязательно добавьте пользователя zabbix в группу dialout<br>
adduser zabbix dialout

После создания хоста и привязки шаблона необходимо в макросах хоста указать требуемые вам значения



