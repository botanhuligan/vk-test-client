from flask import redirect, url_for, render_template
from flask_socketio import emit

from . import main
from .forms import LoginForm
from flask import request, session
from datetime import datetime


ROOM = "ChatBot"


@main.route('/say', methods=['POST'])
def post():
    rq = request.json
    request.__dict__['namespace'] = '/chat'
    time = datetime.now().strftime('%H:%M:%S')
    emit('message', {'msg': time + ' ANSWER to user <' + rq["user_id"] + '>:  ' + rq["message_text"]}, room=ROOM)
    return 'OK'


@main.route('/log', methods=['POST'])
def log():
    rq = request.json
    user = rq['user_id']
    log_text = rq['log']
    request.__dict__['namespace'] = '/chat'
    time = datetime.now().strftime('%H:%M:%S')
    emit('logs', {'msg': time + " " + user + ": " + log_text}, room=ROOM)
    return 'OK'


@main.route('/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')

    return render_template('index.html', form=form)


@main.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    if name == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=ROOM)
