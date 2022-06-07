from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    result = cur.execute(
        "Select people.ID, people.NAME, tb.COVID, tb.TIME, tb.LOCATION from tb, people Where tb.ID=people.ID ORDER BY tb.TIME")
    if result > 0:
        data = cur.fetchall()
        return render_template('index.html', data=data)


@app.route('/realtime')
def new():
    cur = mysql.connection.cursor()
    result = cur.execute(
        "Select people.ID, people.NAME, tb.COVID, tb.TIME, tb.LOCATION from tb, people Where tb.ID=people.ID ORDER BY tb.TIME desc limit 1")
    if result > 0:
        data = cur.fetchall()
        return render_template('realtime.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
