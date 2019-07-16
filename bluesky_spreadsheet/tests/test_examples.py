from pathlib import Path

import pandas

from .. import ExcelSpreadsheet


def test_instantiation(tmp_path):
    "Very basic test that does not actually *run* anything"

    def plan(detectors, row):
        ...

    filepath = Path(tmp_path, 'test.xlsx')
    pandas.DataFrame({'a': [1, 2]}).to_excel(filepath)
    ExcelSpreadsheet(filepath, plan, [])
