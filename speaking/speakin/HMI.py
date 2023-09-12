import tkinter as tk
import pyttsx3
import threading
from utility import bind_keys, setTEXTBG, setTEXT, setBGImage, unbind_keys, bind_gpio_pins


class ImagesToSpeechPage:
    def __init__(self, parent):
        self.parent = parent
        self.key_function_map_its = {
            '1': self.open_general_functionality,
            '2': self.open_emergency_functionality,
            '3': self.open_food_functionality,
            '4': self.open_travel_functionality,
            '5': self.open_family_functionality,
            '<Control_R>': self.go_back,
            '<Escape>': self.default_binding
            }
        self.its_setup_attributes()

    def its_setup_attributes(self):
        self.hmi_window = tk.Toplevel(self.parent.root)
        self.hmi_window.title("HMI-Viwer")
        self.hmi_window.attributes("-fullscreen", True)
        bind_keys(self.key_function_map_its, self.hmi_window)
        self.hmi_window.image_path = "images/images/main.png"
        setBGImage("images/images/main.png", self.hmi_window)
        self.hmi_window.focus_force()
        self.process_running = False
        print("why")

    def set_female_voice(self, engine, voice_index):
        voices = engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            engine.setProperty('voice', voices[voice_index].id)
        else:
            print("Invalid voice index.")

    def go_back(self):
        print('3')
        bind_gpio_pins(self.parent.pin_functions)
        self.hmi_window.destroy()


    def display_image(self, image_path):
        setBGImage(image_path, self.hmi_window)

    def display_icon_and_speak(self, icon, text_to_speak, image_after):
        self.display_image(icon)
        self.play_audio(text_to_speak)
        self.hmi_window.after(100, lambda: self.display_image(image_after))
        self.process_running = False

    def play_audio(self, text):
        engine = pyttsx3.init()
        #self.set_female_voice(engine, 1)
        engine.say(text)
        engine.runAndWait()

    def default_binding(self, event=None):
        # Reset the default bindings
        self.hmi_window.bind('1', self.open_general_functionality)
        self.hmi_window.bind('2', self.open_emergency_functionality)
        self.hmi_window.bind('3', self.open_food_functionality)
        self.hmi_window.bind('4', self.open_travel_functionality)
        self.hmi_window.bind('5', self.open_family_functionality)
        self.hmi_window.unbind('6')
        self.display_image(self.hmi_window.image_path)
        self.process_running = False

    def bind_speak(self, key, image1, text, image2):
        self.hmi_window.bind(key, lambda event: threading.Thread(target=self.display_icon_and_speak, args=(
        image1, text, image2)).start())

    def open_general_functionality(self, event=None):
        if not self.process_running:
            self.process_running = True
            threading.Thread(target=self.display_icon_and_speak,
            args=("images/images/general-icon.png", "general", "images/general.png")).start()
            self.hmi_window.unbind('5')
            self.hmi_window.unbind('6')
            self.bind_speak('1', "images/toilet-icon.png", "i   want   to   go   to   toilet", "images/general.png")
            self.bind_speak('2', "images/hungry-icon.png", "i am Hungry", "images/general.png")
            self.bind_speak('3', "images/sleepy-icon.png", "i   am   Sleepy", "images/general.png")
            self.bind_speak('4', "images/pain-icon.png", "i   am   in   Pain", "images/general.png")


    def open_emergency_functionality(self, event=None):
        if not self.process_running:
            self.process_running = True
            threading.Thread(target=self.display_icon_and_speak, args=("images/images/emergency-icon.png", "emergency", "images/emergency.png")).start()
            self.hmi_window.unbind('5')
            self.hmi_window.unbind('6')
            self.bind_speak('1', "images/policestation-icon.png", "call the Police", "images/emergency.png")
            self.bind_speak('2', "images/hospital-icon.png", "take me to the hospital", "images/emergency.png")
            self.bind_speak('3', "images/ambulanceicon.png", "call the Ambulance", "images/emergency.png")
            self.bind_speak('4', "images/firedept-icon.png", "call the Fire Force", "images/emergency.png")
    def open_food_functionality(self, event=None):
        if not self.process_running:
            self.process_running = True
            threading.Thread(target=self.display_icon_and_speak, args=("images/food-icon.png", "food", "images/food.png")).start()
            self.bind_speak('1', "images/water-icon.png", "i need a glass of water", "images/food.png")
            self.bind_speak('2', "images/tea-icon.png", "i would like some tea", "images/food.png")
            self.bind_speak('3', "images/juice-icon.png", "i would love some juice", "images/food.png")
            self.bind_speak('4', "images/breakfast-icon.png", "i would like some breakfast", "images/food.png")
            self.bind_speak('5', "images/lunch-icon.png", "i am ready to have lunch", "images/food.png")
            self.bind_speak('6', "images/dinner-icon.png", "i am in the mood for dinner", "images/food.png")

    def open_travel_functionality(self, event=None):
        if not self.process_running:
            self.process_running = True
            threading.Thread(target=self.display_icon_and_speak, args=("images/travel-icon.png", "travel", "images/travel.png")).start()
            self.hmi_window.unbind('5')
            self.hmi_window.unbind('6')
            self.bind_speak('1', "images/busstop-icon.png", "Bus Stop", "images/travel.png")
            self.bind_speak('2', "images/auto-icon.png", "Auto Rickshaw", "images/travel.png")
            self.bind_speak('3', "images/taxi-icon.png", "Taxi", "images/travel.png")
            self.bind_speak('4', "images/trainstation-icon.png", "take me to the Railway Station", "images/travel.png")
    def open_family_functionality(self, event=None):
        if not self.process_running:
            self.process_running = True
            threading.Thread(target=self.display_icon_and_speak, args=("images/family-icon.png", "family", "images/family.png")).start()
            self.bind_speak('1', "images/dad.png", "hi   dad", "images/family.png")
            self.bind_speak('2', "images/mom.png", "hi  mum me", "images/family.png")
            self.bind_speak('3', "images/brother.png", "hi    bro", "images/family.png")
            self.bind_speak('4', "images/sister.png", "hi    sis", "images/family.png")
            self.bind_speak('5', "images/grandpa.png", "hi    grandpa", "images/family.png")
            self.bind_speak('6', "images/grandma.png", "hi    grandma", "images/family.png")
