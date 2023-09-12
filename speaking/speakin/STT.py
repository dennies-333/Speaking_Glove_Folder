import tkinter as tk
import speech_recognition as sr
from utility import bind_keys, setTEXTBG, setTEXT, setBGImage
from utility import unbind_keys, bind_gpio_pins, unbind_gpio_pins
import pyaudio


class STTPage:
    def __init__(self, parent):

        self.parent = parent
        self.key_function_map_stt = {
            "<Control_R>": self.go_back
        }

        self.stt_pin_function = {
            3: self.toggle_recording
        }
        self.recognizer = sr.Recognizer()
        self.audio = pyaudio.PyAudio()
        self.stt_setup_attributes()

    def stt_setup_attributes(self):

        self.stt_window = tk.Toplevel(self.parent.root)
        self.stt_window.title("Speech-To-Text")
        self.stt_window.attributes("-fullscreen", True)
        unbind_gpio_pins(self.parent.pin_functions)
        bind_gpio_pins(self.stt_pin_function)
        bind_keys(self.key_function_map_stt, self.stt_window)
        setTEXTBG(
            "images/background2.png",
            self.stt_window
        )
        self.text_widget = setTEXT(self.stt_window)
        self.stt_window.focus_force()
        self.recognizing_text = "Recognizing..."
        self.recognizing_fail = "Speech Transcription Failed !\nTry Again..."
        self.is_recording = False
        self.audio_stream = None
        self.audio_segments = []
        print("la")

    def update_text_widget(self, text):
        print("update")
        self.text_widget.delete(1.0, tk.END)  # Clear existing text
        self.text_widget.insert(tk.END, text)  # Insert new text

    def toggle_recording(self, event=None):
        print("cap")
        if not self.is_recording:
            # Start recording
            self.is_recording = True
            self.audio_segments = []
            self.audio_stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                                                frames_per_buffer=1024, stream_callback=self.capture_audio)
            self.audio_stream.start_stream()
            self.update_text_widget(self.recognizing_text)
            print("Recording...")
        else:
            # Stop recording and transcribe audio
            self.is_recording = False
            print("Stopped recording.")
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            try:
                combined_audio_data = b''.join(self.audio_segments)
                audio_data = sr.AudioData(combined_audio_data, 16000, 2)  # 2 represents sample width in bytes
                recognized_text = self.recognizer.recognize_google(audio_data)
                self.update_text_widget(recognized_text)
            except sr.UnknownValueError:
                self.update_text_widget(self.recognizing_fail)
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def capture_audio(self, in_data, frame_count, time_info, status):
        print("capture")
        if self.is_recording:
            self.audio_segments.append(in_data)
        return in_data, pyaudio.paContinue

    def go_back(self):

        unbind_gpio_pins(self.stt_pin_function)
        bind_gpio_pins(self.parent.pin_functions)
        self.stt_window.destroy()
