from modules.chat import Chatbot
from modules.voice import VoiceInterface
from modules.audio import AudioFile
from modules.functions import bot_functions

interact_mode = "text"
bot = Chatbot(system_message_file="config/system_message.txt", functions=bot_functions)

print("Ollie initialized successfully")
print(f"Interaction Mode: {interact_mode}")

match interact_mode:
	case "text":
		AudioFile("audio/startup.wav").play()
		
		while True:
			user_message = input("You: ")

			bot.chat(user_message)
		
	case "voice":
		voice = VoiceInterface("vosk-model-large")
		trigger = "curse"

		AudioFile("audio/startup.wav").play()
		
		while True:
			detected = voice.listen_for_keyword(trigger)

			if detected:
				print("Keyword detected. Now listening for your command...")

				command = voice.get_command_after_keyword()
				if command:
					response = bot.chat(command)
					voice.speak_text(response)
				else:
					print("No command detected after keyword.")
