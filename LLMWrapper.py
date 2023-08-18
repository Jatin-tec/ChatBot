import time
import requests
import openai
import dotenv
import os


dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMWrapper:
    """Wrapper class for the LLM API."""
    def __init__(self, max_tokens=1000, model="gpt-3.5-turbo", max_try=2):
        self.max_tokens = max_tokens
        self.model = model
        self.max_try = max_try
        self.history = []

    def _send_request(self, prompt):
        for _ in range(self.max_try):
            try:
                if self.history:
                    for elm in self.history[-2:]:
                        if elm['role'] == 'user':
                            messages = [{"role": "user", "content": elm['content']}]
                        else:
                            messages = [{"role": "assistant", "content": elm['content']}]
                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=messages,
                        temperature=0.8,
                    )
                    return response.choices[0].message["content"]
                else:
                    messages = [{"role": "user", "content": prompt}]
                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=messages,
                        temperature=0.8,
                    )
                    return response.choices[0].message["content"]

            except openai.error.RateLimitError as e:
                print("Rate limit exceeded. Waiting before retrying...")
                time.sleep(60)
                return self._send_request(messages)
            
            except openai.error.InvalidRequestError as e:
                if len(prompt) > self.max_tokens:
                    print("Prompt too long. Truncating...")
                    prompt = prompt[:self.max_tokens]
                    return self._send_request(prompt)
                print("Invalid request:", e)
                return {'error': 'invalid_request'}
            
            except Exception as e:
                print("Unhandled exception:", e)
                return {'error': 'unknown'}

    def _handle_rate_limit(self):
        print("Rate limit exceeded. Waiting before retrying...")
        time.sleep(60) 

    def generate_response(self, user_input):
        if len(self.history) > 0:
            conversation = "\n".join(self.history + [user_input])
        else:
            conversation = user_input
        
        response = self._send_request(conversation)

        generated_text = response
        self.history.append(generated_text)
        return generated_text

    def reset_history(self):
        self.history = []

# wrapper = LLMWrapper()
# response = wrapper.generate_response("""""")
# print(response)