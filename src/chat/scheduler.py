import schedule
from revChatGPT.V1 import Chatbot
from dotenv import load_dotenv
import chatgpt


def func():
    try:
        chatgpt.ask_all_questions()
    except:
        print("oof")


schedule.every(1).hours.do(func)
func()

while True:
    schedule.run_pending()
