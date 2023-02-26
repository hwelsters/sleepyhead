import pandas
import re
import os
from typing import List
from sympy.parsing.sympy_parser import parse_expr
from sympy import Eq, simplify, exp, cos
from sympy.solvers import solve
import collections
import numpy

pandas.options.mode.chained_assignment = None  # default='warn'

input_file_path = "data/original/"
template_file_path = "data/template/"
output_file_path = "data/variations/"
filter_file_path = "data/filter/"
data_file_path = "draw.json"

QUESTION_COLUMN = "sQuestion"
EQUATIONS_COLUMN = "lEquations"
TEMPLATE_COLUMN = "Template"
SOLUTIONS_COLUMN = "lSolutions"

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


def is_integer(solution: float):
    return solution % 1 == 0


def is_positive(solution: float):
    return solution > 0


def get_constraints(solution: float):
    return {
        "integer": is_integer(solution),
        "positive": is_positive(solution)
    }


def get_numbers(text: str):
    text = text.replace(",", "")
    decimals = re.findall("[0-9]+\.?[0-9]*", text)

    for i in range(decimals.count("0.01")):
        decimals.remove("0.01")

    return decimals


def get_template_text(text: str, number_map: dict):
    numbers = get_numbers(text)

    for number in numbers:
        if not float(number) in number_map:
            continue
        text = text.replace(number, number_map[float(number)], 1)
    return text


def get_template_equations(equations: pandas.DataFrame, number_map):
    template_equation = []
    for equation in equations:
        template_equation += [get_template_text(equation, number_map)]
    return str(template_equation)


def generate_template_file():
    input_data = pandas.read_json(f"{input_file_path}{data_file_path}")

    question_numbers = input_data.apply(
        lambda row: get_numbers(row[QUESTION_COLUMN]), axis=1)
    equation_numbers = input_data.apply(
        lambda row: get_numbers(str(row[EQUATIONS_COLUMN])), axis=1)

    float_question_numbers = question_numbers.apply(
        lambda row: set([float(x) for x in row]))
    float_equation_numbers = equation_numbers.apply(
        lambda row: set([float(x) for x in row]))

    valid = {
        "question": float_question_numbers,
        "equation": float_equation_numbers
    }
    valid = pandas.concat(valid, axis=1)
    valid = valid.apply(
        lambda row: row["question"].issubset(row["equation"]), axis=1)

    # FILTER OUT FAILED QUESTIONS FOR FURTHER ANALYSIS
    input_data[valid == False].to_json(
        f"{filter_file_path}{data_file_path}", orient="records")

    valid_data = input_data[valid == True]

    for index, row in valid_data.iterrows():
        numbers = get_numbers(valid_data.loc[index, QUESTION_COLUMN])
        number_map = {}

        for i, number in enumerate(numbers):
            number_map[float(number)] = f"[{chr(i + ord('a'))}]"

        valid_data.loc[index, "numbers"] = str(numbers)
        valid_data.loc[index, "ConstantsConstraints"] = str(
            [{**get_constraints(float(number)), "key": number_map[float(number)]} for number in list(number_map.keys())])
        valid_data.loc[index, QUESTION_COLUMN] = get_template_text(
            valid_data.loc[index, QUESTION_COLUMN], number_map)
        valid_data.loc[index, EQUATIONS_COLUMN] = get_template_equations(
            valid_data.loc[index, EQUATIONS_COLUMN], number_map)

    valid_data[EQUATIONS_COLUMN] = valid_data.apply(
        lambda row: eval(row[EQUATIONS_COLUMN]), axis=1)
    valid_data["numbers_len"] = valid_data.apply(
        lambda row: len(eval(row["numbers"])), axis=1)
    valid_data.to_json(
        f"{template_file_path}{data_file_path}", orient="records")


def generate_Eq(equation: str):
    equation = equation.split("=")
    eqs = Eq(parse_expr(equation[0], evaluate=False), 
             parse_expr(equation[1], evaluate=False))
    return eqs


def fulfills_constraints(num: float, constraints):
    if constraints["positive"] and num <= 0:
        return False
    if constraints["integer"] and not is_integer(num):
        return False
    return True


def generate_variation(question: str, equations: List[str], solutions: List[float], constant_constraints, numbers_len):
    RANGE_SIZE = 100
    FLOAT_STEP_SIZE = 1

    constant_constraints_map : dict= {}
    for constraint in constant_constraints:
        constant_constraints_map[constraint["key"]] = {'integer': constraint['integer'], 
                                                       'positive': constraint['positive']}
    print(constant_constraints_map)
    
    def recurse(index: int, max_index: int, current_question: str, current_equations: List[str]):
        var_char = f"[{chr(index + ord('a'))}]"
        if index == max_index:
            eq_to_solve = [generate_Eq(equation) for equation in current_equations]
            solved = solve(eq_to_solve)
            solved = solved

            solved_constraints = [get_constraints(num) for num in solved]
            solution_constraints = [get_constraints(num) for num in solutions]
            
            if (solved_constraints == solution_constraints):
                data = pandas.DataFrame({"question" : current_question, "equations" : current_equations, "solutions": str(solved)})
                print(data)
            
            return
        
        for i in range(-RANGE_SIZE * 10, RANGE_SIZE*10):
            num = FLOAT_STEP_SIZE * i
            if var_char in (constant_constraints_map.keys()) and fulfills_constraints(num,constant_constraints_map[var_char]): continue
            new_question = current_question.replace(var_char, str(num))
            new_equations = [current_equation.replace(var_char, str(num)) for current_equation in current_equations]
            recurse(index + 1, max_index, new_question, new_equations)

    recurse(0, numbers_len, question, equations)

def generate_variation_file():
    print("BONK")


generate_variation("The ratio of girls to boys of a dance group is [a] to [d] . There would had been equal number of boys and girls if there had been [d] more boys and [d] fewer girls . How many girls and boys are in a dance group ?", 
                   ["x-[d]=y+[d]", "[d]*x = [a]*y"], [15.0, 9.0], [{'integer': True, 'positive': True, 'key': '[a]'}, {'integer': True, 'positive': True, 'key': '[d]'}], 4)
# generate_template_file()
# generate_variations()
