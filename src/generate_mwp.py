import sympy
import pandas
import re
import os

pandas.options.mode.chained_assignment = None  # default='warn'

input_file_path = "data/original/"
template_file_path = "data/template/"
output_file_path = "data/variations/"
filter_file_path = "data/filter/"
data_file_path = "alg514.json"

QUESTION_COLUMN = "sQuestion"
EQUATIONS_COLUMN = "lEquations"
TEMPLATE_COLUMN = "Template"

# This code attemps to generate tem of math word problem solving datasets with different solutions

# This code makes a few critical assumptions:
# 1) The numbers in question will appear exactly the same as it does in the intermediary equations. (This one is ok since the questions are filtered out)
# 2) Furthermore, much of the design decisions are based on the DRAW-1K MWP dataset
# 3) 0.01 is ONLY used for questions involving percentages

# There are a few things that we do to reduce possibility of error
# 1) First things first, we filter out questions where the constants in the equations are not equal to the constants in the intermediary equations. These are placed in a separate file

# The code does the following:
# Extablish constraints on the data in the project

if not os.path.exists(template_file_path):
    os.makedirs(template_file_path)
if not os.path.exists(output_file_path):
    os.makedirs(output_file_path)
if not os.path.exists(filter_file_path):
    os.makedirs(filter_file_path)

def is_integer(solution : float):
    return solution.is_integer()

def is_positive(solution : float):
    return solution > 0

def get_constraints(solution : float):
    return {
        "integer": is_integer(float),
        "positive": is_positive
    }

def get_numbers(text: str):
    text = text.replace(",", "")
    decimals = re.findall("[0-9]+\.?[0-9]*", text)
    for i in range(decimals.count("0.01")): decimals.remove("0.01")
    return list(set(decimals))

def get_template_text(text : str, numbers):
    numbers.sort()
    numbers.sort(key = len)
    numbers.reverse()

    for index, number in enumerate(numbers):
        template = f"[{chr(index + ord('a'))}]"
        text = text.replace(str(number), template)
    return text

def get_template_equations(equations : pandas.DataFrame, numbers):
    template_equation = []
    for equation in equations:
        template_equation += [get_template_text(equation, numbers)]
    return str(template_equation)

def generate_template_file():
    input_data = pandas.read_json(f"{input_file_path}{data_file_path}")
    
    question_numbers = input_data.apply(lambda row : get_numbers(row[QUESTION_COLUMN]), axis = 1)
    equation_numbers = input_data.apply(lambda row : get_numbers(str(row[EQUATIONS_COLUMN])), axis = 1)
    
    float_question_numbers = question_numbers.apply(lambda row : set([float(x) for x in row]))
    float_equation_numbers = equation_numbers.apply(lambda row : set([float(x) for x in row]))
    valid = float_equation_numbers == float_question_numbers

    # FILTER OUT FAILED QUESTIONS FOR FURTHER ANALYSIS
    input_data[valid == False].to_json(f"{filter_file_path}{data_file_path}", orient="records")

    valid_data = input_data[valid == True]

    for index, row in valid_data.iterrows():
        numbers = get_numbers(valid_data.loc[index, QUESTION_COLUMN])
        valid_data.loc[index, "numbers"] = str(numbers)
        valid_data.loc[index, QUESTION_COLUMN] = get_template_text(valid_data.loc[index, QUESTION_COLUMN], numbers)
        valid_data.loc[index, EQUATIONS_COLUMN] = get_template_equations(valid_data.loc[index, EQUATIONS_COLUMN], numbers)
        
    valid_data[EQUATIONS_COLUMN] = valid_data.apply(lambda row : eval(row[EQUATIONS_COLUMN]), axis=1)
    valid_data["numbers_len"] = valid_data.apply(lambda row : len(eval(row["numbers"])), axis=1)

    valid_data.to_json(f"{template_file_path}{data_file_path}", orient="records")

generate_template_file()