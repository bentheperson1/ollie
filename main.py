import argparse
import os
from modules.chat import ChatInterface
from modules.voice import VoiceInterface
from modules.audio import AudioFile
from plugins.plugin_register import load_active_plugins, bot_functions
from dotenv import load_dotenv
from yapper import PiperVoiceUS

def main():
    parser = argparse.ArgumentParser(description="Ollie - Chat and Voice Interface")
    parser.add_argument("--mode", choices=["text", "voice"], default="voice",
                        help="Interaction mode: 'text' or 'voice'")
    parser.add_argument("--trigger", default="curse",
                        help="Keyword trigger for voice mode")
    parser.add_argument("--model", default="llama3.1",
                        help="Model to use for chat")
    parser.add_argument("--voice_config", default="LESSAC",
                        help="Piper voice configuration to use (e.g., LESSAC)")
    args = parser.parse_args()

    load_dotenv()
    os.system('cls' if os.name == 'nt' else 'clear')

    load_active_plugins()

    system_message_file = "config/system_message.txt"
    vosk_model = "vosk-model-large"

    bot = ChatInterface(model=args.model,
                        system_message_file=system_message_file,
                        functions=bot_functions)

    print("Ollie initialized successfully")
    print(f"Interaction Mode: {args.mode}")

    if args.mode == "text":
        AudioFile("audio/startup.wav").play()
        
        while True:
            user_message = input("You: ")
            
            response = bot.chat(user_message)
            
    elif args.mode == "voice":
        voice_config = getattr(PiperVoiceUS, args.voice_config, PiperVoiceUS.HFC_MALE)
        voice = VoiceInterface(vosk_model, voice_config)
        trigger = args.trigger

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

if __name__ == "__main__":
    main()
