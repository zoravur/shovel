from pynput import keyboard

def on_press(key):
    try:
        print(f'alphanumeric key {key.char} pressed')
    except AttributeError:
        print(f'special key {key} pressed')

def on_release(key):
    print(f'key {key} released')
    if key == keyboard.Key.esc:
        # stop listener
        return False

# collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()