#import keyboard
from pykeyboard import PyKeyboard
import time
import os

k = PyKeyboard()
#scenes = {"1": "shift+1", "2": "shift+2", "3": "shift+3"}
scenes = {"1": ["shift","1"], "2": ["shift","2"], "3": ["shift","3"]}
transition = "shift+t"

dwell = 4



time.sleep(4)
while True:
    for scene in scenes:
        print(scenes[scene])
        # obs studio hotkeys only work when the window has focus
        os.system('xdotool search "OBS Studio" | xargs xdotool windowactivate')
        #keyboard.press_and_release(scenes[scene])
        #keyboard.press_and_release(transition)
        k.press_keys([k.shift_key, scenes[scene][1]])
        k.press_keys([k.shift_key, 't'])
        time.sleep(dwell)
