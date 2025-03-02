import json
import pyaudio
import time
import os
import requests
import zipfile

from vosk import Model, KaldiRecognizer, SetLogLevel
from modules.audio import AudioFile
from yapper import PiperSpeaker
from tqdm import tqdm

class VoiceInterface:
    def __init__(self, vosk_model_path, piper_voice):
        SetLogLevel(-1)
        
        print("Starting voice module...")

        self.pull_vosk_model(vosk_model_path)

        self.model = Model(vosk_model_path)
        
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=4000)
        self.stream.start_stream()
        self.tts_engine = PiperSpeaker(voice=piper_voice)

    def pull_vosk_model(self, model_dir):
        if not os.path.isdir(model_dir):
            print(f"Model directory '{model_dir}' not found. Downloading the model...")

            url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
            zip_filename = "vosk-model.zip"

            try:
                with requests.get(url, stream=True) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))
                    block_size = 8192

                    with open(zip_filename, 'wb') as file, tqdm(total=total_size, unit='iB', unit_scale=True, desc=zip_filename) as bar:
                        for chunk in response.iter_content(chunk_size=block_size):
                            if chunk:
                                file.write(chunk)
                                bar.update(len(chunk))

                print("\nDownload complete. Extracting the model...")

                extracted_folder = None
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    members = zip_ref.namelist()
                    if members:
                        extracted_folder = members[0].split('/')[0]
                    zip_ref.extractall(".")

                print("Extraction complete.")

                if extracted_folder and extracted_folder != model_dir:
                    if os.path.isdir(extracted_folder):
                        os.rename(extracted_folder, model_dir)
                        print(f"Renamed extracted folder '{extracted_folder}' to '{model_dir}'.")
                    else:
                        print(f"Expected extracted folder '{extracted_folder}' not found.")
                
                os.remove(zip_filename)
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Large English Vosk model already present.")

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
    