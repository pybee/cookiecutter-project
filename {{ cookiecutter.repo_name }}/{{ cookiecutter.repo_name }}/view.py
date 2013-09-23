"""A module containing a visual representation of the connection

This is the "View" of the MVC world.
"""
import os
from Tkinter import *
from tkFont import *
from ttk import *
import webbrowser

from {{ cookiecutter.repo_name }} import VERSION, NUM_VERSION
from {{ cookiecutter.repo_name }}.widgets import CodeView, FileView

def filename_normalizer(base_path):
    """Generate a fuction that will normalize a full path into a
    display name, by removing a common prefix.

    In most situations, this will be removing the current working
    directory.
    """
    def _normalizer(filename):
        if filename.startswith(base_path):
            return filename[len(base_path):]
        else:
            return filename
    return _normalizer


class MainWindow(object):
    def __init__(self, root, options):
        '''
        -----------------------------------------------------
        | main button toolbar                               |
        -----------------------------------------------------
        |       < ma | in content area >                    |
        |            |                                      |
        | File list  | File name                            |
        |            |                                      |
        -----------------------------------------------------
        |     status bar area                               |
        -----------------------------------------------------

        '''

        # Obtain and expand the current working directory.
        base_path = os.path.abspath(os.getcwd())
        base_path = os.path.normcase(base_path) + '/'

        # Create a filename normalizer based on the CWD.
        self.filename_normalizer = filename_normalizer(base_path)

        # Root window
        self.root = root
        self.root.title('{{ cookiecutter.formal_name }}')
        self.root.geometry('1024x768')

        # Prevent the menus from having the empty tearoff entry
        self.root.option_add('*tearOff', FALSE)
        # Catch the close button
        self.root.protocol("WM_DELETE_WINDOW", self.cmd_quit)
        # Catch the "quit" event.
        self.root.createcommand('exit', self.cmd_quit)

        # Setup the menu
        self._setup_menubar()

        # Set up the main content for the window.
        self._setup_button_toolbar()
        self._setup_main_content()
        self._setup_status_bar()

        # Now configure the weights for the root frame
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)

    ######################################################
    # Internal GUI layout methods.
    ######################################################

    def _setup_menubar(self):
        # Menubar
        self.menubar = Menu(self.root)

        # self.menu_Apple = Menu(self.menubar, name='Apple')
        # self.menubar.add_cascade(menu=self.menu_Apple)

        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.menu_help = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_help, label='Help')

        # self.menu_Apple.add_command(label='Test', command=self.cmd_dummy)

        # self.menu_file.add_command(label='New', command=self.cmd_dummy, accelerator="Command-N")
        # self.menu_file.add_command(label='Close', command=self.cmd_dummy)

        self.menu_help.add_command(label='Open Documentation', command=self.cmd_{{ cookiecutter.repo_name }}_docs)
        self.menu_help.add_command(label='Open {{ cookiecutter.formal_name }} project page', command=self.cmd_{{ cookiecutter.repo_name }}_page)
        self.menu_help.add_command(label='Open {{ cookiecutter.formal_name }} on GitHub', command=self.cmd_{{ cookiecutter.repo_name }}_github)
        self.menu_help.add_command(label='Open BeeWare project page', command=self.cmd_beeware_page)

        # last step - configure the menubar
        self.root['menu'] = self.menubar

    def _setup_button_toolbar(self):
        '''
        The button toolbar runs as a horizontal area at the top of the GUI.
        It is a persistent GUI component
        '''

        # Main toolbar
        self.toolbar = Frame(self.root)
        self.toolbar.grid(column=0, row=0, sticky=(W, E))

        # Buttons on the toolbar
        self.run_button = Button(self.toolbar, text='Run', command=self.cmd_run)
        self.run_button.grid(column=0, row=0)

        self.toolbar.columnconfigure(0, weight=0)
        self.toolbar.rowconfigure(0, weight=0)

    def _setup_main_content(self):
        '''
        Sets up the main content area. It is a persistent GUI component
        '''

        # Main content area
        self.content = PanedWindow(self.root, orient=HORIZONTAL)
        self.content.grid(column=0, row=1, sticky=(N, S, E, W))

        # Create subregions of the content
        self._setup_file_tree()
        self._setup_code_area()

        # Set up weights for the left frame's content
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=1)

        self.content.pane(0, weight=1)
        self.content.pane(1, weight=2)

    def _setup_file_tree(self):
        self.file_tree_frame = Frame(self.content)
        self.file_tree_frame.grid(column=0, row=0, sticky=(N, S, E, W))

        self.file_tree = FileView(self.file_tree_frame, normalizer=self.filename_normalizer)
        self.file_tree.grid(column=0, row=0, sticky=(N, S, E, W))

        # # The tree's vertical scrollbar
        self.file_tree_scrollbar = Scrollbar(self.file_tree_frame, orient=VERTICAL)
        self.file_tree_scrollbar.grid(column=1, row=0, sticky=(N, S))

        # # Tie the scrollbar to the text views, and the text views
        # # to each other.
        self.file_tree.config(yscrollcommand=self.file_tree_scrollbar.set)
        self.file_tree_scrollbar.config(command=self.file_tree.yview)

        # Setup weights for the "file_tree" tree
        self.file_tree_frame.columnconfigure(0, weight=1)
        self.file_tree_frame.columnconfigure(1, weight=0)
        self.file_tree_frame.rowconfigure(0, weight=1)

        # Handlers for GUI events
        self.file_tree.bind('<<TreeviewSelect>>', self.on_file_selected)

        self.content.add(self.file_tree_frame)

    def _setup_code_area(self):
        self.code_frame = Frame(self.content)
        self.code_frame.grid(column=1, row=0, sticky=(N, S, E, W))

        # Label for current file
        self.current_file = StringVar()
        self.current_file_label = Label(self.code_frame, textvariable=self.current_file)
        self.current_file_label.grid(column=0, row=0, sticky=(W, E))

        # Code display area
        self.code = CodeView(self.code_frame)
        self.code.grid(column=0, row=1, sticky=(N, S, E, W))

        # Set up weights for the code frame's content
        self.code_frame.columnconfigure(0, weight=1)
        self.code_frame.rowconfigure(0, weight=0)
        self.code_frame.rowconfigure(1, weight=1)

        self.content.add(self.code_frame)

    def _setup_status_bar(self):
        # Status bar
        self.statusbar = Frame(self.root)
        self.statusbar.grid(column=0, row=2, sticky=(W, E))

        # Current status
        self.run_status = StringVar()
        self.run_status_label = Label(self.statusbar, textvariable=self.run_status)
        self.run_status_label.grid(column=0, row=0, sticky=(W, E))
        self.run_status.set('Not running')

        # Main window resize handle
        self.grip = Sizegrip(self.statusbar)
        self.grip.grid(column=1, row=0, sticky=(S, E))

        # Set up weights for status bar frame
        self.statusbar.columnconfigure(0, weight=1)
        self.statusbar.columnconfigure(1, weight=0)
        self.statusbar.rowconfigure(0, weight=0)

    ######################################################
    # Utility methods for controlling content
    ######################################################

    def show_file(self, filename, line=None, breakpoints=None):
        """Show the content of the nominated file.

        If specified, line is the current line number to highlight. If the
        line isn't currently visible, the window will be scrolled until it is.

        breakpoints is a list of line numbers that have current breakpoints.

        If refresh is true, the file will be reloaded and redrawn.
        """
        # Set the filename label for the current file
        self.current_file.set(self.filename_normalizer(filename))

        # Update the code view; this means changing the displayed file
        # if necessary, and updating the current line.
        if filename != self.code.filename:
            self.code.filename = filename

        self.code.line = line

    ######################################################
    # TK Main loop
    ######################################################

    def mainloop(self):
        self.root.mainloop()

    ######################################################
    # TK Command handlers
    ######################################################

    def cmd_quit(self):
        "Quit the program"
        self.root.quit()

    def cmd_run(self, event=None):
        "Run ... whatever that means"

    def cmd_{{ cookiecutter.repo_name }}_page(self):
        "Show the {{ cookiecutter.formal_name }} project page"
        webbrowser.open_new('http://pybee.org/{{ cookiecutter.repo_name }}')

    def cmd_{{ cookiecutter.repo_name }}_github(self):
        "Show the {{ cookiecutter.formal_name }} GitHub repo"
        webbrowser.open_new('http://github.com/pybee/{{ cookiecutter.repo_name }}')

    def cmd_{{ cookiecutter.repo_name }}_docs(self):
        "Show the {{ cookiecutter.formal_name }} documentation"
        # If this is a formal release, show the docs for that
        # version. otherwise, just show the head docs.
        if len(NUM_VERSION) == 3:
            webbrowser.open_new('http://{{ cookiecutter.repo_name }}.readthedocs.org/en/v%s/' % VERSION)
        else:
            webbrowser.open_new('http://{{ cookiecutter.repo_name }}.readthedocs.org/')

    def cmd_beeware_page(self):
        "Show the BeeWare project page"
        webbrowser.open_new('http://pybee.org/')

    ######################################################
    # Handlers for GUI actions
    ######################################################

    def on_file_selected(self, event):
        "When a file is selected, highlight the file and line"
        if event.widget.selection():
            _, index = event.widget.selection()[0].split(':')
            # line, frame = self.debugger.stack[int(index)]

            # Display the file in the code view
            self.show_file(filename=frame['filename'], line=line)

            # Display the contents of the selected frame in the inspector
            self.inspector.show_frame(frame)

            # Clear any currently selected item on the breakpoint tree
            self.breakpoints.selection_remove(self.breakpoints.selection())
