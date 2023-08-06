from functools import reduce
import itertools
import warnings


class Iterable:

    def __init__(self, iterable):
        iter(iterable)
        self.__iterable = list(iterable)

    def __iter__(self):
        return iter(self.__iterable)

    def __len__(self):
        return len(list(self.__iterable))

    # built-in equivalent data structures
    def to_frozenset(self):
        """ Equivalent to the built-in type **frozenset(** *iterable* **)**

        :return: frozenset

        >>> numbers = Iterable([10, 7, 28, 7, 19, 19, 70])
        >>> numbers
        <pyiterable.iterable.Iterable object at 0x017BA610>
        >>> numbers.to_frozenset()
        frozenset({10, 19, 28, 70, 7})
        """
        return frozenset(self.__iterable)

    def to_list(self):
        """ Equivalent to the built-in function **list(** *iterable* **)**

        :return: list

        >>> grades = Iterable([('Alice', 94), ('Bob', 65), ('Charlie', 79), ('Daniel', 70)])
        >>> grades
        <pyiterable.iterable.Iterable object at 0x017BACB0>
        >>> grades.to_list()
        [('Alice', 94), ('Bob', 65), ('Charlie', 79), ('Daniel', 70)]
        """
        return list(self.__iterable)

    def to_set(self):
        """ Equivalent to the built-in function **set(** *iterable* **)**

        :return: set

        >>> numbers = Iterable([10, 7, 28, 7, 19, 19, 70])
        >>> numbers
        <pyiterable.iterable.Iterable object at 0x017BA610>
        >>> numbers.to_set()
        {10, 19, 28, 70, 7}
        """
        return set(self.__iterable)

    def to_tuple(self):
        """ Equivalent to the built-in function **tuple(** *iterable* **)**

        :return: tuple

        >>> numbers = Iterable([10, 7, 28, 7, 19, 19, 70])
        >>> numbers
        <pyiterable.iterable.Iterable object at 0x0130FE70>
        >>> numbers.to_tuple()
        (10, 7, 28, 7, 19, 19, 70)
        """
        return tuple(self.__iterable)

    # built-in equivalent transformations
    def all(self):
        """ Equivalent to the built-in function **all(** *iterable* **)**

        :return: True if all elements in *self* are True, else False

        >>> Iterable([True, False, True]).all()
        False
        >>> Iterable([True, True, True, True]).all()
        True
        """
        return all(self.__iterable)

    def any(self):
        """ Equivalent to the built-in function **any(** *iterable* **)**

        :return: True if any element in *self* is True, else False

        >>> Iterable([True, False, True]).any()
        True
        >>> Iterable([False, False, False, False]).any()
        False
        """
        return any(self.__iterable)

    def enumerate(self, start=0):
        """ Equivalent to the built-in function **enumerate(** *sequence, start=0* **)**

        :param start: integer value to start from
        :return: **(index + start, value)**, where **sequence[index] == value**

        >>> grades = Iterable(['a', 'b', 'c', 'd', 'f'])
        >>> grades.enumerate().to_list()
        [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (5, 'f')]
        >>> grades.enumerate(start=5).to_list()
        [(5, 'a'), (6, 'b'), (7, 'c'), (8, 'd'), (9, 'f')]
        """
        return Iterable(enumerate(self.__iterable, start))

    def filter(self, function):
        """ Equivalent to the built-in function **filter(** *function, iterable* **)**

        :param function: function that returns **False** for items to exclude
        :return: *Iterable* object that only contains items filtered by *function*

        >>> grades = Iterable(['a', 'b', 'c', 'd', 'f'])
        >>> grades.enumerate().filter(lambda i_x: i_x[0] < 3).to_list()
        [(0, 'a'), (1, 'b'), (2, 'c')]
        """
        return Iterable(filter(function, self.__iterable))

    def len(self):
        """ Equivalent to the built-in function **len(** *s* **)**

        :return: number of items in *self*

        >>> grades = Iterable(['a', 'b', 'c', 'd', 'f'])
        >>> grades.len()
        5
        """
        return self.__len__()

    def map(self, function):
        """ Equivalent to the built-in function **map(** *function, iterable* **)**

        :param function: function applied to every item in *self*
        :return: *Iterable* of results

        >>> numbers = Iterable([1, 3, 10, 4, 8])
        >>> numbers.map(lambda x: x * 2).to_list()
        [2, 6, 20, 8, 16]
        """
        return Iterable(map(function, self.__iterable))

    def max(self, **kwargs):
        """ Equivalent to the built-in function **max(** *iterable, \*[, key, default]* **)**

        :param key: keyword-only; function that returns the value to compare
        :param default: keyword-only; value to return if *self* is empty. Only available in Python 3.4 or later
        :return: largest item in *self*

        >>> grades = Iterable([('Charlie', 79), ('Alice', 94), ('Bob', 65)])
        >>> grades.max(key=lambda x: x[1])
        ('Alice', 94)
        """
        return max(self.__iterable, **kwargs)

    def min(self, **kwargs):
        """ Equivalent to the built-in function **min(** *iterable, \*[, key, default]* **)**

        :param key: keyword-only; function that returns the value to compare
        :param default: keyword-only; value to return if *self* is empty. Only available in Python 3.4 or later
        :return: smallest item in *self*

        >>> grades = Iterable([('Charlie', 79), ('Alice', 94), ('Bob', 65)])
        >>> grades.min(key=lambda x: x[1])
        ('Bob', 65)
        """
        return min(self.__iterable, **kwargs)

    def reversed(self):
        """ Equivalent to the built-in function **reversed(** *seq* **)**

        :return: *self* in the reversed order

        >>> names = Iterable(['Bob', 'Alice', 'Daniel', 'Charlie'])
        >>> names.reversed().to_list()
        ['Charlie', 'Daniel', 'Alice', 'Bob']
        """
        return Iterable(reversed(self.__iterable))

    def sorted(self, **kwargs):
        """ Equivalent to the built-in function **sorted(** *iterable[, cmp[, key[, reverse]]]* **)**

        :param cmp: keyword-only; custom comparison function. Only available in Python 2.x
        :param key: keyword-only; function that returns the value to compare
        :param reverse: keyword-only; boolean; if True, *self* is sorted with the largest value first
        :return: a sorted *Iterable*

        >>> grades = Iterable([('Charlie', 79), ('Alice', 94), ('Bob', 65)])
        >>> grades.sorted().to_list()
        [('Alice', 94), ('Bob', 65), ('Charlie', 79)]
        >>> grades.sorted(key=lambda x: x[1]).to_list()
        [('Bob', 65), ('Charlie', 79), ('Alice', 94)]
        >>> grades.sorted(key=lambda x: x[1], reverse=True).to_list()
        [('Alice', 94), ('Charlie', 79), ('Bob', 65)]
        """
        return Iterable(sorted(self.__iterable, **kwargs))

    def sum(self, start=0):
        """ Equivalent to the built-in function **sum(** *iterable[, start]* **)**

        :param start: starting value; default is 0
        :return: sum of all values in *Iterable*

        >>> numbers = Iterable([1, 3, 10, 4, 8])
        >>> numbers.sum()
        26
        >>> numbers.sum(10)
        36
        """
        return sum(self.__iterable, start)

    def zip(self, *args):
        """ Equivalent to the built-in function **zip(** *[iterable, ...]* **)**

        :param args: any number of iterable objects
        :return: list of tuples; i-th tuple contains all elements from each i-th element in *self* and *\*args*

        >>> left = Iterable(['Alice', 'Bob', 'Charlie', 'Daniel'])
        >>> left.zip([94, 65, 79, 70]).to_list()
        [('Alice', 94), ('Bob', 65), ('Charlie', 79), ('Daniel', 70)]
        """
        return Iterable(zip(self.__iterable, *args))

    # functools (Python 3) equivalent transformations
    def reduce(self, function, initializer=None):
        """ Equivalent to:

        * **Python 2.x:** the built-in function **reduce(** *function, iterable[, initializer]* **)**
        * **Python 3.x:** **reduce(** *function, iterable[, initializer]* **)** in *functools*

        Repeatedly applies *function* to sequence until one value is left

        :param function: function that takes two values and returns a single value
        :param initializer: initial value combined with the first value in *self*
        :return: single value

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.reduce(lambda a, b: a + b)
        17
        >>> values.reduce(lambda a, b: a + b, 10)
        27
        """
        if initializer is None:
            return reduce(function, self.__iterable)
        else:
            return reduce(function, self.__iterable, initializer)

    # custom transformations / functions
    def contains(self, value):
        """ Equivalent to calling **value in** *iterable*

        :param value: value to search for inside *iterable*
        :return: *True* if value exists inside *iterable*, otherwise false

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.contains(2)
        True
        >>> values.contains(4)
        False
        """

        return value in self.__iterable

    def is_empty(self):
        """ Equivalent to calling **len( list(** *iterable* **) ) == 0**

        :return: *True* if *iterable* does not contain any elements; otherwise *False*

        >>> Iterable([1, 2, 5, 9]).is_empty()
        False
        >>> Iterable([]).is_empty()
        True
        """
        return len(list(self.__iterable)) == 0

    def mapmany(self, function):
        """ Equivalent to calling **itertools.chain.from_iterable( map(** *function, iterable* **) )**

        :param function: function to be applied to each input; outputs an iterable
        :return: *Iterable* comprised of every element returned by **function**

        >>> values = Iterable([1, 2, 5, 9])
        >>> func = lambda x: [x, x]
        >>> values.map(func).to_list()
        [[1, 1], [2, 2], [5, 5], [9, 9]]
        >>> values.mapmany(func).to_list()
        [1, 1, 2, 2, 5, 5, 9, 9]
        """
        return Iterable(itertools.chain.from_iterable(map(function, self.__iterable)))

    def single(self, filter_by=None, default=None):
        """ Equivalent to calling **first()**, except it raises *ValueError* if *iterable* contains more than one element

        :param filter_by: keyword-only; function used to filter unwanted values
        :param default: keyword-only value to return if *self* is empty after filtered by *filter_by*
        :return: value of *self* filtered by *filter_by*

        :raises ValueError: *iterable* contains more than one element after being filtered by *filter_by*

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.single()
        ValueError: iterable [1, 2, 5, 9] contains more than one element
        >>> values.single(filter_by=lambda x: x > 1)
        ValueError: iterable [2, 5, 9] contains more than one element
        >>> values.single(filter_by=lambda x: x > 5)
        9
        >>> values.single(filter_by=lambda x: x > 10) # Returns None
        >>> values.single(filter_by=lambda x: x > 10, default=0)
        0
        """
        if filter_by is None:
            filtered_self = self
        else:
            filtered_self = self.filter(filter_by)

        if filtered_self.len() > 1:
            raise ValueError("iterable {} contains more than one element".format(filtered_self.__iterable))

        return filtered_self.first(default=default)


    # List-like transformations / functions
    def concat(self, iterable):
        """ Equivalent to calling **list(** *left* **) + list(** *right* **)**

        :param iterable: iterable to concat with *self*
        :return: New *Iterable* containing the elements from *self* and *iterable*

        >>> left = [2, 10, 2, 2, 5, 9, 10]
        >>> right = [13, -5, 1982, -10, 2384, 1982, 98]
        >>> Iterable(left).concat(right).to_list()
        [2, 10, 2, 2, 5, 9, 10, 13, -5, 1982, -10, 2384, 1982, 98]
        """
        return Iterable(list(self.__iterable) + list(iterable))

    def first(self, filter_by=None, default=None, function=None):
        """ Equivalent to calling **next( iter( filter(** *filter_by, iterable* **) )** *, default* **)**

        :param filter_by: keyword-only; function used to filter unwanted values
        :param default: keyword-only; value to return if *self* is empty after filtered by *filter_by*
        :param function: deprecated; use *filter_by*
        :return: first value of *self* filtered by *filter_by*

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.first()
        1
        >>> values.first(filter_by=lambda x: x > 5)
        9
        >>> values.first(filter_by=lambda x: x > 10) # Returns None
        >>> values.first(filter_by=lambda x: x > 10, default=0)
        0
        """
        if function is not None:
            warnings.warn(
                "'function' is deprecated; use 'filter_by' instead",
                category=DeprecationWarning
            )
            if filter_by is not None:
                raise ValueError("both 'filter_by' and 'function' were provided; please only use 'filter_by', as 'function' is deprecated")

        filter_func = filter_by or function

        if filter_func:
            return next(iter(filter(filter_func, self.__iterable)), default)
        else:
            return next(iter(self.__iterable), default)

    def get(self, index):
        """ Equivalent to calling **list(** *iterable* **)[** *index* **]**

        * This function will convert the *iterable* to a sequence type before retrieving the value at *index*
        * *-1* is not supported to get the last element; use **last()** instead

        :param index: element number inside *iterable*
        :return: value at *index* from *iterable*

        :raises IndexError: *index* is less than 0 or is out of bounds

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.get(2)
        5
        >>> values.get(-1)
        IndexError: index out of range
        >>> values.get(5)
        IndexError: index out of range
        """
        iterable_as_list = list(self.__iterable)

        if index < 0 or index >= len(iterable_as_list):
            raise IndexError("index out of range")

        return list(self.__iterable)[index]

    def last(self, filter_by=None, default=None):
        """ Equivalent to calling **next( iter( reversed( list( filter(** *filter_by, iterable* **) ) ) )** *, default* **)**

        :param filter_by: keyword-only; function used to filter unwanted values
        :param default: keyword-only value to return if *self* is empty after filtered by *filter_by*
        :return: last value of *self* filtered by *filter_by*

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.last()
        9
        >>> values.last(filter_by=lambda x: x < 5)
        2
        >>> values.last(filter_by=lambda x: x < 1) # Returns None
        >>> values.last(filter_by=lambda x: x < 1, default=0)
        0
        """
        if filter_by:
            reversed_iterable = reversed(list(filter(filter_by, self.__iterable)))
        else:
            reversed_iterable = reversed(list(self.__iterable))

        return next(iter(reversed_iterable), default)

    def skip(self, count):
        """ Skips the first *count* elements in *iterable*

        * This function will convert the *iterable* to a sequence type before retrieving the values
        * If *count* is equal to or greater than the length of *iterable*, no elements are taken

        :param count: number of values to skip
        :return: *Iterable* containing all the elements of *iterable* without the first *count* elements

        :raises ValueError: *count* is a negative value

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.skip(1).to_list()
        [2, 5, 9]
        >>> values.skip(3).to_list()
        [9]
        >>> values.skip(10).to_list()
        []
        >>> values.take(-1).to_list()
        ValueError: 'count' must be greater than 0
        """
        if count < 0:
            raise ValueError("'count' must be greater than 0")
        elif count == 0:
            return self
        elif count >= len(self.__iterable):
            return Iterable([])
        else:
            return Iterable(list(self.__iterable)[count:])

    def take(self, count):
        """ Gets the first *count* elements in *iterable*

        * This function will convert the *iterable* to a sequence type before retrieving the values
        * If *count* is equal to or greater than the length of *iterable*, all elements are taken

        :param count: number of values to retrieve
        :return: *Iterable* comprised of the first *count* elements

        :raises ValueError: *count* is a negative value

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.take(1).to_list()
        [1]
        >>> values.take(3).to_list()
        [1, 2, 5]
        >>> values.take(10).to_list()
        [1, 2, 5, 9]
        >>> values.take(-1).to_list()
        ValueError: 'count' must be greater than 0
        """
        if count < 0:
            raise ValueError("'count' must be greater than 0")
        elif count == 0:
            return Iterable([])
        elif count >= len(self.__iterable):
            return self
        else:
            return Iterable(list(self.__iterable)[:count])

    # Set-like transformations / functions
    def difference(self, iterable):
        """ Equivalent to calling **set(** *left* **).difference( set (** *iterable* **) )**

        :param iterable: iterable to check against for differences
        :return: New *Iterable* containing elements found in *self* but not *iterable*

        >>> left = [2, 10, 1982, -5, 9, 10]
        >>> right = [1982, -10, -5, 1982, 98]
        >>> Iterable(left).difference(right).to_list()
        [9, 2, 10]
        """
        return Iterable(set(self.__iterable).difference(set(iterable)))

    def distinct(self):
        """ Equivalent to calling **set(** *iterable* **)**

        :return: New *Iterable* containing only the distinct elements; order not preserved

        >>> values = Iterable([2, 10, 2, 2, 5, 9, 10])
        >>> values.distinct().to_list()
        [9, 2, 10, 5]
        """
        return Iterable(set(self.__iterable))

    def intersection(self, iterable):
        """ Equivalent to calling **set(** *left* **).intersection( set(** *right* **) )**

        :param iterable: iterable to intersect with *self*
        :return: *Iterable* with distinct values found in both *self* and *iterable*

        >>> left = [2, 10, 1982, -5, 9, 10]
        >>> right = [1982, -10, -5, 1982, 98]
        >>> Iterable(left).intersection(right).to_list()
        [-5, 1982]
        """
        return Iterable(set(self.__iterable).intersection(set(iterable)))

    def symmetric_difference(self, iterable):
        """ Equivalent to calling **set(** *left* **).symmetric_difference( set(** *right* **) )**

        :param iterable: iterable to perform symmetric difference against
        :return: *Iterable* with distinct values found in either *self* or *iterable* but not both

        >>> left = [2, 10, 1982, -5, 9, 10]
        >>> right = [1982, -10, -5, 1982, 98]
        >>> Iterable(left).symmetric_difference(right).to_list()
        [98, 2, 9, 10, -10]
        """
        return Iterable(set(self.__iterable).symmetric_difference(set(iterable)))

    def union(self, iterable):
        """ Equivalent to calling **set(** *left* **).union( set(** *right* **) )**

        :param iterable: iterable to union with *self*
        :return: *Iterable* with distinct values in either *self* or *iterable*

        >>> left = [2, 10, 2, 2, 5, 9, 10]
        >>> right = [1982, -10, 5, 1982, 9]
        >>> Iterable(left).union(right).to_list()
        [2, 5, 9, 10, -10, 1982]
        """
        return Iterable(set(self.__iterable).union(set(iterable)))
