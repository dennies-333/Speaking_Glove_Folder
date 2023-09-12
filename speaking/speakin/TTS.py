import tkinter as tk
import subprocess
from utility import bind_keys, setTEXTBG, setTEXT, setBGImage, unbind_keys, bind_gpio_pins, unbind_gpio_pins, panic_audio


class TTSPage:
    def __init__(self, parent):
        self.parent = parent
        self.key_function_map_tts = {
            "<Control_R>": self.go_back,
            "<Control_L>": panic_audio
        }
        self.tts_pin_function = {
            3: self.speak_button_callback,
        }
        self.tts_setup_attributes()

    def tts_setup_attributes(self):
        self.tts_window = tk.Toplevel(self.parent.root)
        self.tts_window.title("Text-to-Speech")
        self.tts_window.attributes("-fullscreen", True)
        bind_gpio_pins(self.tts_pin_function)
        bind_keys(self.key_function_map_tts, self.tts_window)
        setTEXTBG(
           "images/back.png",
            self.tts_window
        )
        self.input_text = setTEXT(self.tts_window)
        self.tts_window.focus_force()
        self.input_text.focus_set()


    def speak_button_callback(self, channel):
        text = self.input_text.get("1.0", tk.END).strip()
        self.text_to_speech(text)

    def text_to_speech(self, text):
        #subprocess.call(["espeak-ng", "-v", "en+f3", "-s", "120", "-k", "0.8", text])
        subprocess.call(["espeak", "-v", "en+f3", "-s", "120","-k", "0.8","-p", "50", text])

    def go_back(self):
        print("back")
        unbind_gpio_pins(self.tts_pin_function)
        bind_gpio_pins(self.parent.pin_functions)
        self.tts_window.destroy()

