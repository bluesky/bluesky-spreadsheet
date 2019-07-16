import pandas

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


class ExcelSpreadsheet:
    """
    A bluesky plan parameterized by an Excel spreadsheet

    Parameters
    ----------
    filepath: string
        path to Excel file
    plan: callable
        Expected signature: ``plan(row)`` where row is a row from the
        spreadsheet given as a dict.
    quiet: boolean, optional
        False by default. Set True to silence printing of rows when they are
        parsed.

    Attributes
    ----------
    filepath
    plan
    quiet
    """
    def __init__(self, filepath, plan, quiet=False):
        self.filepath = filepath
        self.plan = plan
        self._current_row = 0
        self.quiet = quiet

    def __call__(self, start_at=None):
        """Use the plan.

        Parameters
        ----------
        start_at: integer, optional
            If None, start where we left off from the last ``__call__``.
        """
        if start_at is not None:
            self._current_row = start_at
        while True:
            df = pandas.read_excel(self.filepath)
            try:
                row = df.ffill().loc[self._current_row].to_dict()
            except KeyError:
                # We have reached the end.
                break
            if not self.quiet:
                print(row)
            yield from self.plan(row)
            self._current_row += 1
