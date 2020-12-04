from typing import List, Tuple
import pytest


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(
            1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


def test_equal():
    words = ['table', 'apple', 'orange', 'tree']
    answer = [
        ('table', [0, 0, 0, 1]),
        ('apple', [0, 0, 1, 0]),
        ('orange', [0, 1, 0, 0]),
        ('tree', [1, 0, 0, 0])
    ]
    assert fit_transform(words) == answer


def test_equal_with_repeats():
    words = ['table', 'apple', 'orange', 'tree', 'table', 'table']
    answer = [
        ('table', [0, 0, 0, 1]),
        ('apple', [0, 0, 1, 0]),
        ('orange', [0, 1, 0, 0]),
        ('tree', [1, 0, 0, 0]),
        ('table', [0, 0, 0, 1]),
        ('table', [0, 0, 0, 1])
    ]
    assert fit_transform(words) == answer


def test_notin():
    words = ['table', 'apple', 'orange', 'tree']
    assert ('cat', [0, 0, 0, 1]) not in fit_transform(words)


def test_exception():
    with pytest.raises(TypeError):
        fit_transform()
