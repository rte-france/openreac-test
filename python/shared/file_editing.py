import os

def delete_all_the_files_in_directory(directory):
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