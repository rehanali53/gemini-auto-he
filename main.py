import google.generativeai as genai
import os
from datetime import datetime
import re
from utils.data_extract import *
from utils.scarping import *


class ChatHistoryManager:
    def __init__(self, filename="chat_history.txt", max_file_size_mb=5):
        self.history = []
        self.filename = filename
        self.max_file_size_mb = max_file_size_mb

    def add_message(self, role, text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(
            {'role': role, 'text': text, 'timestamp': timestamp})

    def save_to_file(self):
        self._rotate_file_if_needed()
        with open(self.filename, "a", encoding="utf-8") as file:
            for message in self.history:
                file.write(
                    f"{message['timestamp']} {message['role']}: {message['text']}\n")
        self.history.clear()

    def display(self):
        for message in self.history:
            print(
                f"{message['timestamp']} {message['role']}: {message['text']}")

    def _rotate_file_if_needed(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "a", encoding="utf-8") as file:
                pass

        if os.path.getsize(self.filename) > self.max_file_size_mb * 1024 * 1024:
            os.rename(self.filename, self.filename + ".backup")


def main():
    
    os.environ['GOOGLE_API_KEY'] = "Use YOUR GEMINI API KEY"
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
    }

    history_manager = ChatHistoryManager()
    history_manager.add_message("system", "--- New Session ---")

    model = genai.GenerativeModel(
        'gemini-pro', generation_config=generation_config, safety_settings=safety_settings)
    chat = model.start_chat(history=[])

    urls = load_urls_from_json()
    car_data = extract_car_data(urls)
    car_names = extract_car_titles(car_data)
    previous_data=scrp()
    car_prompt = ""

    while True:
        
        user_input = f"conversation with user should be in hebrew, remeber this you are bot which knows only about vehicle so if user ask other things appologise and respond that ask about vehicle and first only greet the user once as -welcome to company name {previous_data} and how can i help you-, the user query is after this sentence."
        user_input += input("User: ").strip()
            
        if not user_input:
            print("Please enter some text.")
            continue

        if user_input.lower() == "history":
            history_manager.display()
            continue


        if user_input.lower() == "restart":
            history_manager.save_to_file()
            os.system('cls' if os.name == 'nt' else 'clear')
            history_manager.add_message("system", "--- New Session ---")
            chat = model.start_chat(history=[])
            continue

        if 'exit' in user_input.lower():
            history_manager.save_to_file()
            break

        try:
            
            for name in car_names:
                if name in user_input:
                    action_url, image_url = search_car_by_name(name, car_data)
                    car_prompt = f"all conversation must be in hebrew language. answer all users questions if you have knowlegde about price tell the user or just give estimate price. if user asking for proposal write an complete proposal. if user asking for load guide him according to your knowledge = {previous_data}. act as you are customer service provider of autobot . this is our website https://autobot.co.il/  mention this website where you need and show the car action_url ={action_url} and also show the car image_url ={image_url}."
                    user_input = car_prompt
                    response = model.generate_content(user_input, stream=True)
                    response_text = ""
                    for chunk in response:
                        if chunk.text.endswith("."):
                            response_text += chunk.text
                    else:
                        response_text += re.sub(r'\s*$', '.', chunk.text)
                    print(chunk.text)

                    history_manager.add_message("user", user_input)
                    history_manager.add_message("gemini", response_text)
                
            
            if user_input == car_prompt:
                continue

            elif 'buy' in user_input or 'car' in user_input or 'cars' in user_input:
                user_input = f"all conversation must be in hebrew language. show catalogue of car from carnames = {car_names}."
                print(user_input)
                response = model.generate_content(user_input, stream=True)
                response_text = ""
                for chunk in response:
                    if chunk.text.endswith("."):
                        response_text += chunk.text
                    else:
                        response_text += re.sub(r'\s*$', '.', chunk.text)
                    print(chunk.text)

                    history_manager.add_message("user", user_input)
                    history_manager.add_message("gemini", response_text)

            else:
                response = chat.send_message(user_input, stream=True)
                response_text = ""
                for chunk in response:
                    if chunk.text.endswith("."):
                        response_text += chunk.text
                    else:
                        response_text += re.sub(r'\s*$', '.', chunk.text)
                    print(chunk.text)

                    history_manager.add_message("user", user_input)
                    history_manager.add_message("gemini", response_text)
                    
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()