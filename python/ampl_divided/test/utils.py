import shutil
import os

from .network import *
from shared.config import *
from shared.file_editing import *
from shared.openreac_output_loader import *
from shared.openreac_execution import *

RESOURCES_PATH = PYTHON_DIR / "ampl_divided" / "resources"

#########################################################
# Functions to run specific Open Reac results
#########################################################

def write_open_reac_param_files(output_path, param_shunts_content, param_transformers_content):
    with open(output_path / "param_shunts.txt", 'w') as f:
        f.write(param_shunts_content)
    with open(output_path / "param_transformers.txt", 'w') as f:
        f.write(param_transformers_content)

def run_cc_only(network, ampl_code_path, output_path, resources_path=None):
    """
    Run CC block on given network, using given AMPL code, in given output path.

    The AMPL code must be divided in three directories : 
        - ampl_code_path/divided, for the divided ampl code tested.
        - ampl_code_path/export_ampl_files, for the code exporting the blocks results.
        - ampl_code_path/importer_ampl_files, for the code importing the results of 
        the blocks preceding the one tested. 
    """
    non_executed_blocks = []
    ampl_files_to_import_results_non_executed_blocks = []
    results_files_non_executed_blocks = []
    run_block(network=network, ampl_code_path=ampl_code_path, tested_blocks=["connected_component"], 
            avoided_blocks=non_executed_blocks, output_path=output_path, resources_path=resources_path,
            ampl_files_to_import_results_non_executed_blocks=ampl_files_to_import_results_non_executed_blocks,
            results_files_non_executed_blocks=results_files_non_executed_blocks)


def run_dcopf_only(network, ampl_code_path, output_path, resources_path):
    """
    Run DCOPF block on given network, using given AMPL code, in given output path.

    The AMPL code must be divided in three different directories : 
        - ampl_code_path/divided, for the divided ampl code tested (in functionnal blocks).
        - ampl_code_path/export_ampl_files, for the code exporting the blocks results.
        - ampl_code_path/importer_ampl_files, for the code importing the results of the blocks preceding the one tested. 
    """
    non_executed_blocks = ["connected_component"]
    ampl_files_to_import_results_non_executed_blocks = ["connected_component_results_importer.run"]
    results_files_non_executed_blocks = ["connected_component_results.txt", "null_phase_bus.txt"]
    run_block(network=network, ampl_code_path=ampl_code_path, tested_blocks=["dcopf"], 
            avoided_blocks=non_executed_blocks, output_path=output_path, resources_path=resources_path,
            ampl_files_to_import_results_non_executed_blocks=ampl_files_to_import_results_non_executed_blocks,
            results_files_non_executed_blocks=results_files_non_executed_blocks)


def run_acopf(network, ampl_code_path, output_path, resources_path):
    """
    Run ACOPF block on given network, using given AMPL code, in given output path.

    The AMPL code must be divided in three different directories : 
        - ampl_code_path/divided, for the divided ampl code tested (in functionnal blocks).
        - ampl_code_path/export_ampl_files, for the code exporting the blocks results.
        - ampl_code_path/importer_ampl_files, for the code importing the results of the blocks preceding the one tested. 
    """

    non_executed_blocks = ["connected_component", "dcopf"]
    ampl_files_to_import_results_non_executed_blocks = [block + "_results_importer.run" for block in non_executed_blocks]
    results_files_non_executed_blocks = ["connected_component_results.txt", "null_phase_bus.txt", "dcopf_angle_results.txt"]
    run_block(network=network, ampl_code_path=ampl_code_path, tested_blocks=["acopf"], 
            avoided_blocks=non_executed_blocks, output_path=output_path, resources_path=resources_path,
            ampl_files_to_import_results_non_executed_blocks=ampl_files_to_import_results_non_executed_blocks,
            results_files_non_executed_blocks=results_files_non_executed_blocks)


def run_all_the_blocks(network, ampl_code_path, output_path):
    """
    Run open reac code and export all the blocks output.
    """
    non_executed_blocks = []
    ampl_files_to_import_results_non_executed_blocks = []
    results_files_non_executed_blocks = []
    run_block(network=network, ampl_code_path=ampl_code_path, tested_blocks=["connected_component", "dcopf", "acopf"],
            avoided_blocks=non_executed_blocks, output_path=output_path, resources_path="",
            ampl_files_to_import_results_non_executed_blocks=ampl_files_to_import_results_non_executed_blocks,
            results_files_non_executed_blocks=results_files_non_executed_blocks)

def run_block(network, ampl_code_path, tested_blocks, avoided_blocks, 
            output_path, ampl_files_to_import_results_non_executed_blocks, results_files_non_executed_blocks,
            resources_path=None, param_shunts_content="#empty\n", param_transformers_content="#empty\n"):
    """
    Run given OR block on given network. 
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
    execute_open_reac()
    
def get_reactiveopf_run_file_to_test_block(reactiveopf_run_path, avoided_blocks, tested_blocks):
    """
    Modify reactiveopf.run given file, to avoid the execution of the avoided_blocks, and replace it by importers of the results.
    It also add the exporter of the tested_block, to test its output.
    """
    # replace lines executing avoided blocks by others importing their results
    ampl_execution_of_avoided_blocks = ["include \"" + block + ".run\";\n" for block in avoided_blocks]
    files_to_import_results_of_avoided_blocks = [block + "_results_importer.run" for block in avoided_blocks]
    ampl_import_of_avoided_blocks = ["include \"" + import_results + "\";\n" for import_results in files_to_import_results_of_avoided_blocks]         
    replace_lines_in_file(reactiveopf_run_path, lines_to_replace=ampl_execution_of_avoided_blocks, replacements=ampl_import_of_avoided_blocks)

    # add ampl export after execution of tested_block
    ampl_execution_of_tested_blocks = ["include \"" + tested_block + ".run\";\n" for tested_block in tested_blocks]
    ampl_export_of_tested_blocks = ["include \"" + tested_block + "_output.run\";\n" for tested_block in tested_blocks]
    add_lines_after_flags_in_file(reactiveopf_run_path, lines_after_which_add=ampl_execution_of_tested_blocks, lines_to_add=ampl_export_of_tested_blocks)
