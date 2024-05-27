import shutil
import os
from subprocess import Popen, PIPE

from shared.config import *
from shared.file_editing import *
from shared.openreac_output_loader import *
from shared.openreac_output_comparison import *

GOLDEN_MASTER_PATH = PYTHON_DIR / "golden_master" / "resources"

def open_reac_output_comparison(test, verbose=False):
    """
    Test if there are differences in output between execution of original ampl code and divided one, on given test.
    Return: True if no difference, False otherwise.
    """
    golden_test_path = GOLDEN_MASTER_PATH / test
    output_test_path = OUTPUT_DIR # this path must exist before copy/paste the files

    # clean output path
    if str(output_test_path).endswith("output"):
        delete_all_the_files_in_directory(output_test_path)
    
    # copy/paste test network data and open reac parameter files
    for file in os.listdir(golden_test_path):
        if file.endswith(".txt") and file != INDICATORS_FILE:
            shutil.copy(golden_test_path / file, output_test_path / file)

    # copy/paste divided ampl code to test its execution
    shutil.copytree(AMPL_DIVIDED_DIR, output_test_path, dirs_exist_ok=True)

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

    indicators = load_open_reac_indicators(output_test_path / INDICATORS_FILE)
    or_csv_files_to_compare = OR_CSV_RESULTS_FILES
    if indicators["log_level_ampl"] == "DEBUG":
        or_csv_files_to_compare.add("reactiveopf_results_generators_Pnull.csv")
        or_csv_files_to_compare.add("debug_bus.csv")
    if indicators["final_status"] != "OK":
        or_csv_files_to_compare = []
    
    # compare expected/actual results of open reac
    are_results_different = compare_open_reac_csv_results(golden_test_path, output_test_path, or_csv_files_to_compare) # boolean
    if not are_results_different:
        print("Difference in comparision of csv results.")

    return not bool(printings_differences) and not bool(indicators_differences) and are_results_different # True if no differences in comparisons

if __name__ == "__main__":
    open_reac_output_comparison("ieee14", True)