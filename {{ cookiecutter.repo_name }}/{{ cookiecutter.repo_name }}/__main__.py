'''
This is the main entry point for the {{ cookiecutter.formal_name }} GUI.
'''
from Tkinter import *

import argparse

from bugjar import VERSION
from bugjar.view import MainWindow


def main():
    parser = argparse.ArgumentParser(
        description='{{ cookiecutter.description }}',
        version=VERSION
    )

    # parser.add_argument(
    #     'filename',
    #     metavar='script.py',
    #     help='The script to debug.'
    # )
    # parser.add_argument(
    #     'args', nargs=argparse.REMAINDER,
    #     help='Arguments to pass to the script you are debugging.'
    # )

    options = parser.parse_args()

    # Set up the root Tk context
    root = Tk()

    # Construct a window debugging the nominated program
    view = MainWindow(root, options)

    # Run the main loop
    try:
        view.mainloop()
    except KeyboardInterrupt:
        view.on_quit()

if __name__ == '__main__':
    main()
