import json
import requests
from config import *


class Chatbot:
    def __init__(self) -> None:
        self.model = CHAT_MODEL
        self.system_prompt = {"role": "system", "content": "You are a personal assistant of student. You must say content only related to science and technology and education. You mustn't say too long. Say in short. At most 2 sentences."}
        self.history = []
        self.messages = []

    def get_response(self):
        response = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": self.model, "messages": self.messages, "stream": True}
        )
        response.raise_for_status()
        output = ""

        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done") is False:
                message = body.get("message", "")
                content = message.get("content", "")
                output += content
                print(content, end="", flush=True)

            if body.get("done", False):
                message["content"] = output
                return message


    def chat(self, user_input):
        self.history.append({'role': 'user', 'content': user_input})
        if len(self.history) > 5:
            self.messages = [self.system_prompt] + self.history[-5:]
        else:
            self.messages = [self.system_prompt] + self.history
        
        bot_response = self.get_response()
        self.history.append(bot_response)
        return bot_response['content']


bot = Chatbot()
while True:
    user_input = input('User: ')
    bot_output = bot.chat(user_input)
    print()