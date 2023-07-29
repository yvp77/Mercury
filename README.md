# Mercury
ПО для счетчиков Меркурий

# Сканер
Сканер адресов счетчиков Меркурий200

Подготовка:
pip install modbus_crc \r\n
pip install argparse
pip install pyserial
pip install struct

Запуск linux:
./Mercury200.py /dev/ttyUSB0 9600 23 55

Запуск в Windows:
./Mercury200.py COM5 9600 23 55
