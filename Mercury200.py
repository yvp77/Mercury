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
# pip install re
# pip install json
#
# Скрипт для удаленного снятия показаний со счетчиков Меркурий 200.2Т
# запуск ./Mercury200.py /dev/ttyUSB0 <скорость_порта> <адрес_счетчика>
# <скорость_порта> - 9600,19200, и т.д.
# <адрес_счетчика> последние 6 цифр серийного номера, или в формате Наладчик+ kv<NNN>, где <NNN> номер квартиры/дома
#
# Примеры linux:
# ./Mercury200.py /dev/ttyUSB0 9600 512230
# ./Mercury200.py /dev/ttyUSB0 9600 kv125
# ./Mercury200.py /dev/ttyUSB0 9600 kv125 csv
# ./Mercury200.py /dev/ttyUSB0 9600 kv125 json
#
#
#
# Примеры Windows:
# ./Mercury200.py COM1 9600 512230
# ./Mercury200.py COM1 9600 kv125
# ./Mercury200.py COM1 9600 kv125 csv
# ./Mercury200.py COM1 9600 kv125 json

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
import datetime
import re
import modbus_crc
import json

from modbus_crc import add_crc

# Parse args
parser = argparse.ArgumentParser(
		description='Опрос данных счетчика Меркурий 200.2',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('serial',  nargs='?', default='/dev/ttyUSB0', help='COM-порт. Пример linux: /dev/ttyUSB0 Пример Windows: COM1')
parser.add_argument('baudrate',  nargs='?', default='9600', help='Скрость COM порта')
parser.add_argument('dev_sn',  nargs='?', default='0', help='Серийный номер счетчика, последние 6 цифр серийного номера, либо в формате Наладчик+ kv<NNN>, например kv125')
parser.add_argument('format',  nargs='?', default='csv', help='Формат вывода данных csv или json')
parser.add_argument('info',  nargs='?', default='noinfo', help='Показать дополнительную информацию')
args = parser.parse_args()


intext = args.dev_sn
format = args.format
info = str(args.info)

if re.search('kv', intext): # Проверяем текст на то что он начинается с символов kv
   print('Адрес введен в формате Наладчик+') if info=='info' or format=='info' else ''
#Отрезаем первые два символа
   number = intext[2:]
   print('Номер квартиры/дома:',number) if info=='info' or format=='info' else ''
#Расчитываем адрес наладчик+
   addr = ((8*int(number))+3)+4194304000

else:
   print('Введен класический адрес') if info=='info' or format=='info' else ''
   addr = intext


com = args.serial
baudrate=args.baudrate
addr = int(addr)
#insn = int(args.dev_sn)
addr_hex = hex(int(addr)).split('x')[-1]
print ('Cетевой адрес:',addr,'HEX адрес:',addr_hex) if info=='info' or format=='info' else ''
# Открываем порт с параметрами
ser = serial.Serial(com, baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
print ('Подключение через',com,':', ser.isOpen()) if info=='info' or format=='info' else ''

# There are commands for get different data:

# \x21 - HEX, 33  - DEC self time
# \x2b - HEX, 43  - DEC datetime input power down
# \x2c - HEX, 44  - DEC datetime input power up
# \x2f - HEX, 47  - DEC serial number
# \x66 - HEX, 103 - DEC date productions
# \x63 - HEX, 99  - DEC get U,I,P
# \x29 - HEX, 41  - DEC battery U
# \x27 - HEX, 39  - DEC expended electricity distributed according to tariffs

# More information you can get there: http://www.incotexcom.ru/doc/M20x.rev2015.02.15.pdf
#chunk += b'\x27'


# Send data формирование и запрос серийного номера
cmd = 47
chunk = struct.pack('>LB',addr,cmd)
signed_package = add_crc(chunk)
ser.write(signed_package)
time.sleep(0.12)
out = ser.read_all()
print ('Результат сер. номер HEXResult:', ':'.join('{:02x}'.format(c) for c in out)) if info=='info' or format=='info' else ''
sn = ''.join('{:02x}'.format(c) for c in out[5:9])
#t2 = ''.join('{:02x}'.format(c) for c in out[9:13])
#t3 = ''.join('{:02x}'.format(c) for c in out[13:17])
#t4 = ''.join('{:02x}'.format(c) for c in out[17:21])






# Send data формирование и запрос расхода по тарифам
cmd2 = 39
chunk2 = struct.pack('>LB',addr,cmd2)
signed_package2 = add_crc(chunk2)
ser.write(signed_package2)
time.sleep(0.12)
out = ser.read_all()
print ('Результат по тарифам HEXResult:', ':'.join('{:02x}'.format(c) for c in out)) if info=='info' or format=='info' else ''
t1 = ''.join('{:02x}'.format(c) for c in out[5:9])
t2 = ''.join('{:02x}'.format(c) for c in out[9:13])
t3 = ''.join('{:02x}'.format(c) for c in out[13:17])
t4 = ''.join('{:02x}'.format(c) for c in out[17:21])




# Send data формирование и запрос мгновенных значений P U I
cmd3 = 99
chunk3 = struct.pack('>LB',addr,cmd3)
signed_package3 = add_crc(chunk3)
ser.write(signed_package3)
time.sleep(0.12)
out = ser.read_all()
print ('Результат мгновенных HEXResult:', ':'.join('{:02x}'.format(c) for c in out)) if info=='info' or format=='info' else ''
u = ''.join('{:02x}'.format(c) for c in out[5:7])
i = ''.join('{:02x}'.format(c) for c in out[7:9])
p = ''.join('{:02x}'.format(c) for c in out[9:12])




# Send data формирование и запрос напряжения батарейки
cmd4 = 41
chunk4 = struct.pack('>LB',addr,cmd4)
signed_package4 = add_crc(chunk4)
ser.write(signed_package4)
time.sleep(0.12)
out = ser.read_all()
print ('Результат Батарейка  HEXResult:', ':'.join('{:02x}'.format(c) for c in out)) if info=='info' or format=='info' else ''
uBat = ''.join('{:02x}'.format(c) for c in out[5:7])



# Send data формирование и запрос даты пропадания питания
cmd5 = 43
chunk5 = struct.pack('>LB',addr,cmd5)
signed_package5 = add_crc(chunk5)
ser.write(signed_package5)
time.sleep(0.12)
out = ser.read_all()
print ('Пропадание питания   HEXResult:', ':'.join('{:02x}'.format(c) for c in out)) if info=='info' or format=='info' else ''
#DOW День недели 0-воскресенье, 1-понедельник,....., 6-суббота, 7-праздник
pd_dow = ''.join('{:02x}'.format(c) for c in out[5:6])
pd_hh = ''.join('{:02x}'.format(c) for c in out[6:7])
pd_mm = ''.join('{:02x}'.format(c) for c in out[7:8])
pd_ss = ''.join('{:02x}'.format(c) for c in out[8:9])
pd_dd = ''.join('{:02x}'.format(c) for c in out[9:10])
pd_mon = ''.join('{:02x}'.format(c) for c in out[10:11])
pd_yy = ''.join('{:02x}'.format(c) for c in out[11:12])
pd_yy = int(pd_yy)+2000
power_down=(datetime.datetime(int(pd_yy),int(pd_mon),int(pd_dd),int(pd_hh),int(pd_mm),int(pd_ss)).timestamp())


# Send data формирование и запрос даты появления питания
cmd6 = 44
chunk6 = struct.pack('>LB',addr,cmd6)
signed_package6 = add_crc(chunk6)
ser.write(signed_package6)
time.sleep(0.12)
out = ser.read_all()
print ('Появилось питание    HEXResult:', ':'.join('{:02x}'.format(c) for c in out)) if info=='info' or format=='info' else ''
#DOW День недели 0-воскресенье, 1-понедельник,....., 6-суббота, 7-праздник
pu_dow = ''.join('{:02x}'.format(c) for c in out[5:6])
pu_hh = ''.join('{:02x}'.format(c) for c in out[6:7])
pu_mm = ''.join('{:02x}'.format(c) for c in out[7:8])
pu_ss = ''.join('{:02x}'.format(c) for c in out[8:9])
pu_dd = ''.join('{:02x}'.format(c) for c in out[9:10])
pu_mon = ''.join('{:02x}'.format(c) for c in out[10:11])
pu_yy = ''.join('{:02x}'.format(c) for c in out[11:12])
pu_yy = int(pu_yy)+2000
power_up=(datetime.datetime(int(pu_yy),int(pu_mon),int(pu_dd),int(pu_hh),int(pu_mm),int(pu_ss)).timestamp())



# Закрываю подключение к КОМ-порту
ser.close()


#Вывод данных
print ('Считан серийный номер SN:',int(sn,16)) if info=='info' or format=='info' else ''
print ('Питание пропадало: ',pd_dd,'.',pd_mon,'.',pd_yy,' в ',pd_hh,':',pd_mm,':',pd_ss,'; Unixtime=',int(power_down), sep='') if info=='info' or format=='info' else ''
print ('Питание появилось: ',pu_dd,'.',pu_mon,'.',pu_yy,' в ',pu_hh,':',pu_mm,':',pu_ss,'; Unixtime=',int(power_up), sep='') if info=='info' or format=='info' else ''
print ('Напряжение батарейки: ',int(uBat)*0.01,' В', sep='') if info=='info' or format=='info' else ''


sn = int(sn,16)
t1 = float('{:.2f}'.format(int(t1)*0.01))
t2 = float('{:.2f}'.format(int(t2)*0.01))
t3 = float('{:.2f}'.format(int(t3)*0.01))
t4 = float('{:.2f}'.format(int(t4)*0.01))
u = float('{:.2f}'.format(int(u)*0.1))
i = float('{:.2f}'.format(int(i)*0.01))
p = (int(p))
uBat= float('{:.2f}'.format(int(uBat)*0.01))
power_down = int(power_down)
power_up = int(power_up)


if format == 'csv':

   print ('  Сер.номер','Тариф_Т1','Тариф_Т2','Тариф_Т3','Т4','Напряжение','Ток','Мощность','Бат','ПропалоПИТ','ПоявилосьПИТ',sep=';')
   # Формат чисел  print('{:.2f}'.format(2323.12345) обрезает до 2-х знаков после .
   print ('Mercury',sn,t1,t2,t3,t4,u,i,p,uBat,power_down,power_up,sep=';')

else:

   print(json.dumps({"Mercury": {intext: {"data": {"sn": sn,"Tarif_T1":t1,"Tarif_T2":t2,"Tarif_T3":t3,"Tarif_T4":t4,"U":u,"I":i,"P":p,"uBat":uBat,"powerDown":power_down,"powerUp":power_up}}}}))
