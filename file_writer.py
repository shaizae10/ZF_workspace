import os

def write_file(directory, filename, content):
    """Write content to a file inside a directory."""
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as file:
        file.write(content)

def write_files(directory, files):
    """Write multiple files inside a directory."""
    for filename, content in files.items():
        write_file(directory, filename, content)
