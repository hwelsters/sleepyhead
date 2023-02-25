import schedule
import chat.chatgpt
import traceback
import logging

def sleepy_ask(config, questions : list, output_file_path : str):
    if not isinstance(questions, list): raise ValueError("[questions] should be a list")
    def func() -> None:
        try: chat.chatgpt.ask_all_questions(config=config, questions=questions, output_file_path=output_file_path)
        except Exception as e: 
            logging.error(traceback.format_exc())
    schedule.every(1).hours.do(func)
    func()
    while True: schedule.run_pending()