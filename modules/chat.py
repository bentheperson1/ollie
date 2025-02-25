import ollama

class Chatbot:
    def __init__(self, model="llama3.2", system_message_file="system_message.txt"):
        self.model = model
        try:
            with open(system_message_file, "r") as f:
                self.system_message = f.read().strip()
        except Exception as e:
            print(f"Warning: Could not load system message from file: {e}")
            self.system_message = ""

    def chat(self, prompt):
        messages = []
        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})
        messages.append({"role": "user", "content": prompt})

        try:
            response = ollama.chat(model=self.model, messages=messages, stream=False)
            full_response = response["message"]["content"]

            print("Chatbot:", full_response)
            return full_response
        except Exception as e:
            error_message = f"Error communicating with Ollama: {e}"
            print(error_message)
            return error_message
