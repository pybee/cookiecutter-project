from ttk import *

from tkreadonly import ReadOnlyCode

from pygments.lexers import PythonLexer


class CodeView(ReadOnlyCode):
    def __init__(self, *args, **kwargs):
        kwargs['lexer'] = PythonLexer(stripnl=False)
        ReadOnlyCode.__init__(self, *args, **kwargs)


class FileView(Treeview):
    def __init__(self, *args, **kwargs):
        # Only a single stack frame can be selected at a time.
        kwargs['selectmode'] = 'browse'
        self.normalizer = kwargs.pop('normalizer')
        Treeview.__init__(self, *args, **kwargs)

        # self['columns'] = ('line',)
        # self.column('line', width=100, anchor='center')
        self.heading('#0', text='File')
        # self.heading('line', text='Line')

        # Set up styles for line numbers
        self.tag_configure('enabled', foreground='red')
        self.tag_configure('disabled', foreground='gray')
        self.tag_configure('ignored', foreground='green')
        self.tag_configure('temporary', foreground='pink')

    def insert_filename(self, filename):
        "Ensure that a specific filename exists in the breakpoint tree"
        if not self.exists(filename):
            # First, establish the index at which to insert this child.
            # Do this by getting a list of children, sorting the list by name
            # and then finding how many would sort less than the label for
            # this node.
            files = sorted(self.get_children(''), reverse=False)
            index = len([item for item in files if item > filename])

            # Now insert a new node at the index that was found.
            self.insert(
                '', index, self._nodify(filename),
                text=self.normalizer(filename),
                open=True,
                tags=['file']
            )

    def update_breakpoint(self, bp):
        """Update the visualization of a breakpoint in the tree.

        If the breakpoint isn't arlready on the tree, add it.
        """
        self.insert_filename(bp.filename)

        # Determine the right tag for the line number
        if bp.enabled:
            if bp.temporary:
                tag = 'temporary'
            else:
                tag = 'enabled'
        else:
            tag = 'disabled'

        # Update the display for the line number,
        # adding a new tree node if necessary.
        if self.exists(unicode(bp)):
            self.item(unicode(bp), tags=['breakpoint', tag])
        else:
            # First, establish the index at which to insert this child.
            # Do this by getting a list of children, sorting the list by name
            # and then finding how many would sort less than the label for
            # this node.
            lines = sorted((int(self.item(item)['text']) for item in self.get_children(bp.filename)), reverse=False)
            index = len([line for line in lines if line < bp.line])

            # Now insert a new node at the index that was found.
            self.insert(
                self._nodify(bp.filename), index, unicode(bp),
                text=unicode(bp.line),
                open=True,
                tags=['breakpoint', tag]
            )

    def _nodify(self, node):
        "Escape any problem characters in a node name"
        return node.replace('\\', '/')

    def selection_set(self, node):
        """Node names on the breakpoint tree are the filename.

        On Windows, this requires escaping, because backslashes
        in filenames cause problems with Tk.
        """
        Treeview.selection_set(self, self._nodify(node))
