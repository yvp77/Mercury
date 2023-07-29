#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Mercury_remote, allows you to remotely receive data from an electricity meter
#
# Для работы необходимо установить модули
#
# pip install modbus_crc
# pip install argparse
# pip install pyserial
# pip install struct
#
# Скрипт для сканирования и поиска адресов счетчиков Меркурий 200
# запуск ./Mercury200_scan.py /dev/ttyUSB0 <скорость_порта> <первый_номер_кв> <последний_номер_кв>
# <скорость_порта> - 9600,19200, и т.д.
#
# Примеры linux:
# ./Mercury200.py /dev/ttyUSB0 9600 23 55
#
#
# Примеры Wondows:
# ./Mercury200.py COM5 9600 23 55
#
#
# ______________________________________________________________________________________
# Если у Вас адреса защифрованны  ПО Наладчик+ то их можно посчитать по формуле либо вводить в формате наладчика, например: kv125
# Расчет:
# номер счетчика = ((8*N)+3)+4194304000
# где N - это номер квартиры иди номер дома(если СНТ)
# можно быстро посчитать в Exel
#
# ______________________________________________________________________________________


import argparse
import serial
import struct
import time

from modbus_crc import add_crc

# Parse args
parser = argparse.ArgumentParser(
		description='Сканер адресов Наладчик+ для Меркурий 200.2',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('serial',  nargs='?', default='/dev/ttyUSB0', help='COM-порт. Пример linux: /dev/ttyUSB0 Пример Windows: COM1')
parser.add_argument('baudrate',  nargs='?', default='9600', help='Скрость COM порта')
parser.add_argument('num_top',  nargs='?', default='1', help='Начальный номер крвартиры')
parser.add_argument('num_end',  nargs='?', default='1001', help='Последний номер крвартиры')
args = parser.parse_args()


num_top = int(args.num_top)
num_end = int(args.num_end)
com = args.serial
baudrate=args.baudrate


print ('Диапазон сканирования: ',num_top,'-',num_end)
# Открываем порт с параметрами
ser = serial.Serial(com, baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
print ('Подключение через',com,':', ser.isOpen())



for i in range(num_top, num_end+1):

    addr = ((8*int(i))+3)+4194304000    # Расчитываем адрес наладчик+ по номеру квартиры
    cmd = 47                            # Команда запроса ссерийного номера счетчика в десятичном формате
    chunk = struct.pack('>LB',addr,cmd) # Формируем пакет для отправки в КОМ порт
    signed_package = add_crc(chunk)     # Контрольная сумма CRC14 MODBUS
    ser.write(signed_package)           # Отправляем пакет в КОМ порт
    time.sleep(0.2)                     # Ждем
    out = ser.read_all()                # Читаем из порта
    sn = ''.join('{:02x}'.format(c) for c in out[5:9])
# Параметры сообщение и подставляем в вывод для перевода строки
    message = '<<<--НАЙДЕН!!!'
    param1 = '\r\n' # Конец строки с переходом на новую строку
    param2 = False
    if not sn:                          #Если sn пусто, то принудительно ставим в 0
     sn = '0'
# Параметры собщения подставляем в вывод для печати в той же строке
     message = '-------'
     param1 = '\r' # Конец строки без перевода на новую
     param2 = True
# Выводим сообщение с параметрами назначенными ранее, в засисимости от того найден номер или нет
    print ('№ кв:',i,'Адрес Наладчик+:',addr, 'СерНомер:',int(sn,16),message, end=param1, flush=param2)


else:
       print()
       print('Сканирование окончено!', end='\r\n', flush=False);
       ser.close()
