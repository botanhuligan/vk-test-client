#!/bin/env python
from flask_socketio import emit
from client import create_app, socketio
app = create_app(debug=True)
socketio.run(app, host='0.0.0.0', port=9081)

if __name__ == "__main__":
    pass