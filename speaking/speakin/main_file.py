import tkinter as tk
from utility import bind_keys, setTEXTBG, setTEXT, setBGImage, unbind_keys, bind_gpio_pins, unbind_gpio_pins, \
    panic_audio
from SM import SavedMessagesPage
from STT import STTPage
from HMI import ImagesToSpeechPage
from TTS import TTSPage


class HomePage:

    def __init__(self, root):
        self.root = root
        self.pin_functions = {
            19: self.open_tts_functionality,
            6: self.open_stt_functionality,
            13: self.open_images_to_speech_functionality,
            3: self.open_saved_messages_functionality,
            16: self.quit_application
        }
        self.setup_attributes()

    def setup_attributes(self):
        self.root.title("Speaking Glove")
        self.root.attributes("-fullscreen", True)
        self.bind_gpio()
        setBGImage(
            "images/home.png",
            self.root)
        self.root.focus_force()

    def bind_gpio(self):
        bind_gpio_pins(self.pin_functions)

    def open_tts_functionality(self, channel):
        unbind_gpio_pins(self.pin_functions)
        TTSPage(self)

    def open_stt_functionality(self, channel):
        print("11")
        # unbind_gpio_pins(self.pin_functions)
        print("22")
        STTPage(self)

    def open_images_to_speech_functionality(self, channel):
        unbind_gpio_pins(self.pin_functions)
        ImagesToSpeechPage(self)

    def open_saved_messages_functionality(self, channel):
        unbind_gpio_pins(self.pin_functions)
        SavedMessagesPage(self)

    def quit_application(self, channel):
        unbind_gpio_pins(self.pin_functions)
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    home_page = HomePage(root)
    root.mainloop()
