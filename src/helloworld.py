import pandas
from chat.scheduler import sleepy_ask
import os

input_file_path = 'data/original/draw.json'
output_file_path = 'output/original/draw.json'
questions = pandas.read_json(input_file_path)

config = {
    "email": os.environ.get("email"),
    "password": os.environ.get("password")}
sleepy_ask(config=config,
           questions=questions["sQuestion"].to_list(),
           output_file_path=output_file_path)
