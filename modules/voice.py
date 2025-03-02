import json
import pyaudio
import pyttsx3
import time
from vosk import Model, KaldiRecognizer, SetLogLevel
from modules.audio import AudioFile

class VoiceInterface:
    def __init__(self, vosk_model_path):
        SetLogLevel(-1)
        
        print("Starting voice module...")

        self.model = Model(vosk_model_path)
        
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=4000)
        self.stream.start_stream()
        self.tts_engine = pyttsx3.init()

    def listen_for_keyword(self, keyword):
        print("Listening for keyword...")

        while True:
            data = self.stream.read(4000, exception_on_overflow=False)

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").lower()

                if keyword.lower() in text:
                    print(f"Keyword '{keyword}' detected in final result: {text}")
                    self.recognizer.Reset()
                    return text
            else:
                partial_result = json.loads(self.recognizer.PartialResult())
                partial_text = partial_result.get("partial", "").lower()

                if keyword.lower() in partial_text:
                    print(f"Keyword '{keyword}' detected in partial result: {partial_text}")
                    self.recognizer.Reset()
                    return partial_text

            time.sleep(0.01)

    def get_command_after_keyword(self, timeout=5):
        print("Listening for command after keyword...")
        AudioFile("audio/listening.wav").play()

        result_text = ""
        start_time = time.time()

        while True:
            if time.time() - start_time > timeout:
                print("Command listening timeout reached.")
                break

            data = self.stream.read(4000, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                result_text = result.get("text", "")
                break
            time.sleep(0.01)
        
        self.recognizer.Reset()
        print("Command captured:", result_text)
        return result_text

    def speak_text(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()