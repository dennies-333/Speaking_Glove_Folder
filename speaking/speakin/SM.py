import tkinter as tk
from PIL import Image, ImageTk
import threading
from utility import bind_keys, setTEXTBG, setTEXT, setBGImage, unbind_keys, bind_gpio_pins, unbind_gpio_pins
import sounddevice as sd
import soundfile as sf
import pygame


class SavedMessagesPage:
    def __init__(self, parent):
        self.parent = parent
        self.key_function_map_sm = {
            "<Control_R>": self.go_back
        }
        self.sm_pin_functions = {
            19: self.show_text_files,
            6: self.show_audio_files
        }
        self.sm_setup_attributes()

    def sm_setup_attributes(self):
        self.sm_window = tk.Toplevel(self.parent.root)
        self.sm_window.attributes("-fullscreen", True)
        bind_gpio_pins(self.sm_pin_functions)
        bind_keys(self.key_function_map_sm, self.sm_window)
        setBGImage("images/saved_message.png", self.sm_window)
        self.sm_window.focus_force()

    def go_back(self):
        unbind_gpio_pins(self.sm_pin_functions)
        unbind_keys(self.key_function_map_sm, self.sm_window)
        bind_gpio_pins(self.parent.pin_functions)
        self.sm_window.destroy()

    def show_text_files(self, event=None):
        unbind_gpio_pins(self.sm_pin_functions)
        unbind_keys(self.key_function_map_sm, self.sm_window)
        self.sm_window.destroy()
        TextViewer(self)

    def show_audio_files(self, event=None):
        unbind_gpio_pins(self.sm_pin_functions)
        unbind_keys(self.key_function_map_sm, self.sm_window)
        self.sm_window.destroy()
        AudioViewer(self)


"""class AudioViewer:
    CHUNK = 1024
    FORMAT = 'wav'
    CHANNELS = 1

    def __init__(self, parent):
        self.parent = parent
        print("audio_viewer")

        self.key_function_map_audio = {
            '1': self.show_audio_file1,
            '2': self.show_audio_file2,
            '3': self.show_audio_file3,
            '4': self.show_audio_file4,
            "<Control_R>": self.go_back
        }
        self.gpio_map_edit = {
            6: self.play_audio,
            19: self.record_audio,
            3: self.stop_audio
        }
        self.back_key = {
            '<Control_R>': self.initial
        }

        self.recording = None
        self.is_recording = False
        pygame.mixer.init()
        self.audio_setup_attributes()

    def audio_setup_attributes(self):
        self.audio_viewer = tk.Toplevel(self.parent)
        self.audio_viewer.title("Audio-Files-Viewer")
        self.audio_viewer.attributes("-fullscreen", True)
        self.audio_viewer.focus_force()
        bind_keys(self.key_function_map_audio, self.audio_viewer)

        setBGImage("images/audio.png", self.audio_viewer)
        self.audio_viewer.focus_force()

        self.recording = None

        image_path_stop = "images/stop_record_button.png"
        self.image_stop = Image.open(image_path_stop)
        self.image_stop = self.image_stop.resize((100, 100))  # Resize the image if needed
        self.photo_stop = ImageTk.PhotoImage(self.image_stop)
        self.stop_button = tk.Button(self.audio_viewer, image=self.photo_stop, borderwidth=0)
        print("Kkkk")

    def play_audio(self, channel):
        pygame.mixer.init()

        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play()

        '''def audio_player():
            print('play')
            data, fs = sf.read(self.audio_file)
            sd.play(data, fs)
            sd.wait()

        audio_thread = threading.Thread(target=audio_player)
        audio_thread.start()'''

    def record_audio(self, channel):
        self.stop_button.pack(side=tk.BOTTOM, anchor=tk.CENTER)
        self.stop_button.config(state=tk.NORMAL)
        # self.record = self.key
        print("recording begins")
        self.recording = sd.rec(int(10 * 44100), samplerate=44100, channels=1)
        self.is_recording = True

    def stop_audio(self, channel):
        self.stop_button.forget()
        sd.stop()
        file_path = self.audio_file
        sf.write(file_path, self.recording, 44100)
        self.recording = None
        self.is_recording = False
        self.stop_button.config(state=tk.DISABLED)
        self.stop_button.pack_forget()

    def show_audio_file1(self):
        self.key = 1
        file_path = "images/audio1.png"
        self.audio_file = "audio/file1.wav"
        self.audio_background(file_path)

    def show_audio_file2(self):
        self.key = 2
        file_path = "images/audio2.png"
        self.audio_file = "audio/file1.wav"
        self.audio_background(file_path)

    def show_audio_file3(self):
        self.key = 3
        file_path = "images/audio3.png"
        self.audio_file = "audio/file1.wav"
        self.audio_background(file_path)

    def show_audio_file4(self):
        self.key = 4
        file_path = "images/audio4.png"
        self.audio_file = "audio/file1.wav"
        self.audio_background(file_path)

    def audio_background(self, file_path):
        setBGImage(file_path, self.audio_viewer)
        unbind_keys(self.key_function_map_audio, self.audio_viewer)
        bind_gpio_pins(self.gpio_map_edit)
        bind_keys(self.back_key, self.audio_viewer)

    def initial(self):
        unbind_gpio_pins(self.gpio_map_edit)
        unbind_keys(self.back_key, self.audio_viewer)
        bind_keys(self.key_function_map_audio, self.audio_viewer)
        setBGImage("images/audio.png", self.audio_viewer)

    def go_back(self, event=None):
        print("go back")
        unbind_keys(self.key_function_map_audio, self.audio_viewer)
        unbind_gpio_pins(gpio_map_edit)
        unbind_keys(self.back_key, self.audio_viewer)
        self.audio_viewer.destroy()
        SavedMessagesPage(self.parent)


class TextViewer:

    def __init__(self, parent):
        #super().__init__()
        self.parent = parent
        self.key_function_map_text = {
            '1': self.show_text_file1,
            '2': self.show_text_file2,
            '3': self.show_text_file3,
            '4': self.show_text_file4,
            "<Control_R>": self.go_back
        }
        self.key_function_map_edit = {
            6: self.enable_editing,
            19: self.save_changes,
        }
        self.back_key = {
            "<Control_R>": self.go_back_to_image
        }
        self.text_setup_attributes()

    def text_setup_attributes(self):

        # self.parent = tk.Toplevel(self.parent.sm_window)
        # self.parent.title("Text-Files-Viewer")
        # self.parent.attributes("-fullscreen", True)
        print("text")
        setBGImage("images/text.png", self.parent)
        print("text2")
        bind_keys(self.key_function_map_text, self.parent)
        self.parent.focus_force()
        self.current_file_number = 0
        self.editing_enabled = False
        self.text_widget = None

    def show_text_file1(self):
        self.key = 1
        file_path = "images/text1.png"
        self.text_file = "text/file1.txt"
        self.text_background(file_path)

    def show_text_file2(self):
        self.key = 1
        file_path = "images/text2.png"
        self.text_file = "text/file2.txt"
        self.text_background(file_path)

    def show_text_file3(self):
        self.key = 1
        file_path = "images/text3.png"
        self.text_file = "text/file3.txt"
        self.text_background(file_path)

    def show_text_file4(self):
        self.key = 1
        file_path = "images/text4.png"
        self.text_file = "text/file4.txt"
        self.text_background(file_path)

    def text_background(self, file_path):
        unbind_keys(self.key_function_map_text, self.parent)
        with open(self.text_file, "r") as file:
            content = file.read()

        if self.text_widget:
            self.text_widget.pack_forget()

        self.canvas = setTEXTBG(file_path, self.parent)
        self.text_widget = setTEXT(self.parent)
        self.text_widget.insert(tk.END, content)
        self.current_file_number = self.key
        self.text_widget.config(state=tk.DISABLED)
        bind_gpio_pins(self.key_function_map_edit)
        bind_keys(self.back_key, self.parent)

    def enable_editing(self):
        # Enable text widget editing when shift is pressed
        self.editing_enabled = True
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.configure(insertwidth=1)
        self.text_widget.focus_set()

    def save_changes(self):
        if self.editing_enabled:
            file_path = self.text_file
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.text_widget.config(state=tk.DISABLED)  # Disable text widget editing after saving
            self.editing_enabled = False
            self.parent.config(cursor="")

    def go_back_to_image(self):
        self.text_widget.pack_forget()
        self.canvas.forget()
        setBGImage("images/text.png", self.parent)
        unbind_gpio_pins(self.key_function_map_edit)
        unbind_keys(self.back_key, self.parent)
        bind_keys(self.key_function_map_text, self.parent)

    def go_back(self):
        unbind_keys(self.key_function_map_text, self.parent)
        unbind_gpio_pins(self.key_function_map_edit)
        bind_gpio_pins(self.parent.sm_pin_functions)
        self.parent.destroy()
        SavedMessagesPage(self.parent)
"""
