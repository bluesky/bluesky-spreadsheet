from pathlib import Path

import bluesky.plans
import bluesky.plan_stubs
from ophyd.sim import det, motor
import pandas

from .. import ExcelSpreadsheet


def test_instantiation(tmp_path):
    "Very basic test that does not actually *run* anything"

    def plan(row):
        ...

    filepath = Path(tmp_path, 'test.xlsx')
    pandas.DataFrame({'a': [1, 2]}).to_excel(filepath)
    ExcelSpreadsheet(filepath, plan, [])


def test_usage(tmp_path):

    filepath = Path(tmp_path, 'test.xlsx')
    df = pandas.DataFrame(
        {'position': [1, None, 2, None],
         'number': [1, 2, 1, 2]})
    df.to_excel(filepath)

    def plan(row):
        yield from bluesky.plan_stubs.mv(motor, row['position'])
        yield from bluesky.plans.count([det], int(row['number']))

    spreadsheet = ExcelSpreadsheet(filepath, plan)

    def expected_plan():
        yield from bluesky.plan_stubs.mv(motor, 1.0)
        yield from bluesky.plans.count([det], 1)
        yield from bluesky.plan_stubs.mv(motor, 1.0)
        yield from bluesky.plans.count([det], 2)
        yield from bluesky.plan_stubs.mv(motor, 2.0)
        yield from bluesky.plans.count([det], 1)
        yield from bluesky.plan_stubs.mv(motor, 2.0)
        yield from bluesky.plans.count([det], 2)

    actual_msgs = list(spreadsheet())
    expected_msgs = list(expected_plan())

    # Strip off nondeterministic value.
    for msg in actual_msgs:
        msg.kwargs.pop('group', None)
    for msg in expected_msgs:
        msg.kwargs.pop('group', None)

    assert actual_msgs == expected_msgs
