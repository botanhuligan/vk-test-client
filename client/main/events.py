import json

from flask import session, jsonify
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import requests
from datetime import datetime


def message_from_user(name, msg):
    return {
        "message_text": msg,
        "user_id": name
    }


headers = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    if "user_id" in message:
        session['name'] = message["user_id"]
        name = message["user_id"]
    else:
        name = session.get('name')

    join_room(name)
    emit('status', {'msg': name + ' has entered the room'}, room=session.get('name'))


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    if "user_id" in message:
        session['name'] = message["user_id"]
        name = message["user_id"]
    else:
        name = session.get('name')

    msg = message['msg']
    time = datetime.now().strftime('%H:%M:%S')

    emit('out', {'msg': time + " " + name + ': ' + msg}, room=session.get('name'))
    requests.post("http://back:9080/message",
                  json.dumps(message_from_user(name, msg)),
                  headers=headers)


@socketio.on('change_user', namespace='/chat')
def change_user(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    session["name"] = message['msg']
    emit('status', {'msg': session.get('name') + ' has entered the room'}, room=session.get('name'))


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    leave_room(session.get('name'))
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=session.get('name'))

