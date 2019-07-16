=====
Usage
=====

The bluesky-speadsheet library provides an object that behaves like any bluesky
plan but obtains its instructions by interpreting an Excel spreadsheet.

To set it up initially, you must provide a standard bluesky plan that knows how
to interpret a row of the spreadsheet.

In the first example, suppose we have a spreadsheet with two columns:

* ``position`` --- desired position of a motor during an exposure
* ``number`` --- number of exposures

This example will generate a :func:`~bluesky.plans.count` for each row in the
spreadsheet.

.. code:: python

    import bluesky.plans
    import bluesky.plan_stubs
    import bluesky_spreadsheet
    from ophyd.sim import det, motor  # simulated hardware for this example

    def plan(detectors, row, state):
        position = row['position']
        number = row['number']
        yield from bluesky.plan_stubs.mv(motor, position)
        yield from bluesky.plans.count([det], number)

    spreadsheet = ExcelSpreadsheet('path/to/spreadsheet.xlsx', plan)

The ``state`` parameter, is a dict that we can use to persist information
across rows. For example, we can implement the rule that if the user leaves a
cell blank, we should use the previous value in that column.

.. code:: python

    def plan(detectors, row, state):
        position = row.get('position', state.get('position'))
        state['position'] = position
        number = int(row.get('number', state.get('number')))
        state['number'] = number
        yield from bluesky.plan_stubs.mv(motor, position)
        yield from bluesky.plans.count([det], number)

    spreadsheet = ExcelSpreadsheet('path/to/spreadsheet.xlsx', plan)

The ``spreadsheet`` object is itself a plan, and can be passed to the RunEngine
for execution:

.. code:: python

   from bluesky import RunEngine
   RE(spreadsheet())

The spreadsheet is re-read between each row. Any edits made (and saved) during
execution will be respected. If execution is interrupted, the ``spreadsheet``
object keeps track of where it left off and will resume from the last row that
it did not complete. To resume from a specific row use

.. code:: python

   from bluesky import RunEngine
   RE(spreadsheet(start_at=SOME_ROW_NUMBER))
