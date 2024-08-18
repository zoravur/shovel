import socket
from pynput.keyboard import Controller
import sys

# set up socket
host_ip = '0.0.0.0'
host_port = 65432

keyboard = Controller()

# create a socket to listen for incoming connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host_ip, host_port))
    s.listen()

    # accept one connection and keep it open
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break  # connection closed by client
            key = data.decode('utf-8')

            sys.stdout.write(key)
            sys.stdout.flush()
            # simulate the keystroke on the host
            # if len(key) == 1:
            #     keyboard.press(key)
            #     keyboard.release(key)
            # else:
            #     # handle special keys if necessary
            #     pass

