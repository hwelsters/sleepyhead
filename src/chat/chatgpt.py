from revChatGPT.V1 import Chatbot
from dotenv import load_dotenv
import os
import pandas
import json

load_dotenv()

data_file_path = "data/original/"
output_file_path = "output/original/"
question_file_path = "draw.json"
question_column = "sQuestion"

if not os.path.exists(output_file_path):
    os.makedirs(output_file_path)

chatbot = Chatbot(config={
    "email": os.environ.get("email"),
    "password": os.environ.get("password"),
})

def ask_chat_gpt(question : str) -> str:
    message = ""
    prev_text = ""
    for data in chatbot.ask(question):
        message += data["message"][len(prev_text) :]
        prev_text = data["message"]
    return message

def append_to_file(output_file_path : str, data):
    with open(output_file_path, 'a') as outfile:
        outfile.write("\n")
        outfile.write(json.dumps(data))
        outfile.close()

def clean_str_for_json(text : str):
    return text.replace("\"", "\'")

def ask_all_questions() -> None:
    questions = pandas.read_json(f"{data_file_path}{question_file_path}")
    output = pandas.read_json(f"{output_file_path}{question_file_path}", lines=True)
    last_index = output.iloc[-1]["question_number"]
    del output
    print(last_index)
    for index, row in questions.iterrows():
        if index <= last_index: continue

        chatgpt_response = ask_chat_gpt(row[question_column])
            
        row_to_append = {
            "question_number": index,
            "response": clean_str_for_json(chatgpt_response)
        }

        append_to_file(f"{output_file_path}{question_file_path}", row_to_append)