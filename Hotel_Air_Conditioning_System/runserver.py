"""
This script runs the Hotel_Air_Conditioning_System application using a development server.
"""

from os import environ
from Hotel_Air_Conditioning_System import app
from Hotel_Air_Conditioning_System.dao import mapper
from Hotel_Air_Conditioning_System.impl import ServicePool,Service,Schedule
from flask_apscheduler import APScheduler


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(HOST, PORT, debug=True)
    
