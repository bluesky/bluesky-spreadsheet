import pandas

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


class ExcelSpreadsheet:
    def __init__(self, filepath, plan, quiet=False):
        self.filepath = filepath
        self.plan = plan
        self._current_row = 0
        self.quiet = quiet
        self.state = {}

    def reset(self):
        self._current_row = 0
        self.state.clear()

    def __call__(self, start_at=None):
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
