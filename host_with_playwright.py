import socket
import signal
from playwright.sync_api import sync_playwright
import sys

host_ip = '0.0.0.0'
host_port = 65432
should_exit = False

def handle_keypress(page, key, motion: str ='Press'):
    if len(key) != 1:
        print(f'Invalid key: {key}')
        return
    if motion == 'Press':
        page.keyboard.down(key)
    elif motion == 'Release':
        page.keyboard.up(key)
    else:
        print(f'Invalid motion: {motion}')
    # else:
    #     # handle special keys if needed (e.g., arrow keys, enter)
    #     pass

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://example.com")  # replace with your game's URL
    page.bring_to_front()

    # set up a simple server to receive keystrokes
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host_ip, host_port))
        s.listen()

        def cleanup(signal_received, frame):
            global should_exit
            print('SIGINT or SIGTERM received. Closing server and browser.')
            # try:
            #     s.shutdown(socket.SHUT_RDWR)
            #     s.close()
            # except Exception as e:
            #     print(f'Error closing socket: {e}')
            # browser.close()
            should_exit = True

        # register the signal handlers
        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)

        s.settimeout(1)

        while True:
            try:
                conn, addr = s.accept()
                break
            except socket.timeout:
                pass
            if should_exit:
                break

        if should_exit:
            sys.exit(0)
            
        with conn:
            print('Connected by', addr)
            while True:
                try: 
                    data = conn.recv(1024)
                except socket.timeout:
                    if should_exit:
                        break
                    continue
                if not data:
                    break
                action = data.decode('utf-8').strip()
                motion, key, *rest = action.split(' ')
                handle_keypress(page, key, motion)
    



    browser.close()

with sync_playwright() as playwright:
    run(playwright)