#!/usr/bin/env python3
from modules.chat import Chatbot
from modules.voice import VoiceInterface
from modules.audio import AudioFile

import os

def main():
    bot = Chatbot(system_message_file="config/system_message.txt")
    voice = VoiceInterface("vosk-model")
    trigger_keyword = "ali"

    while True:
        detected = voice.listen_for_keyword(keyword=trigger_keyword)

        if detected:
            AudioFile("audio/confirm.wav").play()

            print("Trigger keyword detected. Now listening for your command...")

            command = voice.get_command_after_keyword()
            if command:
                response = bot.chat(command)
                voice.speak_text(response)
            else:
                print("No command detected after keyword.")

if __name__ == "__main__":
    main()
