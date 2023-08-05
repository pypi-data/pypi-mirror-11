"""Tables as ordered dictionaries of Numpy arrays."""

import collections
import collections.abc
import functools
import itertools
import operator

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import IPython


class Table(collections.abc.Mapping):
    """A sequence of labeled columns.

    >>> letters = ['a', 'b', 'c', 'z']
    >>> counts = [9, 3, 3, 1]
    >>> points = [1, 2, 2, 10]
    >>> t = Table([('letter', letters), ('count', counts), ('points', points)])
    >>> print(t)
    letter | count | points
    a      | 9     | 1
    b      | 3     | 2
    c      | 3     | 2
    z      | 1     | 10
    """

    def __init__(self, columns=None):
        """Create an table.

        columns -- a dictionary of sequence keyed by column label OR
                   a sequence of (label, sequence) pairs,
                   with all columns of equal length
        """
        self._columns = collections.OrderedDict()
        self._formats = dict()
        if not columns:
            columns = []
        if hasattr(columns, 'items'):
            columns = columns.items()
        for label, column in columns:
            self[label] = column

    def __getitem__(self, label):
        return self._columns[label]

    def __setitem__(self, label, values):
        if not isinstance(values, np.ndarray):
            values = array(list(values))
        if hasattr(self, '_num_rows') & self.num_rows > 0:
            assert len(values) == self.num_rows, 'column length mismatch'
        else:
            self._num_rows = len(values)
        self._columns[label] = values

    def __delitem__(self, label):
        del self._columns[label]
        if label in self._formats:
            del self._formats[label]

    def __len__(self):
        return len(self._columns)

    def __iter__(self):
        return iter(self.column_labels())

    def __getattr__(self, attr):
        """Return a method that applies to all columns or a table of attributes."""
        if self.columns() and all(hasattr(c, attr) for c in self.columns()):
            attrs = [getattr(c, attr) for c in self.columns()]
            if all(callable(attr) for attr in attrs):
                @functools.wraps(attrs[0])
                def method(*args, **vargs):
                    """Create a table from the results of calling attrs."""
                    columns = [attr(*args, **vargs) for attr in attrs]
                    return self.with_columns(columns)
                return method
            else:
                return self.with_columns([[attr] for attr in attrs])
        else:
            msg = "'{0}' object has no attribute '{1}'".format(type(self).__name__, attr)
            raise AttributeError(msg)

    @property
    def num_rows(self):
        """Number of rows."""
        if hasattr(self, '_num_rows'):
            return self._num_rows
        else:
            return 0

    def rows(self):
        """Return a view of all rows."""
        return self.Rows(self)

    def column_labels(self):
        """Return a tuple of column labels."""
        return tuple(self._columns.keys())

    def columns(self):
        return tuple(self._columns.values())

    def column_index(self, column_label):
        """Return the index of a column."""
        return self.column_labels().index(column_label)

    def apply(self, fn, column_label):
        """Apply a function to each element of a column."""
        return array([fn(v) for v in self[column_label]])

    ##########
    # Modify #
    ##########

    def set_format(self, column_label, formatter):
        """Set the format function for a column."""
        assert callable(formatter), 'formatter must be a function'
        self._formats[column_label] = formatter
        return self

    def move_to_start(self, column_label):
        """Move a column to the first in order."""
        self._columns.move_to_end(column_label, last=False)
        return self

    def move_to_end(self, column_label):
        """Move a column to the last in order."""
        self._columns.move_to_end(column_label)
        return self

    def append(self, row_or_table):
        """Append a row or the rows of a table with identical column names."""
        if not row_or_table:
            return
        if isinstance(row_or_table, Table):
            table = row_or_table
            assert table.column_labels() == self.column_labels()
            for row in list(row_or_table.rows()):
                self.append(row)
        else:
            row = row_or_table
            for i, column in enumerate(self._columns):
                self._columns[column] = np.append(self[column], row[i])
        self._num_rows = self.num_rows + 1
        return self

    def relabel(self, column_label, new_label):
        """Change the label of a column."""
        assert column_label in self._columns
        update = lambda s: new_label if s == column_label else s
        self._columns = collections.OrderedDict((update(s), c) for s, c in self._columns.items())
        if column_label in self._formats:
            formatter = self._formats.pop(column_label)
            self._formats[new_label] = formatter
        return self

    ##########
    # Create #
    ##########

    @classmethod
    def from_rows(cls, rows, column_labels=None):
        """Create a table from a sequence of fixed-length rows."""
        return Table.from_columns(list(zip(*rows)), column_labels)

    @classmethod
    def from_columns(cls, columns, column_labels=None):
        """Create a table from a sequence of fixed-length columns."""
        assert columns and len(columns[0]), 'Tables cannot have empty columns'
        if not column_labels:
            column_labels = ['column_' + str(i) for i in range(len(columns))]
        assert len(column_labels) == len(columns), "columns do not match column_labels"
        return cls(list(zip(column_labels, columns)))

    @staticmethod
    def from_matrix(numpy_matrix, columns_labels=None):
        """Creates table from a 2-d array (matrix)."""
        return Table.from_columns(numpy_matrix.tolist(), columns_labels)

    @classmethod
    def from_labels(cls, column_labels):
        """Create and empty table of labeled columns that can be filled by row with append."""
        return cls([(label, []) for label in column_labels])

    @classmethod
    def read_table(cls, filepath_or_buffer, *args, **vargs):
        """Read a table from a file or web address.

        filepath_or_buffer -- string or file handle / StringIO; The string
                              could be a URL. Valid URL schemes include http,
                              ftp, s3, and file.
        """
        if filepath_or_buffer.endswith('.csv') and 'sep' not in vargs:
            vargs['sep'] = ','
        df = pd.read_table(filepath_or_buffer, *args, **vargs)
        return Table([(label, df[label].values) for label in df])

    def with_rows(self, rows):
        """Create a table from a sequence of rows, copying column labels."""
        table = self.from_rows(rows, self.column_labels())
        table._formats = self._formats.copy()
        return table

    def with_columns(self, columns):
        """Create a table from a sequence of columns, copying column labels."""
        table = Table()
        for label, column in zip(self.column_labels(), columns):
            self._add_column_and_format(table, label, column)
        return table

    def _add_column_and_format(self, table, label, column):
        """Add a column to table, copying the formatter from self."""
        table[label] = column
        if label in self._formats:
            table.set_format(label, self._formats[label])

    #############
    # Transform #
    #############

    def copy(self):
        """Return a copy of a Table."""
        table = Table()
        for label in self.column_labels():
            self._add_column_and_format(table, label, np.copy(self[label]))
        return table

    def select(self, column_label_or_labels):
        """Return a Table of selected column or sequence of columns by label."""
        if isinstance(column_label_or_labels, str):
            column_labels = [column_label_or_labels]
        else:
            column_labels = column_label_or_labels
        table = Table()
        for label in column_labels:
            self._add_column_and_format(table, label, np.copy(self[label]))
        return table

    def drop(self, column_label_or_labels):
        """Return a Table of selected column or sequence of columns by label."""
        if isinstance(column_label_or_labels, str):
            column_labels = [column_label_or_labels]
        else:
            column_labels = column_label_or_labels
        table = Table()
        for label in self.column_labels() :
            if label not in column_labels:
                self._add_column_and_format(table, label, np.copy(self[label]))
        return table

    def take(self, row_numbers):
        """Return a Table of a sequence of rows taken by number."""
        columns = [np.take(column, row_numbers) for column in self.columns()]
        return self.with_columns(columns)

    def where(self, column_or_label, value=None):
        """Return a Table of rows for which the column is value or a non-zero value."""
        column = self._get_column(column_or_label)
        if value is not None:
            column = column == value
        return self.take(np.nonzero(column)[0])

    def sort(self, column_or_label, decreasing=False, distinct=False):
        """Return a Table of sorted rows by the values in a column."""
        column = self._get_column(column_or_label)
        if distinct:
            _, row_numbers = np.unique(column, return_index=True)
        else:
            # TODO argsort on multi-dimentsional array creates problems
            row_numbers = np.argsort(column)
        assert (row_numbers < self.num_rows).all(), row_numbers
        if decreasing:
            row_numbers = array(row_numbers[::-1])
        return self.take(row_numbers)

    def group(self, column_or_label, collect=None):
        """Group rows by unique values in column_label, aggregating values.

        collect -- an optional function applied to the values for each group.

        The grouped column will appear first in the result.
        """
        self = self.sort(column_or_label)

        column = self._get_column(column_or_label)
        if column_or_label in self.column_labels():
            column_label = column_or_label
            del self[column_label]
        else:
            column_label = self._unused_label('group')

        if collect:
            collect = _zero_on_type_error(collect)
        else:
            collect = lambda x: x

        values, starts = np.unique(column, return_index=True)
        ends = np.append(starts[1:], self.num_rows)
        columns = self.columns()

        rows = []
        for value, start, end in zip(values, starts, ends):
            row = []
            for i, column in enumerate(columns):
                taken = np.take(column, range(start, end))
                cell = collect(taken)
                if cell is None: # on invalid collection, group the entries and try to reduce
                    cell = np.unique(taken)
                    if len(cell) == 1: cell = cell[0]
                row.append(cell)
            rows.append(row)

        labels = []
        for i, label in enumerate(self.column_labels()):
            if not collect.__name__.startswith('<'):
                labels.append(label + ' ' + collect.__name__)
            else:
                labels.append(label)

        table = self.from_rows(rows, labels)
        assert column_label == self._unused_label(column_label)
        table[column_label] = values
        table.move_to_start(column_label)
        return table

    def dist(self, pivot_label, value_label, remove=False):
        """
        Distribute the values in a column over new columns defined by items in a pivot column"
        """
        dtable = self.copy()
        pivots = list(np.unique(dtable[pivot_label]))
        pivot_col_labels = [dtable._unused_label(label + "-" + value_label) for label in pivots]
        dtable.move_to_end(pivot_label)
        dtable.move_to_end(value_label)
        for pivot,label in zip(pivots,pivot_col_labels):
            dtable[label] = np.where(dtable[pivot_label]==pivot,dtable[value_label],None)
        if remove:
            del dtable[pivot_label]
            del dtable[value_label]
        return dtable

    def pivot(self, pivot_label, group_label, collect=None, init=0):
        """
        Pivot on a column forming new columns of unique values,
        grouping a column according to the unique entries in all
        other columns.

        The non-pivot, non-group items form the first columns of the result
        and our sorted, followed by the grouped entries in the pivot columns.
        """
        if collect:
            collect = _zero_on_type_error(collect)
        else:
            collect = lambda x: x

        sorted = self.sort(pivot_label)
        sorted.move_to_end(pivot_label)
        sorted.move_to_end(group_label)
        fixed_column_labels = list(sorted.column_labels()[0:-2])
        for column_label in reversed(fixed_column_labels):
            sorted = sorted.sort(column_label)
        pivots = list(np.unique(sorted[pivot_label]))
        pivot_col_labels = [sorted._unused_label(label + "-" + group_label) for label in pivots]
        labels = fixed_column_labels + pivot_col_labels
        fixed_rows, starts = sorted._starts(fixed_column_labels)
        ends = np.append(starts[1:], self.num_rows)
        rows = []
        for fixed_row, start, end in zip(fixed_rows, starts, ends):
            pivot_row = _distribute(pivots, sorted[pivot_label][start:end],sorted[group_label][start:end])
            pivot_row = [collect(group) if len(group) > 1 else (group[0] if len(group)==1 else init) for group in pivot_row]
            rows.append(fixed_row + pivot_row)
        return Table.from_rows(rows, labels)

    def stack(self, key, column_labels=None):
        """
        Takes k original columns and returns two columns, with col. 1 of
        all column names and col. 2 of all associated data.
        """
        rows, column_labels = [], column_labels or self.column_labels()
        for row in self.rows():
            [rows.append((getattr(row, key), k, v)) for k, v in row._asdict().items()
             if k != key and k in column_labels]
        return Table.from_rows(rows, [key, 'column', 'value'])

    def join(self, column_label, other, other_label=None):
        """Generate a table with the columns of self and other, containing rows
        for all values of a column that appear in both tables. If a join value
        appears more than once, only its first row will be used.

        If the result is empty, return None.
        """
        if self.num_rows == 0 or other.num_rows == 0:
            return None
        if not other_label:
            other_label = column_label

        self_rows = self.index_by(column_label)
        other_rows = other.index_by(other_label)

        # build set of rows from rows that have values in both tables
        joined_rows = []
        for label, rows in self_rows.items():
            if label in other_rows:
                row, other_row = rows[0], other_rows[label][0]
                joined_rows.append(row + other_row)

        if not joined_rows:
            return None

        labels = list(self.column_labels())
        labels += [self._unused_label(s) for s in other.column_labels()]
        joined = Table.from_rows(joined_rows, labels)
        del joined[self._unused_label(other_label)] # Remove redundant column
        return joined.move_to_start(column_label).sort(column_label)

    def currency(self, column_label_or_labels, symbol):
        if isinstance(column_label_or_labels, str):
            column_labels = [column_label_or_labels]
        else: column_labels = column_label_or_labels
        table = Table()
        for label in self.column_labels():
            if label in column_labels:
                assert isinstance(self[label][0],str), "Columns must contain strings"
                table[label] = [float(x.strip(symbol)) for x in self[label]]
                table.set_format(label, lambda x: symbol+"{0:.2f}".format(x))
            else:
                self._add_column_and_format(table, label, np.copy(self[label]))
        return table

    def stats(self, ops=(min, max, np.median, sum)):
        """Compute statistics for each column and place them in a table."""
        names = [op.__name__ for op in ops]
        ops = [_zero_on_type_error(op) for op in ops]
        rows = [[op(column) for column in self.columns()] for op in ops]
        table = self.with_rows(rows)
        stats = self._unused_label('statistic')
        table[stats] = names
        table.move_to_start(stats)
        return table

    def _unused_label(self, label):
        """Generate an unused label."""
        original = label
        existing = self.column_labels()
        i = 2
        while label in existing:
            label = '{}_{}'.format(original, i)
            i += 1
        return label

    def _get_column(self, column_or_label):
        """Convert label to column and check column length."""
        c = column_or_label
        if isinstance(c, collections.Hashable) and  c in self.column_labels():
            return self[c]
        else:
            assert len(c) == self.num_rows, 'column length mismatch'
            return c

    def _starts(self, column_labels):
        """Return a sequence of start points for unique combinations of  sorted rows"""
        val = [self[c][0] for c in column_labels]
        starts = [0]
        values = [val]
        for i in range(1,self.num_rows):
            ival = [self[c][i] for c in column_labels ]
            if ival != val:
                starts.append(i)
                values.append(ival)
                val = ival
        return values, starts

    ##################
    # Export/Display #
    ##################

    def __repr__(self):
        return '<{0}({1} rows): | {3} |>'.format(
            type(self).__name__,
            len(self),self.num_rows,
            " | ".join(map(str, self.column_labels())))

    def __str__(self):
        return self.as_text(self.max_str_rows)

    def _repr_html_(self):
        return self.as_html(self.max_str_rows)

    def show(self, max_rows=0):
        return IPython.display.HTML(self.as_html(max_rows))

    min_val_width = 4
    max_val_width = 60
    max_str_rows = 10

    def as_text(self, max_rows=0, sep=" | "):
        """Format table as text."""
        if not max_rows or max_rows > self.num_rows:
            max_rows = self.num_rows
        omitted = max(0, self.num_rows - max_rows)
        labels = self._columns.keys()
        fmts = [self._formats.get(k, self.format_column(k, v[:max_rows])) for
            k, v in self._columns.items()]
        rows = [[fmt(label) for fmt, label in zip(fmts, labels)]]
        for row in itertools.islice(self.rows(), max_rows):
            rows.append([f(v) for v, f in zip(row, fmts)])
        lines = [sep.join(row) for row in rows]
        if omitted:
            lines.append('... ({} rows omitted)'.format(omitted))
        return '\n'.join([line.rstrip() for line in lines])

    def as_html(self, max_rows=0):
        """Format table as HTML."""
        if not max_rows or max_rows > self.num_rows:
            max_rows = self.num_rows
        omitted = max(0, self.num_rows - max_rows)
        lines =  []
        lines.append((0, '<table border="1" class="dataframe">'))
        lines.append((1, '<thead>'))
        lines.append((2, '<tr>'))
        labels = self.column_labels()
        lines.append((3, ' '.join('<th>' + label + '</th>' for label in labels)))
        lines.append((2, '</tr>'))
        lines.append((1, '</thead>'))
        lines.append((1, '<tbody>'))
        fmts = [self._formats.get(k, self.format_column(k, v[:max_rows])) for
            k, v in self._columns.items()]
        for row in itertools.islice(self.rows(), max_rows):
            lines.append((2, '<tr>'))
            lines.append((3, ' '.join('<td>' + fmt(v) + '</td>' for
                v, fmt in zip(row, fmts))))
            lines.append((2, '</tr>'))
            lines.append((1, '</tbody>'))
        lines.append((0, '</table>'))
        if omitted:
            lines.append((0, '<p>... ({} rows omitted)</p'.format(omitted)))
        return '\n'.join(4 * indent * ' ' + text for indent, text in lines)

    @classmethod
    def format_column(cls, label, column):
        """Return a formatting function that pads values."""
        val_width = 0 if len(column) == 0 else max(len(str(v)) for v in column)
        val_width = min(val_width, cls.max_val_width)
        width = max(val_width, len(str(label)), cls.min_val_width)
        def pad(value):
            try:
                assert not isinstance(value, (bool, np.bool_))
                raw = '{:G}'.format(value)
            except (ValueError, TypeError, AssertionError):
                raw = str(value)
            if len(raw) > width:
                prefix = raw[:width-4] + ' ...'
            else:
                prefix = raw
            return prefix.ljust(width)
        return pad

    def matrix(self):
        """Return a 2-D array with the contents of the table."""
        return np.matrix(list(self._columns.values()))

    def index_by(self, column_or_label):
        """
        Return a dict from the values in a column to the rows containing that value.
        """
        column = self._get_column(column_or_label)
        index = {}
        for key, row in zip(column, self.rows()):
            index.setdefault(key, []).append(row)
        return index

    #############
    # Visualize #
    #############

    def plot(self, column_for_xticks=None, overlay=False, **vargs):
        """Plot contents as lines."""
        xticks, labels = self._split(column_for_xticks)
        def draw(axis, label, color):
            axis.plot(self[label], color=color, **vargs)
        def annotate(axis, ticks):
            axis.set_xticklabels(ticks, rotation='vertical')
        self._visualize(labels, xticks, overlay, draw, annotate)

    def barh(self, column_for_categories, overlay=False, **vargs):
        """Plot contents as a horizontal bar chart."""
        yticks, labels = self._split(column_for_categories)
        index = np.arange(self.num_rows)
        margin = 0.1
        width = 1 - 2 * margin
        if overlay:
            width /= len(labels)
        def draw(axis, label, color):
            if overlay:
                ypos = index + margin + (1-2*margin)*labels.index(label)/len(labels)
            else:
                ypos = index
            axis.barh(ypos, self[label], width, alpha=0.8, color=color, **vargs)
        def annotate(axis, ticks):
            axis.set_yticks(index+0.5) # Center labels on bars
            axis.set_yticklabels(ticks, stretch='ultra-condensed')
        height = max(4, len(index)/2)
        self._visualize(labels, yticks, overlay, draw, annotate, height)

    def _visualize(self, labels, ticks, overlay, draw, annotate, height=4):
        """Generic visualization using overlay or not."""
        n = len(labels)
        colors = list(itertools.islice(itertools.cycle(('b', 'y', 'g', 'r')), n))
        if overlay:
            _, axis = plt.subplots(figsize=(6, height))
            for label, color in zip(labels, colors):
                draw(axis, label, color)
            if ticks is not None:
                annotate(axis, ticks)
            axis.legend(labels, bbox_to_anchor=(1.5, 1.0))
        else:
            _, axes = plt.subplots(n, 1, figsize=(6, height * n))
            if not isinstance(axes, collections.Iterable):
                axes=[axes]
            for axis, label, color in zip(axes, labels, colors):
                draw(axis, label, color)
                axis.set_xlabel(label, fontsize=16)
                if ticks is not None:
                    annotate(axis, ticks)

    def _split(self, column_or_label):
        """Return the specified column and labels of other columns."""
        labels = list(self.column_labels())
        if column_or_label is None:
            return None, labels
        if column_or_label in labels:
            labels.remove(column_or_label)
        column = self._get_column(column_or_label)
        return column, labels

    def pivot_hist(self, pivot_column_label, value_column_label, overlay=False, **vargs):
        """Draw histograms of each category in a column."""
        pvt_labels = np.unique(self[pivot_column_label])
        pvt_columns = [self[value_column_label][np.where(self[pivot_column_label] == pivot)] for pivot in pvt_labels]
        n = len(pvt_labels)
        colors = list(itertools.islice(itertools.cycle(('b', 'g', 'r')), n))
        if overlay:
            plt.figure(figsize=(6, 4))
            vals, bins, patches = plt.hist(pvt_columns, color=colors, **vargs)
            plt.legend(pvt_labels)
        else:
            _, axes = plt.subplots(n, 1, figsize=(6, 4 * n))
            vals = []
            bins = None
            for axis, label, column, color in zip(axes, pvt_labels, pvt_columns, colors):
                if isinstance(bins, np.ndarray):
                    avals, abins, patches = axis.hist(column, color=color, bins=bins, **vargs)
                else:
                    avals, abins, patches = axis.hist(column, color=color, **vargs)
                axis.set_xlabel(label, fontsize=16)
                vals.append(avals)
                if not isinstance(bins, np.ndarray): bins = abins
                else: assert bins.all() == abins.all(), "Inconsistent bins in hist"
        t = Table()
        t['start'] = bins[0:-1]
        t['end'] = bins[1:]
        for label, column in zip(pvt_labels,vals):
            t[label] = column
        return t

    def hist(self, overlay=False, **vargs):
        """Draw histograms of all columns."""
        n = len(self)
        colors = list(itertools.islice(itertools.cycle(('b', 'g', 'r')), n))
        if overlay:
            plt.figure(figsize=(6, 4))
            plt.hist(self.columns(), color=colors, **vargs)
            plt.legend(self.column_labels())
        else:
            _, axes = plt.subplots(n, 1, figsize=(6, 4 * n))
            for axis, label, color in zip(axes, self.column_labels(), colors):
                axis.hist(self[label], color=color, **vargs)
                axis.set_xlabel(label, fontsize=16)

    ###########
    # Support #
    ###########

    class Rows(collections.abc.Sequence):
        """An iterable view over the rows in a table."""
        def __init__(self, table):
            self._table = table
            self._labels = None

        def __getitem__(self, i):
            if isinstance(i, slice):
                return [self[j] for j in range(*i.indices(len(self)))]
            labels = tuple(self._table.column_labels())
            if labels != self._labels:
                self._labels = labels
                self._row = collections.namedtuple('Row', labels, rename=True)
            return self._row(*[c[i] for c in self._table._columns.values()])

        def __len__(self):
            return self._table.num_rows

        def __repr__(self):
            return '{0}({1})'.format(type(self).__name__, repr(self._table))


def array(*args, **vargs):
    """Create an array. String arrays are endowed with string methods."""
    a = np.array(*args, **vargs)
    if a.dtype.char in ('S', 'U'):
        return a.view(np.chararray)
    else:
        return a


def _zero_on_type_error(column_fn):
    """Wrap a function on an np.ndarray to return 0 on a type error."""
    @functools.wraps(column_fn)
    def wrapped(column):
        try:
            return column_fn(column)
        except TypeError:
            if isinstance(column, np.ndarray):
                return column.dtype.type() # A typed zero value
            else:
                raise
    return wrapped

def _distribute(full_labels, labels, values):
    """Distribute values to their labels position in full_labels."""
    row = [[] for x in full_labels]
    for label, value in zip(labels,values):
        i = full_labels.index(label)
        row[i].append(value)
    return row

