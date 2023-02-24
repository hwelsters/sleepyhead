import binary_operations
import pandas
import pandas.testing as testing


def is_binary():
    test_1 = pandas.Series([], dtype=float)
    test_2 = pandas.Series([0, 1, 0, 1, 1, 1, 0])
    test_3 = pandas.Series([10, 1, 0, 2, 1, 1, 0])
    test_4 = pandas.Series([0, 1, 0, 0, "string", 1, 0])

    assert binary_operations.is_binary(test_1) == True
    assert binary_operations.is_binary(test_2) == True
    assert binary_operations.is_binary(test_3) == False
    assert binary_operations.is_binary(test_4) == False

    """"""


def negation():
    test_1 = pandas.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    test_2 = pandas.Series([], dtype=float)
    test_3 = pandas.Series([1, 0, 0, 0, 1, 1, 1])

    solution_1 = pandas.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    solution_2 = pandas.Series([], dtype=float)
    solution_3 = pandas.Series([0, 1, 1, 1, 0, 0, 0])

    output_1 = binary_operations.negation(test_1)
    output_2 = binary_operations.negation(test_2)
    output_3 = binary_operations.negation(test_3)

    testing.assert_series_equal(output_1, solution_1)
    testing.assert_series_equal(output_2, solution_2)
    testing.assert_series_equal(output_3, solution_3)

    """"""


def conjunction():
    test_11, test_12 = pandas.Series([0, 0, 0, 0]), pandas.Series([1, 1, 1, 1])
    test_21, test_22 = pandas.Series([0, 1, 0, 1]), pandas.Series([0, 1, 1, 1])
    test_31, test_32 = pandas.Series(
        [], dtype=int), pandas.Series([], dtype=int)

    output_1 = binary_operations.conjunction(test_11, test_12)
    output_2 = binary_operations.conjunction(test_21, test_22)
    output_3 = binary_operations.conjunction(test_31, test_32)

    solution_1 = pandas.Series([0, 0, 0, 0])
    solution_2 = pandas.Series([0, 1, 0, 1])
    solution_3 = pandas.Series([], dtype=int)

    testing.assert_series_equal(output_1, solution_1)
    testing.assert_series_equal(output_2, solution_2)
    testing.assert_series_equal(output_3, solution_3)

    """"""


def disjunction():
    test_11, test_12 = pandas.Series([0, 0, 0, 0]), pandas.Series([1, 1, 1, 1])
    test_21, test_22 = pandas.Series([0, 1, 0, 1]), pandas.Series([0, 1, 1, 1])
    test_31, test_32 = pandas.Series(
        [], dtype=int), pandas.Series([], dtype=int)
    test_41, test_42 = pandas.Series([0, 1, 0, 1]), pandas.Series([1, 0, 0, 0])

    output_1 = binary_operations.disjunction(test_11, test_12)
    output_2 = binary_operations.disjunction(test_21, test_22)
    output_3 = binary_operations.disjunction(test_31, test_32)
    output_4 = binary_operations.disjunction(test_41, test_42)

    solution_1 = pandas.Series([1, 1, 1, 1])
    solution_2 = pandas.Series([0, 1, 1, 1])
    solution_3 = pandas.Series([], dtype=int)
    solution_4 = pandas.Series([1, 1, 0, 1])

    testing.assert_series_equal(output_1, solution_1)
    testing.assert_series_equal(output_2, solution_2)
    testing.assert_series_equal(output_3, solution_3)
    testing.assert_series_equal(output_4, solution_4)

    """"""


def conditional_probability():
    test_11, test_12 = pandas.Series(
        [0, 0, 0, 1, 0]), pandas.Series([0, 1, 1, 1, 1])
    test_21, test_22 = pandas.Series(
        [0, 0, 1, 1, 0]), pandas.Series([1, 1, 0, 0, 0])
    test_31, test_32 = pandas.Series(
        [0, 0, 1, 1, 0]), pandas.Series([0, 0, 1, 1, 0])
    test_41, test_42 = pandas.Series(
        [1, 1, 1, 1, 0]), pandas.Series([1, 1, 1, 1, 0])

    output_1 = binary_operations.conditional_probability(test_11, test_12)
    output_2 = binary_operations.conditional_probability(test_21, test_22)
    output_3 = binary_operations.conditional_probability(test_31, test_32)
    output_4 = binary_operations.conditional_probability(test_41, test_42)

    assert output_1 == 0.25
    assert output_2 == 0
    assert output_3 == 1
    assert output_4 == 1

    """"""


negation()
is_binary()
conjunction()
conditional_probability()
