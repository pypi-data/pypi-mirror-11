#!/usr/bin/env python

"""
This module contains the :class:`TableSet` class which abstracts an set of
related tables into a single data structure. The most common way of creating a
:class:`TableSet` is using the :meth:`.Table.group_by` method, which is
similar to SQL's ``GROUP BY`` keyword. The resulting set of tables each have
identical columns structure.

:class:`TableSet` functions as a dictionary. Individual tables in the set can
be accessed by using their name as a key. If the table set was created using
:meth:`.Table.group_by` then the names of the tables will be the group factors
found in the original data.

:class:`TableSet` replicates the majority of the features of :class:`.Table`.
When methods such as :meth:`TableSet.select`, :meth:`TableSet.where` or
:meth:`TableSet.order_by` are used, the operation is applied to *each* table
in the set and the result is a new :class:`TableSet` instance made up of
entirely new :class:`.Table` instances.
"""

from collections import Mapping
from copy import copy
from glob import glob
import os

try:
    from collections import OrderedDict
except ImportError: # pragma: no cover
    from ordereddict import OrderedDict

from agate.aggregations import Aggregation
from agate.column_types import TextType, NumberType
from agate.exceptions import ColumnDoesNotExistError
from agate.rows import RowSequence

class TableMethodProxy(object):
    """
    A proxy for :class:`TableSet` methods that converts them to individual
    calls on each :class:`.Table` in the set.
    """
    def __init__(self, tableset, method_name):
        self.tableset = tableset
        self.method_name = method_name

    def __call__(self, *args, **kwargs):
        groups = OrderedDict()

        for name, table in self.tableset._tables.items():
            groups[name] = getattr(table, self.method_name)(*args, **kwargs)

        return TableSet(groups)

class TableSet(Mapping):
    """
    An group of named tables with identical column definitions. Supports
    (almost) all the same operations as :class:`.Table`. When executed on a
    :class:`TableSet`, any operation that would have returned a new
    :class:`.Table` instead returns a new :class:`TableSet`. Any operation
    that would have returned a single value instead returns a dictionary of
    values.

    :param tables: A dictionary of string keys and :class:`Table` values.
    """
    def __init__(self, group):
        self._first_table = list(group.values())[0]
        self._column_types = self._first_table.get_column_types()
        self._column_names = self._first_table.get_column_names()

        for name, table in group.items():
            if table._column_types != self._column_types:
                raise ValueError('Table %i has different column types from the initial table.' % i)

            if table._column_names != self._column_names:
                raise ValueError('Table %i has different column names from the initial table.' % i)

        self._tables = copy(group)

        self.select = TableMethodProxy(self, 'select')
        self.where = TableMethodProxy(self, 'where')
        self.find = TableMethodProxy(self, 'find')
        self.stdev_outliers = TableMethodProxy(self, 'stdev_outliers')
        self.mad_outliers = TableMethodProxy(self, 'mad_outliers')
        self.pearson_correlation = TableMethodProxy(self, 'pearson_correlation')
        self.order_by = TableMethodProxy(self, 'order_by')
        self.limit = TableMethodProxy(self, 'limit')
        self.distinct = TableMethodProxy(self, 'distinct')
        self.inner_join = TableMethodProxy(self, 'inner_join')
        self.left_outer_join = TableMethodProxy(self, 'left_outer_join')
        # self.group_by = TableMethodProxy(self, 'group_by')
        self.compute = TableMethodProxy(self, 'compute')
        self.percent_change = TableMethodProxy(self, 'percent_change')
        self.rank = TableMethodProxy(self, 'rank')
        self.z_scores = TableMethodProxy(self, 'z_scores')

    def __getitem__(self, k):
        return self._tables.__getitem__(k)

    def __iter__(self):
        return self._tables.__iter__()

    def __len__(self):
        return self._tables.__len__()

    @classmethod
    def from_csv(cls, dir_path, column_info, header=True, **kwargs):
        """
        Create a new :class:`TableSet` from a directory of CSVs. This method
        will use csvkit if it is available, otherwise it will use Python's
        builtin csv module.

        ``kwargs`` will be passed through to :meth:`csv.reader`.

        If you are using Python 2 and not using csvkit, this method is not
        unicode-safe.

        :param dir_path: Path to a directory full of CSV files. All CSV files
            in this directory will be loaded.
        :param column_info: See :class:`.Table` constructor.
        :param header: If `True`, the first row of the CSV is assumed to contains
            headers and will be skipped.
        """
        from agate.table import Table

        if not os.path.isdir(dir_path):
            raise IOError('Specified path doesn\'t exist or isn\'t a directory.')

        tables = OrderedDict()

        for path in glob(os.path.join(dir_path, '*.csv')):
            name = os.path.split(path)[1].strip('.csv')
            table = Table.from_csv(path, column_info, header=header, **kwargs)

            tables[name] = table

        return TableSet(tables)

    def to_csv(self, dir_path, **kwargs):
        """
        Write this each table in this set to a separate CSV in a given
        directory. This method will use csvkit if it is available, otherwise
        it will use Python's builtin csv module.

        ``kwargs`` will be passed through to :meth:`csv.writer`.

        If you are using Python 2 and not using csvkit, this method is not
        unicode-safe.

        :param dir_path: Path to the directory to write the CSV files to.
        """
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for name, table in self._tables.items():
            path = os.path.join(dir_path, '%s.csv' % name)

            table.to_csv(path, **kwargs)

    def get_column_types(self):
        """
        Get an ordered list of this :class:`.TableSet`'s column types.

        :returns: A :class:`tuple` of :class:`.Column` instances.
        """
        return self._column_types

    def get_column_names(self):
        """
        Get an ordered list of this :class:`TableSet`'s column names.

        :returns: A :class:`tuple` of strings.
        """
        return self._column_names

    def aggregate(self, aggregations=[]):
        """
        Aggregate data from the tables in this set by performing some
        set of column operations on the groups and coalescing the results into
        a new :class:`.Table`.

        :class:`group` and :class:`count` columns will always be included as at
        the beginning of the output table, before the aggregated columns.

        :code:`aggregations` must be a list of tuples, where each has three
        parts: a :code:`column_name`, a :class:`.Aggregation` instance and a
        :code:`new_column_name`.

        :param aggregations: An list of triples in the format
            :code:`(column_name, aggregation, new_column_name)`.
        :returns: A new :class:`.Table`.
        """
        output = []

        column_types = [TextType(), NumberType()]
        column_names = ['group', 'count']

        for column_name, aggregation, new_column_name in aggregations:
            c = self._first_table.columns[column_name]

            column_types.append(aggregation.get_aggregate_column_type(c))
            column_names.append(new_column_name)

        for name, table in self._tables.items():
            new_row = [name, len(table.rows)]

            for column_name, aggregation, new_column_name in aggregations:
                c = table.columns[column_name]

                new_row.append(c.aggregate(aggregation))

            output.append(tuple(new_row))

        return self._first_table._fork(output, zip(column_names, column_types))
