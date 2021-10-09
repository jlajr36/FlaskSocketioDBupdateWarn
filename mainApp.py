from flask import Flask, render_template, request
import sqlite3 as sql, os
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kabwV6RD'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        rows = []
        try:
            newnum = request.form['theNum']
            with sql.connect('numbers.db') as con:
                cur = con.cursor()
                if newnum != '':
                    cur.execute("INSERT INTO nums (num) VALUES (?)", (newnum,))
                    con.commit()
                cur.execute("SELECT * from nums")
                rows = cur.fetchall()
        except:
            print('DB write error')
            con.rollback()
        finally:
            con.close()
            return render_template('index.html', rows=rows)
    else:
        rows = []
        try:
            with sql.connect('numbers.db') as con:
                cur = con.cursor()
                cur.execute("SELECT * from nums")
                rows = cur.fetchall()
        except:
            print('DB read error')
            con.rollback()
        finally:
            con.close()
            return render_template('index.html', rows=rows)

if __name__ == "__main__":
    #Make current dir working directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    socketio.run(app, host='0.0.0.0', debug='True')