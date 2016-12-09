from flask import Flask, render_template
#from flask_jsonpify import jsonify
#import argparse
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)

values = {
    'slider1' : 25,
    'slider2' : 0
}

@app.route('/')
def index():
    return render_template('index.html', **values)

@socketio.on('value changed')
def value_changed(message):
    if ';' in message['data']:
        data = ['','']
        count = 0
        for c in message['data']:
            if c == ';':
                count += 1
            else:
                data[count] += c
        python_data = {
            'from' : data[0],
            'to' : data[1]
        }
        message['data'] = json.loads(json.dumps(python_data))
    values[message['who']] = message['data']
    print(message)
    emit('update value', message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
