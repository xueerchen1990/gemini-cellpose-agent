import os
import importlib
import re
import sys
from io import StringIO
import traceback
import PIL.Image

def get_package_source_path(package_name):
    try:
        # Import the package
        package = importlib.import_module(package_name)

        # Get the file path of the package
        package_file = package.__file__

        # Get the directory containing the package
        package_dir = os.path.dirname(package_file)

        return package_dir
    except ImportError:
        return f"Package '{package_name}' not found."
    except AttributeError:
        return f"Package '{package_name}' is a built-in or not a standard package."

def read_python_files_and_write_to_output(folder_path, output_text_path):
    with open(output_text_path, 'w', encoding='utf-8') as output_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    output_file.write(f"File Path: {file_path}\n")
                    with open(file_path, 'r', encoding='utf-8') as python_file:
                        content = python_file.read()
                        output_file.write(content)
                        output_file.write('\n\n')  # Adding a separator between files

def load_env(env_file='.env'):
    """
    Load environment variables from a .env file into the environment.

    :param env_file: The path to the .env file. Defaults to '.env' in the current directory.
    """
    try:
        with open(env_file, 'r') as file:
            for line in file:
                # Strip leading/trailing whitespace and skip empty lines and comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Split the line into key and value
                key, value = line.split('=', 1)

                # Strip any quotes around the value
                value = value.strip("'\"")

                # Set the environment variable
                os.environ[key.strip()] = value

        print(f"Environment variables loaded from {env_file}")
    except FileNotFoundError:
        print(f"Warning: {env_file} not found. No environment variables loaded.")
    except Exception as e:
        print(f"Error loading environment variables: {e}")

def load_text(text_path:str) -> str:
    # Load the notebook from the given path
    with open(text_path, 'r') as file:
        text = file.read()
    return text

def count_tokens(text_or_path:str) -> int:
    if os.path.isfile(text_or_path):
        text = load_text(text_or_path)
    else:
        text = text_or_path
    return count_tokens_in_text(text)

def count_tokens_in_text(text):
    import google.generativeai as genai
    # Use the tiktoken library to count the number of tokens in the text
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    return model.count_tokens(text)

def add_print_statements(code):
    lines = code.split('\n')
    variable_names = set()

    # Regular expression to find variable assignments
    pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*')

    output_lines = []
    for line in lines:
        match = pattern.match(line)
        if match:
            var_name = match.group(1)
            if var_name not in variable_names:
                variable_names.add(var_name)
                output_lines.append(line)
                indent = re.match(r'^\s*', line).group(0)
                output_lines.append(f'{indent}print("Type of {var_name}:", type({var_name}))')
                output_lines.append(f'{indent}if hasattr({var_name}, "shape"):')
                output_lines.append(f'{indent}    print("Shape of {var_name}:", {var_name}.shape)')
            else:
                output_lines.append(line)
        else:
            output_lines.append(line)

    return '\n'.join(output_lines)

def exec_code(code):
    # Create a StringIO object to capture the output
    output_capture = StringIO()
    
    # Redirect stdout to the StringIO object
    original_stdout = sys.stdout
    sys.stdout = output_capture
    error_message = None
    try:
        # Execute the code
        exec(code)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        error_info = traceback.format_exc()

        # Extract the last frame of the traceback
        last_frame = tb[1]
        error_line = code.split('\n')[last_frame.lineno - 1].strip()
        error_message = f"Error occurred at line {last_frame.lineno} in {last_frame.filename}:\n{error_line}\n{error_info}"
    finally:
        # Restore the original stdout
        sys.stdout = original_stdout
    
    # Get the captured output
    captured_output = output_capture.getvalue()
    return captured_output, error_message

def is_image(file_path):
    """
    Check if a file is an image based on its extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    # List of common image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp']

    # Get the file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # Check if the file extension is in the list of image extensions
    return file_extension in image_extensions

def append_image_metadata(message):
    """
    Appends the content of image files attached to a message to the message content.
    Args:
        message (cl.Message): The input message.

    Returns:
        list: The updated message content with attached image files appended.
    """
    input_msg = message.content
    # Processing attachments
    files = message.elements
    print(files)
    if len(files):
        for fi in files:
            if is_image(fi.path):
                if isinstance(input_msg, list):
                    input_msg.append(PIL.Image.open(fi.path))
                else:
                    input_msg = [input_msg, PIL.Image.open(fi.path)]
    return input_msg

if __name__ == "__main__":
    #load_env()
    # package_name = 'cellpose'
    # package_source_path = get_package_source_path(package_name)
    # print(f"Package '{package_name}' source path: {package_source_path}")
    # read_python_files_and_write_to_output(package_source_path, 'cellpose_source.txt')
    file_path = '../notebooks/cellpose_notebooks.txt'
    num_tokens = count_tokens(file_path)
    print(num_tokens)