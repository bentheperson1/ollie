import ollama

class ChatInterface:
    def __init__(self, model="llama3.1", functions = {}, system_message_file="system_message.txt"):
        self.model: str = model
        self.available_functions: dict = functions
        self.model_options = {
            "temperature": 0
        }

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
            response: ollama.ChatResponse = ollama.chat(
                model=self.model, 
                messages=messages,
                tools=self.available_functions.values(),
                options=self.model_options
            )
            
            full_response = response.message.content

            if response.message.tool_calls:
                for tool in response.message.tool_calls:
                    if function_to_call := self.available_functions.get(tool.function.name):
                        output = function_to_call(**tool.function.arguments)

                #messages.append(response.message)
                messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

                final_response = ollama.chat(self.model, messages=messages, options=self.model_options)
                full_response = final_response.message.content

            print("Ollie:", full_response)
            return full_response
        except Exception as e:
            error_message = f"Error communicating with Ollama: {e}"
            print(error_message)
            return error_message
