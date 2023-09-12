import tkinter as tk
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import soundfile as sf
import sounddevice as sd


def bind_gpio_pins(pins_functions):
    GPIO.setmode(GPIO.BCM)
    for pin, function in pins_functions.items():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=function, bouncetime=2000)


def unbind_gpio_pins(pins_functions):
    for pin, function in pins_functions.items():
        GPIO.remove_event_detect(pin)


def bind_keys(key_function_map, parent_window):
    for key, callback in key_function_map.items():
        parent_window.bind(key, lambda event, cb=callback: cb())


def unbind_keys(key_function_map, parent_window):
    for key, callback in key_function_map.items():
        parent_window.unbind(key)


def setBGImage(file_source, parent_window):
    bg_image_path = file_source
    bg_image = Image.open(bg_image_path)
    new_size = (1350, 720)
    bg_image = bg_image.resize(new_size, Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(bg_image)
    label_bg = tk.Label(parent_window, image=bg_image)
    label_bg.image = bg_image
    label_bg.place(x=0, y=0, relwidth=1, relheight=1)


def setTEXTBG(file_source, parent_window):
    original_image = Image.open(file_source)
    canvas_width = parent_window.winfo_screenwidth()
    canvas_height = parent_window.winfo_screenheight()
    resized_image = original_image.resize((canvas_width, canvas_height), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resized_image)
    canvas = tk.Canvas(parent_window, width=canvas_width, height=canvas_height)
    canvas.pack()
    canvas.background = background_image
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
    return canvas


def setTEXT(parent_window):
    input_text = tk.Text(parent_window, wrap=tk.WORD, font=("Helvetica", 40), width=33, height=12)
    input_text.pack(expand=True)
    input_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    return input_text


def panic_audio():
    print("called")
    audio_file = "panic.wav"

    def play_audio():
        data, samplerate = sf.read(audio_file)
        sd.play(data, samplerate)
        sd.wait()

    play_audio()

