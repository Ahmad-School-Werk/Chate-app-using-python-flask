from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheime_sleutel'
socketio = SocketIO(app)

# Een eenvoudige lijst om de chatberichten op te slaan
messages = {}

@app.route('/')
def index():
    return render_template('index.html', groups=messages.keys())

@app.route('/create_group', methods=['POST'])
def create_group():
    group_name = request.form['group_name']
    password = request.form['password']

    if group_name not in messages:
        messages[group_name] = []
        return redirect(url_for('chat', group=group_name, password=password))
    else:
        return "Groepsnaam bestaat al."

@app.route('/chat/<group>/<password>')
def chat(group, password):
    if group not in messages:
        return redirect(url_for('index'))

    return render_template('chat.html', group=group, password=password)

@socketio.on('join_room')
def handle_join_room(data):
    username = data['username']
    group = data['group']
    join_room(group)
    emit('message', {'msg': username + ' heeft de chat betreden.', 'username': 'Systeem'}, room=group)

@socketio.on('leave_room')
def handle_leave_room(data):
    username = data['username']
    group = data['group']
    leave_room(group)
    emit('message', {'msg': username + ' heeft de chat verlaten.', 'username': 'Systeem'}, room=group)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    msg = data['msg']
    group = data['group']
    messages[group].append({'username': username, 'msg': msg})
    emit('message', {'msg': msg, 'username': username}, room=group)

if __name__ == '__main__':
    socketio.run(app, debug=True)
