#!/usr/bin/env python3
from modules.chat import Chatbot
from modules.voice import VoiceInterface
from modules.audio import AudioFile
from dotenv import load_dotenv

import os

load_dotenv()

interact_mode = "voice"

def main():
	bot = Chatbot(system_message_file="config/system_message.txt")

	print(f"Interaction Mode: {interact_mode}")
	
	match interact_mode:
		case "text":
			while True:
				user_message = input("You: ")

				bot.chat(user_message)
			
		case "voice":
			voice = VoiceInterface("vosk-model")
			trigger_keyword = "ali" # vosk hears 'ollie' as 'ali'
			
			while True:
				detected = voice.listen_for_keyword(keyword=trigger_keyword)
				print(detected)
				if detected:
					AudioFile("audio/confirm.wav").play()

					print("Keyword detected. Now listening for your command...")

					command = voice.get_command_after_keyword()
					if command:
						response = bot.chat(command)
						voice.speak_text(response)
					else:
						print("No command detected after keyword.")

if __name__ == "__main__":
	main()
