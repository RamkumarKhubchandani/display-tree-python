import os
from typing import Tuple
from flask import Flask, render_template, request
from io import StringIO
from contextlib import redirect_stdout

app = Flask(__name__)

def print_directory(path: str, indentation_level: int = 0) -> Tuple[int, int]:
    """
    Recursively prints the directory structure of the given path.
    Returns a tuple (number of files, number of directories).
    """
    nfiles, ndirectories = 0, 0

    # Unicode symbols for tree structure
    branch = chr(9500)
    leaf = chr(9472)
    vert = chr(9474)
    space = chr(9472) + chr(9472)

    # Iterate over the directory entries
    with os.scandir(path) as entries:
        entries = sorted(entries, key=lambda f: f.name.lower())
        for i, entry in enumerate(entries):
            # Determine the appropriate symbol based on the position
            prefix = (space * (indentation_level - 1) + vert + space) if indentation_level else ""
            symbol = branch if entry.is_dir() else leaf

            # Print the file/directory name
            print(f"{prefix}{symbol} {entry.name}")

            # Recursively print subdirectories
            if entry.is_dir():
                ndirectories += 1
                files, dirs = print_directory(os.path.join(path, entry.name), indentation_level + 1)
                nfiles += files
                ndirectories += dirs
            else:
                nfiles += 1

    # Print the summary
    print(f"{space * indentation_level}{chr(9492)} {ndirectories} directories, {nfiles} files")

    return nfiles, ndirectories

# Command-line interface
# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(description="Display directory tree structure")
#     parser.add_argument("path", nargs="?", default=".", help="Path to the directory (default: current directory)")
#     args = parser.parse_args()

#     print_directory(args.path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        path = request.form['path']
        try:
            output = ""
            captured_output = StringIO()
            with redirect_stdout(captured_output):
                print_directory(path)
            output = captured_output.getvalue()
        except Exception as e:
            output = str(e)
    else:
        path = os.getcwd()
        output = ""

    return render_template('index.html', path=path, output=output)

if __name__ == '__main__':
    app.run(debug=True)
