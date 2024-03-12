import json
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


def json_reader(path: str) -> dict:
    """read json file and return dict"""
    with open(path, "r") as file:
        data = json.load(file)
    return data
