#! /usr/bin/env python

import numpy as np


SIZEOF_INT = np.dtype(np.int).itemsize


def as_id_array(x):
    """Convert an array to an array of ids.

    Parameters
    ----------
    x : ndarray
        Array of IDs.

    Returns
    -------
    ndarray
        A, possibly new, array of IDs.

    Examples
    --------
    >>> import numpy as np
    >>> from landlab.core.utils import as_id_array
    >>> x = np.arange(5)
    >>> y = as_id_array(x)
    >>> y
    array([0, 1, 2, 3, 4])

    >>> x = np.arange(5, dtype=np.int)
    >>> y = as_id_array(x)
    >>> y
    array([0, 1, 2, 3, 4])

    >>> x = np.arange(5, dtype=np.int32)
    >>> y = as_id_array(x)
    >>> y
    array([0, 1, 2, 3, 4])
    >>> y.dtype == np.int
    True

    >>> x = np.arange(5, dtype=np.int64)
    >>> y = as_id_array(x)
    >>> y
    array([0, 1, 2, 3, 4])
    >>> y.dtype == np.int
    True

    >>> x = np.arange(5, dtype=np.intp)
    >>> y = as_id_array(x)
    >>> y
    array([0, 1, 2, 3, 4])
    >>> y.dtype == np.int
    True
    """
    if x.dtype == np.int:
        return x.view(np.int)
    else:
        return x.astype(np.int)


if np.dtype(np.intp) == np.int:
    def _as_id_array(x):
        if x.dtype == np.intp or x.dtype == np.int:
            return x.view(np.int)
        else:
            return x.astype(np.int)
else:
    def _as_id_array(x):
        if x.dtype == np.int:
            return x.view(np.int)
        else:
            return x.astype(np.int)


def get_functions_from_module(mod, pattern=None):
    import inspect, re

    funcs = {}
    for name, func in inspect.getmembers(mod, inspect.isroutine):
        if pattern is None or re.match(pattern, name):
            funcs[name] = func
    return funcs


def add_functions_to_class(cls, funcs):
    for name, func in funcs.items():
        setattr(cls, name, func)


def add_module_functions_to_class(cls, module, pattern=None):
    import inspect, imp, os

    caller = inspect.stack()[1]
    path = os.path.join(os.path.dirname(caller[1]), os.path.dirname(module))

    (module, _) = os.path.splitext(os.path.basename(module))

    mod = imp.load_module(module, *imp.find_module(module, [path]))

    funcs = get_functions_from_module(mod, pattern=pattern)
    add_functions_to_class(cls, funcs)


