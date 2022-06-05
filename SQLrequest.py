import serial
import mysql.connector
from datetime import datetime
import yaml


# =======parameter========
COM_PORT = '/dev/ttyACM1'
BAUD_RATES = 115200
LOCATION = 'RPi_1_location'
# ========================

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)

mysql_connection = mysql.connector.connect(
    host=db['mysql_host'],
    user=db['mysql_user'],
    password=db['mysql_password'],
    database=db['mysql_db']
)

cursor = mysql_connection.cursor()

# push a new data
def push(id, covid, time, location):
    cursor.execute(
        'INSERT INTO tb(ID, COVID, TIME, LOCATION) VALUES (%s, %s, %s, %s)', (id, covid, time, location))
    mysql_connection.commit()

# clear table
def clear():
    cursor.execute('truncate table tb')

# fetch all data in tb
def seeall():
    cursor.execute(
        "Select people.ID, people.NAME, tb.COVID, tb.TIME, tb.LOCATION from people,tb Where people.ID = tb.ID")
    for x in cursor:
        print(x)

# delete table
def delete():
    cursor.execute('DROP TABLE tb')

# create table
def create():
    cursor.execute(
        "CREATE TABLE tb (ID int NOT NULL, COVID enum('T', 'F'), TIME datetime NOT NULL, LOCATION varchar(255) NOT NULL)")



def process(data):
    str2 = data.split()
    push(str2[0], str2[1], datetime.now(), LOCATION)


ser = serial.Serial(COM_PORT, BAUD_RATES)
try:
    while True:
        while ser.in_waiting:
            data_raw = ser.readline()
            data = data_raw.decode()
            print('get data: ', data)
            process(data)

except KeyboardInterrupt:
    ser.close()
    print('terminate')
