import pandas

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


class ExcelSpreadsheet:
    def __init__(self, filepath, plan, detectors, quiet=False):
        self.filepath = filepath
        self._current_row = 0
        self.detectors = detectors
        self.quiet = quiet

    def __call__(self, start_at=None):
        if start_at is not None:
            self._current_row = start_at
        while True:
            df = pandas.from_excel(filepath)
            row = df.iloc[self.current_row]
            if not self.quiet:
                print(row)
            yield from self.plan(self.detectors, row)
            self._curent_row += 1
