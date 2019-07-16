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

    def plan(detectors, row):
        yield from bluesky.plan_stubs.mv(motor, row['position'])
        yield from bluesky.plans.count([det], int(row['number']))

    spreadsheet = ExcelSpreadsheet('path/to/spreadsheet.xlsx', plan)

The ``spreadsheet`` object is itself a plan, and can be passed to the RunEngine
for execution:

.. code:: python

   from bluesky import RunEngine

   RE = RunEngine()
   RE(spreadsheet())


The spreadsheet is re-read between each row. Any edits or additionals made (and
saved) to during execution to rows that have not yet been reached will be
respected. If execution is interrupted, the ``spreadsheet`` object keeps track
of where it left off and will resume from the last row that it did not
complete. To resume from a specific row use

.. code:: python

   RE(spreadsheet(start_at=SOME_ROW_NUMBER))

.. important::

   Notice in the example above that the number of exposures ``row['numbers']``
   is explicit converted to an integer as ``int(row['numbers'])``. Excel stores
   all numerical data as floating point, so any values that are actually
   expected to be integers will need to be converted.
