import requests

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