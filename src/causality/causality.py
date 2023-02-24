import binary_operations
import pandas

prior_value = -1


def prior(effect: pandas.Series) -> float:
    if not binary_operations.is_binary(effect):
        raise ValueError("[effect] should contain only 0s or 1s")
    if prior_value == -1:
        prior_value = effect.sum() / len(effect)
    return prior_value


def causality_value(effect: pandas.Series, cause: pandas.Series):
    prior()


def is_prima_facie(effect: pandas.Series, cause: pandas.Series) -> bool:
    return binary_operations.conditional_probability(effect, cause) > prior
