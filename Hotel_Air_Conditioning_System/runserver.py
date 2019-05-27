"""
This script runs the Hotel_Air_Conditioning_System application using a development server.
"""

from os import environ
from Hotel_Air_Conditioning_System import app
from Hotel_Air_Conditioning_System.dao import mapper
from Hotel_Air_Conditioning_System.impl import ServicePool,Service,Schedule



if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
