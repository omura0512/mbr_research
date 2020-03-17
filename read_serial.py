import serial
import sys
import os
import datetime

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

if len(sys.argv) == 2 and sys.argv[1] == 'test':
    PATH_LOG_FILE = './raw_data/test.csv'
    os.remove(PATH_LOG_FILE)
elif len(sys.argv) == 4:
    PATH_LOG_FILE = './raw_data/raw_type' + sys.argv[1] + '_blower_' + sys.argv[2] + '%_rotation_' + sys.argv[3] + '%.csv'
else:
    print('You need 3 args: [type] [blower] [rotatinal speed]')
    sys.exit()

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout = None)
for i in range(5):
    ser.readline() # discard initial data

while True:
    line = ser.readline().decode('utf-8')
    dt_now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(PATH_LOG_FILE, 'a')  as f:
        print(dt_now + ',' + line, end="")
        print(dt_now + ',' + line, end="", file=f)
