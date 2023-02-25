![image](../../images/sleepyhead_logo.png)
![image](../../images/chat.png)

<p align="center">
  Talking to ChatGPT in your sleep.
</p>

Example using pandas:
```python
import pandas
from chat.scheduler import sleepy_ask
import os

input_file_path = 'data/original/draw.json'
output_file_path = 'output/original/draw.json'
questions = pandas.read_json(input_file_path)

config = {
    "email": "email@email.email",
    "password": "password"
}
sleepy_ask(config, questions["sQuestion"].to_list(), output_file_path)
```
