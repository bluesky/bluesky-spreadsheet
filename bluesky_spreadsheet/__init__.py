import pandas

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


class ExcelSpreadsheet:
    """
    A bluesky plan parameterized by an Excel spreadsheet

    Parameters
    ----------
    filepath : string
        path to Excel file
    plan : callable
        Expected signature: ``plan(row, state)`` where row is a row from the
        spreadsheet given as a dict, and state is an arbitrary dict that
        ``plan`` can use to stash information to persist across rows.
    quiet : boolean, optional
        False by default. Set True to silence printing of rows when they are
        parsed.
    """
    def __init__(self, filepath, plan, quiet=False):
        self.filepath = filepath
        self.plan = plan
        self._current_row = 0
        self.quiet = quiet
        self.state = {}

    def reset(self):
        """Reset the current row and clear the stashed state."""
        self._current_row = 0
        self.state.clear()

    def __call__(self, start_at=None):
        """Use the plan.

        Parameters
        ----------
        start_at : integer, optional
            If None, start where we left off from the last ``__call__``.
        """
        if start_at is not None:
            self._current_row = start_at
        while True:
            df = pandas.read_excel(self.filepath)
            try:
                row = df.loc[self._current_row].dropna().to_dict()
            except KeyError:
                # We have reached the end.
                break
            if not self.quiet:
                print(row)
            yield from self.plan(row, self.state)
            self._current_row += 1
