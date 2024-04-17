def replace_lines_in_file(file_path, lines_to_replace, replacements):
    """
    Replace all the lines specified in lines_to_replace list by the lines specified in replacements list, in given file.
    The number of lines to replace must be equal to the number of replacements.
    """
    if len(lines_to_replace) != len(replacements):
        print(f"Number fo lines to replace must be equal to number of replacement.")
        return
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line_to_replace, replacement in zip(lines_to_replace, replacements):
        line_to_replace_index = lines.index(line_to_replace)
        if line_to_replace_index == -1:
            print(f"Line '{line_to_replace}' not found in the file '{file_path}'.")
            continue
        lines[line_to_replace_index] = replacement

    with open(file_path, 'w') as file:
        file.writelines(lines)

def add_lines_after_flags_in_file(file_path, lines_after_which_add, lines_to_add):
    """
    Add the lines specified in lines_to_add after flag lines specified in lines_after_which_add, in given file.
    The number of lines to add must be equal to the number of flag lines. 
    """
    if len(lines_after_which_add) != len(lines_to_add):
        print(f"Number fo lines to add must be equal to flags.")
        return
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line_after_which_add, line_to_add in zip(lines_after_which_add, lines_to_add):
        line_after_which_add_index = lines.index(line_after_which_add)
        if line_after_which_add_index == -1:
            print(f"Line '{line_after_which_add}' not found in the file '{file_path}'.")
            return
        lines.insert(line_after_which_add_index + 1, line_to_add)

    with open(file_path, 'w') as file:
        file.writelines(lines)

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

if __name__ == "__main__":
    import pathlib, shutil
    PARENT = pathlib.Path(__file__).parent.parent.parent
    TEMPO = PARENT / "tempo"
    AMPL_CODE = PARENT / "ampl"
    shutil.copyfile(AMPL_CODE / "divided" / "reactiveopf.run", TEMPO / "reactiveopf.run")
    get_reactiveopf_run_file_to_test_block(reactiveopf_run_path=TEMPO / "reactiveopf.run", avoided_blocks=["connex_component", "dcopf"], tested_block="acopf")


