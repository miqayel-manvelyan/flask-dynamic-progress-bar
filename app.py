from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from random import random
from time import sleep


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key!'
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()


class ProgressThread(Thread):
    def __init__(self):
        self.delay = 1
        self._progress = 0
        super(ProgressThread, self).__init__()

    def test_function(self):
        self.progress = 1
        sleep(3)
        self.progress = 10
        sleep(3)
        self.progress = 50
        sleep(3)
        self.progress = 100

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        socketio.emit('progress', {'percent': self._progress}, namespace='/progress')

    def run(self):
        self.test_function()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/progress')
def test_connect():
    global thread

    if not thread.isAlive():
        print("Starting ProgressThread")
        thread = ProgressThread()
        thread.start()


if __name__ == '__main__':
    socketio.run(app, debug=True)
