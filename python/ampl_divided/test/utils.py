import shutil
import os
import pandas as pd
from reactiveopf_run_to_test_block import *
from subprocess import Popen, PIPE

DELTA_V = 0.001
DELTA_ANGLE = 0.001
DELTA_P = 0.001
DELTA_Q = 0.001


def is_diff_less_than_threshold(x, y, threshold):
    """
    Parameters:
        a (float): First value.
        b (float): Second value.
        threshold (float): Threshold value.
        
    Returns:
        bool: True if |a - b| < threshold, False otherwise.
    """
    return abs(x - y) < threshold


#########################################################
# Import open reac results
#########################################################

def import_connected_component_results(output_path):
    """
    Import the results of the CC optimization problem.
    The results consist of null phase bus and buses in the main connected component.
    """
    bus_cc_file = "connected_component_results.txt"
    null_phase_bus_file = "null_phase_bus.txt"

    # import bus_cc file result
    bus_cc = pd.read_csv(output_path / bus_cc_file, sep=" ", header=0)
    bus_cc.rename(columns=lambda x: x.replace('#', ''), inplace=True)

    # import null_phase_bus result
    with open(output_path / null_phase_bus_file, 'r') as f:
        next(f) # first line is a comment
        null_phase_bus = int(next(f).strip())

    return bus_cc, null_phase_bus

def import_dcopf_results(output_path):
    """
    Import the results of the DCOPF optimization problem.
    The results consist of voltage angles computed for each bus of the main connected component.
    """
    angle_results_file = "dcopf_angle_results.txt"
    angle_results = pd.read_csv(output_path / angle_results_file, sep=" ", header=0)
    angle_results.rename(columns=lambda x: x.replace('#', ''), inplace=True)
    return angle_results

def import_acopf_results(output_path):
    """
    Import the results of the ACOPF optimization problem.
    The results consist of voltage results for each bus, and flows for each branch of the main connected component.
    """
    voltage_results_file_name = "acopf_voltage_results.txt"
    voltage_results = pd.read_csv(output_path / voltage_results_file_name, sep=" ", header=0)
    voltage_results.rename(columns=lambda x: x.replace('#', ''), inplace=True)

    flows_results_file_name = "acopf_flows_results.txt"
    flows_results = pd.read_csv(output_path / flows_results_file_name, sep=" ", header=0)
    flows_results.rename(columns=lambda x: x.replace('#', ''), inplace=True)
    
    return voltage_results, flows_results


#########################################################
# Functions to run specific Open Reac results
#########################################################

def write_open_reac_param_files(output_path, param_shunts_content, param_transformers_content):
    with open(output_path / "param_shunts.txt", 'w') as f:
        f.write(param_shunts_content)
    with open(output_path / "param_transformers.txt", 'w') as f:
        f.write(param_transformers_content)

def run_connected_component(network, ampl_code_path, output_path, resources_path):
    """
    Run CC block on given network, using AMPL code situated in given path, in given output path.

    The AMPL code must be divided in three different directories : 
        - ampl_code_path/divided, for the divided ampl code tested (in functionnal blocks).
        - ampl_code_path/export_ampl_files, for the code exporting the blocks results.
        - ampl_code_path/importer_ampl_files, for the code importing the results of the blocks preceding the one tested. 
    """

    # list of blocks preceding DCOPF and that must not be executed
    non_executed_blocks = []
    # list of ampl files used to import the results of the non_executed_blocks
    ampl_files_to_import_results_non_executed_blocks = []
    # list of files with results of non_executed_blocks
    results_files_non_executed_blocks = []

    run_open_reac_block(network=network, ampl_code_path=ampl_code_path, tested_blocks=["connected_component"], 
                        avoided_blocks=non_executed_blocks, output_path=output_path, resources_path=resources_path,
                        ampl_files_to_import_results_non_executed_blocks=ampl_files_to_import_results_non_executed_blocks,
                        results_files_non_executed_blocks=results_files_non_executed_blocks)

def run_dcopf(network, ampl_code_path, output_path, resources_path):
    """
    Run DCOPF block on given network, using AMPL code situated in given path, in given output path.

    The AMPL code must be divided in three different directories : 
        - ampl_code_path/divided, for the divided ampl code tested (in functionnal blocks).
        - ampl_code_path/export_ampl_files, for the code exporting the blocks results.
        - ampl_code_path/importer_ampl_files, for the code importing the results of the blocks preceding the one tested. 
    """

    # list of blocks preceding DCOPF and that must not be executed
    non_executed_blocks = ["connected_component"]
    # list of ampl files used to import the results of the non_executed_blocks
    ampl_files_to_import_results_non_executed_blocks = ["connected_component_results_importer.run"]
    # list of files with results of non_executed_blocks
    results_files_non_executed_blocks = ["connected_component_results.txt", "null_phase_bus.txt"]

    run_open_reac_block(network=network, ampl_code_path=ampl_code_path, tested_blocks=["dcopf"], 
                        avoided_blocks=non_executed_blocks, output_path=output_path, resources_path=resources_path,
                        ampl_files_to_import_results_non_executed_blocks=ampl_files_to_import_results_non_executed_blocks,
                        results_files_non_executed_blocks=results_files_non_executed_blocks)


def run_acopf(network, ampl_code_path, output_path, resources_path):
    """
    Run ACOPF block on given network, using AMPL code situated in given path, in given output path.

    The AMPL code must be divided in three different directories : 
        - ampl_code_path/divided, for the divided ampl code tested (in functionnal blocks).
        - ampl_code_path/export_ampl_files, for the code exporting the blocks results.
        - ampl_code_path/importer_ampl_files, for the code importing the results of the blocks preceding the one tested. 
    """

    # list of blocks preceding ACOPF and that must not be executed
    non_executed_blocks = ["connected_component", "dcopf"]
    # list of ampl files used to import the results of the non_executed_blocks
    ampl_files_to_import_results_non_executed_blocks = [block + "_results_importer.run" for block in non_executed_blocks]
    # list of files with results of non_executed_blocks
    results_files_non_executed_blocks = ["connected_component_results.txt", "null_phase_bus.txt", "dcopf_angle_results.txt"]

    run_open_reac_block(network=network, ampl_code_path=ampl_code_path, tested_blocks=["acopf"], 
                        avoided_blocks=non_executed_blocks, output_path=output_path, resources_path=resources_path,
                        ampl_files_to_import_results_non_executed_blocks=ampl_files_to_import_results_non_executed_blocks,
                        results_files_non_executed_blocks=results_files_non_executed_blocks)


def run_open_reac_block(network, ampl_code_path, tested_blocks, avoided_blocks, 
                        output_path, resources_path, ampl_files_to_import_results_non_executed_blocks, results_files_non_executed_blocks,
                        param_shunts_content="#empty\n", param_transformers_content="#empty\n"):
    """
    Run given AMPL block on given network. 
    
    AMPL functionnal blocks, optionnal parameters files, exporters and importers 
    are copied/pasted from source to output_path, where the execution is done.
    """

    # export the network with ampl format into output_path
    network.save(os.path.join(output_path, "ampl.xiidm"), format="AMPL")

    # copy/paste ampl divided code in output_path
    shutil.copytree(ampl_code_path / "divided", output_path, dirs_exist_ok=True)

    # copy/paste ampl code to export output of the tested block
    tested_block_files = [tested_block + "_output.run" for tested_block in tested_blocks]
    for tested_block_file in tested_block_files:
        shutil.copyfile(ampl_code_path / "output" / tested_block_file, output_path / tested_block_file)

    # copy/paste ampl code to import results of non executed blocks
    for ampl_file_to_import_results in ampl_files_to_import_results_non_executed_blocks:
        shutil.copyfile(ampl_code_path / "input" / ampl_file_to_import_results, output_path / ampl_file_to_import_results)

    # copy/paste results of the non executed blocks, in order to import them
    for results_file in results_files_non_executed_blocks:
        shutil.copyfile(resources_path / network.id / results_file, output_path / results_file)

    # write files to parameterize ampl run in output path
    write_open_reac_param_files(output_path, param_shunts_content, param_transformers_content)

    # modify reactiveopf.run file to import results of avoided block (they are not executed) and export results of tested block
    get_reactiveopf_run_file_to_test_block(reactiveopf_run_path=output_path/"reactiveopf.run", avoided_blocks=avoided_blocks, tested_blocks=tested_blocks)

    # execute the ampl code
    os.chdir(output_path)
    p = Popen(["ampl", "reactiveopf.run"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.communicate()
    p.wait()


def get_all_open_reac_output(network, ampl_code_path, output_path):
    """
    Run open reac code and export all the blocks output.
    """
    run_open_reac_block(network=network, ampl_code_path=ampl_code_path, tested_blocks=["connected_component", "dcopf", "acopf"],
                        avoided_blocks=[], output_path=output_path, resources_path="",
                        ampl_files_to_import_results_non_executed_blocks=[],
                        results_files_non_executed_blocks=[])