import serial
import mysql.connector
from datetime import datetime
import yaml
import time

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
        "Select people.ID, people.NAME, tb.COVID, tb.TIME, tb.LOCATION from tb, people Where tb.ID=people.ID ORDER BY tb.TIME")
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
    try:
        str2 = data.split()
        push(str2[0], str2[1], datetime.now(), LOCATION)
    except:
        pass
        
# process("")
# exit()

# push(48, 'T', datetime.now(), LOCATION)
# time.sleep(1)
# push(2, 'F', datetime.now(), LOCATION)
# time.sleep(1)
# push(43, 'T', datetime.now(), LOCATION)
# time.sleep(1)
# push(5, 'T', datetime.now(), LOCATION)


cursor.execute("UPDATE people SET NAME='CHEN-AN LIN' WHERE ID=42")
mysql_connection.commit()
exit()


ser = serial.Serial(COM_PORT, BAUD_RATES)
try:
    while True:
        received_data = ser.read()  # read serial port
        time.sleep(0.03)
        data_left = ser.inWaiting()  # check for remaining byte
        received_data += ser.read(data_left)
        process(received_data)

except KeyboardInterrupt:
    ser.close()
    print('terminate')
