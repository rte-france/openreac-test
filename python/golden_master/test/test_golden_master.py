# imports
import pytest
import os
from utils import *

TESTS = [test for test in os.listdir(GOLDEN_MASTER_PATH)]

@pytest.mark.parametrize("test", TESTS)
def test_output_comparison(test):
    """
    Test if there are differences in output between execution of original ampl code and divided one,
    for all the tests in the GOLDEN MASTER. 
    """
    # True to print the differences if any
    assert open_reac_output_comparison(test, True)