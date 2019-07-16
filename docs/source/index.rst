.. Packaging Scientific Python documentation master file, created by
   sphinx-quickstart on Thu Jun 28 12:35:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bluesky Spreadsheet Documentation
=================================

This is an experimental library for using an Excel spreadsheet to enter
parameters and metadata for executing data acquisition with bluesky.

Using Excel for data and metadata entry has limitations, and given enough
resources a proper database and GUI or web application is likely a better
solution, but an Excel spreadsheet has proved to be a useful stepping stone for
quickly prototyping a tool that makes users comfortable.

Design requirements:

* The user can add rows during execution.
* The user can modify rows that haven't been executed yet.
* If execution is interrupted, the plan will resume from the last row that it
  has not yet completed.
* The plan can started from a specific row.
* The meaning of the columns in the spreadsheet is open-eneded and can be tuned
  to specific use cases. For example, thespreadsheet can be used to configure
  the hardware before an acquisition, specify the parameters of the acquisition
  itself, and configure how the data is visualized, processed, and/or exported.
* If a cell is blank, the value from the previous cell in that column is used.

.. toctree::
   :maxdepth: 2

   installation
   usage
   reference
   release-history
