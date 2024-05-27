import filecmp
from collections import Counter
from .openreac_output_loader import *
from .config import *

def comparison_open_reac_printings(expected_printings_path, printings):
    """
    Compare the expected printings of OpenReac, situated in given path,
    with printings given as argument. 
    
    Args:
        expected_printing_path: A path towards the expected printings of OpenReac.
        printings: The printings of OpenReac in a list.

    Return: 
        The list of differences between the expected/actual printings.
    """
    expected_printings_file = open(expected_printings_path, 'r', encoding='utf-8')
    expected_printings = expected_printings_file.readlines()

    # list of printings that must not be compared, due to dependance on the time/machine of execution
    to_ignore = ["Start of file", "End of file", "Elapsed time since start", 
                 "solve: start", "solve: end", "Total program time", "Time spent in evaluations", 
                 "é", "Ã©", "Commercial", "Trial", "COMMERCIAL USE"]
    
    # lists of printings, without ignored ones
    filtered_expected_printings = [line for line in expected_printings if all(substring not in line for substring in to_ignore)]
    filtered_actual_printings = [line for line in printings if all(substring not in line for substring in to_ignore)]
    
    # count the number of different printings
    counter_expected = Counter(filtered_expected_printings)
    counter_expected.pop("\n") # remove the lines with only "\n" character
    counter_actual = Counter(filtered_actual_printings)
    counter_actual.pop("\n") # remove the lines with only "\n" character
    
    difference_expected_actual = counter_expected - counter_actual # printings in expected but not in actual (with occurrences)
    difference_actual_expected = counter_actual - counter_expected # printings in actual but not in expected
    return difference_expected_actual + difference_actual_expected

def comparison_open_reac_indicators(indicators_path_1, indicators_path_2):
    """
    Compare the OpenReac indicators files given as argument.

    Args:
        indicators_path_1, indicators_path_2: Paths towards OpenReac indicators.

    Return: 
        A set containing the keys/values different between compared files.
    """
    # indicators that must not be compared, due to dependance on the time/machine of execution
    to_ignore = [2,3] + [i for i in range(6,13)]
    
    # load indicators, except ignored ones, as dictionnaries
    indicators_1 = load_open_reac_indicators(indicators_path_1, to_ignore=to_ignore)
    indicators_2 = load_open_reac_indicators(indicators_path_2, to_ignore=to_ignore)
    
    # comparison of the keys
    keys_diff = set(indicators_1.keys()) ^ set(indicators_2.keys())
    # comparison of the values
    values_diff = {key: (indicators_1[key], indicators_2[key])      
                   for key in set(indicators_1.keys()) & set(indicators_2.keys()) 
                   if indicators_1[key] != indicators_2[key]}

    return keys_diff.union(values_diff.items())

def compare_open_reac_csv_results(directory_path_1, directory_path_2, files_to_compare):
    """
    Compare the files given as argument in the two given directories.

    Args:
        directory_path_1: The first directory.
        directory_path_2: The second directory.
        files_to_compare: The list of files to be compared.

    Return: 
        True if no difference. False otherwise.
    """
    _, mismatchs, errors = filecmp.cmpfiles(directory_path_1, directory_path_2, files_to_compare)
    return len(errors) == 0 and len(mismatchs) == 0

def compare_v(v1, v2, threshold=DELTA_V):
    return abs(v1 - v2) < threshold

def compare_phi(phi1, phi2, threshold=DELTA_PHI):
    return abs(phi1 - phi2) < threshold

def compare_p(p1, p2, threshold=DELTA_P):
    return abs(p1 - p2) < threshold

def compare_q(q1, q2, threshold=DELTA_Q):
    return abs(q1 - q2) < threshold