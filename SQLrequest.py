import serial
import mysql.connector
from datetime import datetime
import yaml

COM_PORT = '/dev/ttyACM1'
BAUD_RATES = 115200

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)

mysql_connection = mysql.connector.connect(
    host=db['mysql_host'],
    user=db['mysql_user'],
    password=db['mysql_password'],
    database=db['mysql_db']
)

cursor = mysql_connection.cursor()

# push a new data
def push(id, covid, time):
    cursor.execute(
        'INSERT INTO tb(ID, COVID, TIME) VALUES (%s, %s, %s)', (id, covid, time))
    mysql_connection.commit()

# clear table
def clear():
    cursor.execute('truncate table tb')

# fetch all data in tb
def seeall():
    cursor.execute(
        "Select people.ID, people.NAME, tb.COVID, tb.TIME from people,tb Where people.ID = tb.ID")
    for x in cursor:
        print(x)

# delete table
def delete():
    cursor.execute('DROP TABLE tb')

# create table
def create():
    cursor.execute(
        "CREATE TABLE tb (ID int NOT NULL, COVID enum('T', 'F') NOT NULL, TIME datetime NOT NULL)")


# push(1, 'F', datetime.now())
# push(4, 'T', datetime.now())
# push(32, 'F', datetime.now())
# push('7', 'T', datetime.now())


def process(data):
    str2 = data.split()
    push(str2[0], str2[1], datetime.now())


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
