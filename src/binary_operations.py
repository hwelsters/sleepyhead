import pandas


def is_binary(column: pandas.Series) -> bool:
    '''
    Returns whether `column` contains only 0s or 1s
    '''
    return column.apply(lambda row: 0 if row in [0, 1] else 1).sum() == 0


def negation(column: pandas.Series) -> pandas.Series:
    if not is_binary(column):
        raise ValueError("[column] shoud contain only 0s and 1s")
    return 1 - column


def conjunction(column_1: pandas.Series, column_2: pandas.Series) -> pandas.Series:
    if not is_binary(column_1) or not is_binary(column_2):
        raise ValueError("[column] shoud contain only 0s and 1s")
    return column_1 & column_2


def disjunction(column_1: pandas.Series, column_2: pandas.Series) -> pandas.Series:
    if not is_binary(column_1) or not is_binary(column_2):
        raise ValueError("[column] shoud contain only 0s and 1s")

    return column_1 & column_2


def conditional_probability(event: pandas.Series, condition: pandas.Series) -> float:
    if not is_binary(event) or not is_binary(condition):
        raise ValueError(
            "[event] and [condition] should contain only 0s or 1s")

    if (condition.sum() == 0):
        raise ValueError("[condition] only contains zeros")

    return conjunction(event, condition).sum() / condition.sum()
