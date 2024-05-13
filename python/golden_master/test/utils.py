# imports
import pathlib
import filecmp
import shutil
import os
from collections import Counter
from subprocess import Popen, PIPE
from io_files import *

# paths
ROOT_PROJECT = pathlib.Path(__file__).parent.parent.parent.parent
OUTPUT_PATH = ROOT_PROJECT / "output"
AMPL_DIVIDED_CODE_PATH = ROOT_PROJECT / "ampl" / "divided"

PYTHON = ROOT_PROJECT / "python"
#GOLDEN_MASTER_PATH = PYTHON / "golden_master" / "resources"
GOLDEN_MASTER_PATH = ROOT_PROJECT.parent / "golden_master"

def delete_files_in_directory(directory):
    try:
        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            # Check if the path is a file (not a directory)
            if os.path.isfile(file_path):
                # Delete the file
                os.remove(file_path)
                print(f"Deleted {file_path}")
        print("All files deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def open_reac_output_comparison(test, verbose=False):
    """
    Test if there are differences in output between execution of original ampl code and divided one, on given test.
    Return: True if no difference, False otherwise.
    """
    golden_test_path = GOLDEN_MASTER_PATH / test
    output_test_path = OUTPUT_PATH # this path must exist before copy/paste the files

    # clean output path
    if str(output_test_path).endswith("output"):
        delete_files_in_directory(output_test_path)

    # copy/paste test network data and open reac parameter files
    for file in os.listdir(golden_test_path):
        if file.endswith(".txt") and file != INDICATORS_FILE:
            shutil.copy(golden_test_path / file, output_test_path / file)

    # copy/paste divided ampl code to test its execution
    shutil.copytree(AMPL_DIVIDED_CODE_PATH, output_test_path, dirs_exist_ok=True)

    # change directory of execution and execute divided ampl code
    os.chdir(output_test_path)
    p = Popen(["ampl", "reactiveopf.run"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    # compare expected/actual printings of reactiveopf.run
    actual_printings = [line.decode("utf-8").replace("\r\n","\n") for line in list(p.stdout)]
    printings_differences = comparison_open_reac_printings(golden_test_path / AMPL_PRINTING_FILE, actual_printings) # list of differences
    if bool(printings_differences):
        print("Difference in comparision of printings.")
        if verbose:
            print(printings_differences)

    # compare expected/actual indicators of open reac
    indicators_differences = comparison_open_reac_indicators(golden_test_path / INDICATORS_FILE, output_test_path / INDICATORS_FILE) # list of differences
    if bool(indicators_differences):
        print("Difference in comparision of indicators.")
        if verbose:
            print(indicators_differences)

    indicators = load_indicators(output_test_path / INDICATORS_FILE)
    or_csv_files_to_compare = OR_CSV_RESULTS_FILES
    if indicators["log_level_ampl"] == "DEBUG":
        or_csv_files_to_compare.add("reactiveopf_results_generators_Pnull.csv")
        or_csv_files_to_compare.add("debug_bus.csv")
    if indicators["final_status"] != "OK":
        or_csv_files_to_compare = []
    
    # compare expected/actual results of open reac
    are_results_different = comparison_open_reac_results(golden_test_path, output_test_path, or_csv_files_to_compare) # boolean
    if not are_results_different:
        print("Difference in comparision of csv results.")

    return not bool(printings_differences) and not bool(indicators_differences) and are_results_different # True if no differences in comparisons

def load_indicators(path_file, to_ignore=[]):
    """
    Load the indicators of open reac reactiveopf_results_indic.txt file. 
    The ones at indexes specified in to_ginore are not loaded.
    Return: The list of indicators as a dictionnary.
    """
    indicators = {}
    file = open(path_file)
    for num, line in enumerate(list(filter(lambda a: a != "\n" and a != "", file.readlines()))):
        # avoid ignored indicators
        if num in to_ignore:
            continue
        values = line.split(" ")
        indicators[values[0]] = values[1]
    return indicators
    
def comparison_open_reac_indicators(expected_file_path, actual_path_file):
    """
    Compare the two indicators file given as argument.
    Return: The set containing different keys or values between compared files.
    """
    # indicators that must not be compared, due to dependance on the time/machine of execution
    to_ignore = [2,3] + [i for i in range(6,13)]
    
    # load indicators, except ignored ones, as dictionnaries
    expected_indicators = load_indicators(expected_file_path, to_ignore=to_ignore)
    actual_indicators = load_indicators(actual_path_file, to_ignore=to_ignore)
    
    # comparison of the keys
    keys_diff = set(expected_indicators.keys()) ^ set(actual_indicators.keys())
    # comparison of the values
    values_diff = {key: (expected_indicators[key], actual_indicators[key])      
                   for key in set(expected_indicators.keys()) & set(actual_indicators.keys()) 
                   if expected_indicators[key] != actual_indicators[key]}

    return keys_diff.union(values_diff.items())


def comparison_open_reac_results(expected_directory_path, actual_directory_path, files_to_compare):
    """
    Compare the files given as argument in the two directories expected and actual.
    Return: True if no difference, False otherwise.
    """
    _, mismatchs, errors = filecmp.cmpfiles(expected_directory_path, actual_directory_path, files_to_compare)
    return len(errors) == 0 and len(mismatchs) == 0


def comparison_open_reac_printings(expected_printings_path, printings):
    """
    Compare the printings given as a list in printings, and in the directory expected_printings_path.
    Return: The list of differences between the expected/actual printings of open reac ampl code.
    """
    file = open(expected_printings_path)
    expected_printings = file.readlines()

    # list of printings that must not be compared, due to dependance on the time/machine of execution
    to_ignore = ["Start of file", "End of file", "Elapsed time since start", 
                 "solve: start", "solve: end", "Total program time", "Time spent in evaluations", 
                 "é", "Ã©", "Commercial", "Trial", "COMMERCIAL USE", "\n"]
    
    # lists of printings, without ignored ones
    filtered_expected_printings = [line for line in expected_printings if all(substring not in line for substring in to_ignore)]
    filtered_act_printings = [line for line in printings if all(substring not in line for substring in to_ignore)]
    
    # count the number of different printings
    counter_expected = Counter(filtered_expected_printings)
    counter_actual = Counter(filtered_act_printings)
    difference_expected_actual = counter_expected - counter_actual # printings in expected but not in actual (with occurrences)
    difference_actual_expected = counter_actual - counter_expected # printings in actual but not in expected

    return difference_expected_actual + difference_actual_expected