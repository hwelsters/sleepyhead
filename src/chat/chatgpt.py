from revChatGPT.V1 import Chatbot
from dotenv import load_dotenv
import os
import pandas
import json
from pathlib import Path

load_dotenv()

def append_to_file(output_file_path: str, data):
    with open(output_file_path, 'a') as outfile:
        outfile.write(json.dumps(data))
        outfile.write("\n")
        outfile.close()


def clean_str_for_json(text: str):
    return text.replace("\"", "\'")


def ask_all_questions(config, questions : list, output_file_path : str) -> None:
    chatbot = Chatbot(config=config)

    def ask_chat_gpt(question: str) -> str:
        question = str(question)
        message = ""
        prev_text = ""
        for data in chatbot.ask(question):
            message += data["message"][len(prev_text):]
            prev_text = data["message"]
        return message
    
    last_index = 0
    if Path(output_file_path).is_file():
        output = pandas.read_json(output_file_path, lines=True)
        if len(output) > 0: last_index = output.iloc[-1]["question_number"]
        del output

    for index, question in enumerate(questions):
        if index <= last_index: continue

        chatgpt_response = ask_chat_gpt(question)
        row_to_append = {"question_number": index, "question": question,"response": clean_str_for_json(chatgpt_response)}
        append_to_file(output_file_path, row_to_append)
