#!/usr/bin/env python3
import requests
import json
import pyaudio
import pyttsx3
import time
from vosk import Model, KaldiRecognizer

class Chatbot:
    def __init__(self, model="gemma2:2b", api_url="http://localhost:11434", system_message_file="system_message.txt"):
        self.model = model
        self.api_url = api_url

        try:
            with open(system_message_file, "r") as f:
                self.system_message = f.read().strip()
        except Exception as e:
            print(f"Warning: Could not load system message from file: {e}")
            self.system_message = ""

    def chat(self, prompt):
        endpoint = f"{self.api_url}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        messages = []
        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            full_response = data["choices"][0]["message"]["content"]
            print("Chatbot:", full_response)
            return full_response

        except Exception as e:
            error_message = f"Error communicating with Ollama: {e}"
            print(error_message)
            return error_message

class VoiceInterface:
    def __init__(self, vosk_model_path="/home/tinybit/ollie/vosk-model"):
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

    def listen_for_keyword(self, keyword="assistant"):
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

def main():
    bot = Chatbot()
    voice = VoiceInterface()
    trigger_keyword = "ali"

    print("System is continuously processing audio and waiting for the keyword...")
    while True:
        detected = voice.listen_for_keyword(keyword=trigger_keyword)

        if detected:
            print("Trigger keyword detected. Now listening for your command...")

            command = voice.get_command_after_keyword()
            if command:
                response = bot.chat(command)
                voice.speak_text(response)
            else:
                print("No command detected after keyword.")

if __name__ == "__main__":
    main()
