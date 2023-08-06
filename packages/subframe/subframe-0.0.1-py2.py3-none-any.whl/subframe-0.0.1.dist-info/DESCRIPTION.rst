.. vim:filetype=rst

SubFrame
--------

DataFrame-friendly jQuery Plugins for `Jupyter Notebook <http://jupyter.org/>`_:

- `DataTables <https://github.com/DataTables/DataTables/>`_
- `PivotTable.js <https://github.com/nicolaskruchten/pivottable/>`_

Usage
-----

::

  In [1]: import subframe
          subframe.plugins.enable()

  In [2]: import pandas

          d = pandas.DataFrame({
              'x': [1, 1, 1, 2, 3],
              'a': [1, 2, 2, 1, 3],
              'b': [23.534, 234.4, 27654.43, 2534.6, 342]
          })

  In [3]: subframe.DataTable(d)
  Out[3]: ...

  In [4]: subframe.PivotTable(d)
  Out[4]: ...


