import pytest
import midpoint
import numpy as np


testdata = [
    [[(0, 1), (5, 1), (4, 1)], True],
    [[(0, 1), (4, 1), (5, 1)], False],
    [[(0, 1), (5, 10), (4, 1)], False],
]


@pytest.mark.parametrize("pts,expected", testdata)
def test_flat(pts, expected):
    assert midpoint.is_flat(*map(np.array, pts)) == expected
