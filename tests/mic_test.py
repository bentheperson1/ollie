import vosk
import pyaudio
import json

model_path = "vosk-model-large"

model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)

print("Listening for speech. Say 'Terminate' to stop.")

while True:
    data = stream.read(4096)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        recognized_text = result['text']
        
        print(recognized_text)
        
        if "terminate" in recognized_text.lower():
            print("Termination keyword detected. Stopping...")
            break

stream.stop_stream()
stream.close()

p.terminate()