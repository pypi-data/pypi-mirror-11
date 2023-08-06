from functools import reduce


class Iterable:

    def __init__(self, iterable):
        iter(iterable)
        self.__iterable = iterable

    def __iter__(self):
        return self.__iterable.__iter__()

    def __len__(self):
        return len(self.__iterable)

    # built-in equivalent data structures
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

            :return: True if all elements in *Iterable* are True, else False

            >>> Iterable([True, False, True]).all()
            False
            >>> Iterable([True, True, True, True]).all()
            True
        """
        return all(self.__iterable)

    def any(self):
        """ Equivalent to the built-in function **any(** *iterable* **)**

            :return: True if any element in *Iterable* is True, else False

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
        [(5, 'a'), (6, 'b'), (7, 'c'), (8, 'd'), (5, 'f')]
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

        :return: number of items in *Iterable*

        >>> grades = Iterable(['a', 'b', 'c', 'd', 'f'])
        >>> grades.len()
        5
        """
        return self.__len__()

    def map(self, function):
        """ Equivalent to the built-in function **map(** *function, iterable* **)**

        :param function: function applied to every item in *Iterable*
        :return: *Iterable* of results

        >>> numbers = Iterable([1, 3, 10, 4, 8])
        >>> numbers.map(lambda x: x * 2).to_list()
        [2, 6, 20, 8, 16]
        """
        return Iterable(map(function, self.__iterable))

    def max(self, **kwargs):
        """ Equivalent to the built-in function **max(** *iterable, \*[, key, default]* **)**

        :param key: keyword-only; function that returns the value to compare
        :param default: keyword-only; value to return if *Iterable* is empty. Only available in Python 3.4 or later
        :return: largest item in *Iterable*

        >>> grades = Iterable([('Charlie', 79), ('Alice', 94), ('Bob', 65)])
        >>> grades.max(key=lambda x: x[1])
        ('Alice', 94)
        """
        return max(self.__iterable, **kwargs)

    def min(self, **kwargs):
        """ Equivalent to the built-in function **min(** *iterable, \*[, key, default]* **)**

        :param key: keyword-only; function that returns the value to compare
        :param default: keyword-only; value to return if *Iterable* is empty. Only available in Python 3.4 or later
        :return: smallest item in *Iterable*

        >>> grades = Iterable([('Charlie', 79), ('Alice', 94), ('Bob', 65)])
        >>> grades.min(key=lambda x: x[1])
        ('Bob', 65)
        """
        return min(self.__iterable, **kwargs)

    def reversed(self):
        """ Equivalent to the built-in function **reversed(** *seq* **)**

        :return: *Iterable* in the reversed order

        >>> names = Iterable(['Bob', 'Alice', 'Daniel', 'Charlie'])
        >>> names.reversed().to_list()
        ['Charlie', 'Daniel', 'Alice', 'Bob']
        """
        return Iterable(reversed(self.__iterable))

    def sorted(self, **kwargs):
        """ Equivalent to the built-in function **sorted(** *iterable[, cmp[, key[, reverse]]]* **)**

        :param cmp: keyword-only; custom comparison function. Only available in Python 2.x
        :param key: keyword-only; function that returns the value to compare
        :param reverse: keyword-only; boolean; if True, *Iterable* is sorted with the largest value fist
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
        :return: list of tuples; i-th tuple contains all elements from each i-th element in *Iterable* and *\*args*

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
        :param initializer: initial value combined with the first value in *Iterable*
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

    # custom transformations
    def first(self, function=None, default=None):
        """ Equivalent to calling **next( iter( filter(** *function, iterable* **)** *, default* **)**

        :param function: function used to filter unwanted values
        :param default: value to return if *Iterable* is empty after filtered by *func*
        :return: first value of *Iterable* filtered by *func*

        >>> values = Iterable([1, 2, 5, 9])
        >>> values.first()
        1
        >>> values.first(function=lambda x: x > 5)
        9
        >>> values.first(function=lambda x: x > 10, 0)
        0
        """
        if function:
            return next(iter(filter(function, self.__iterable)), default)
        else:
            return next(iter(self.__iterable), default)
