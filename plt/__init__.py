from functools import wraps
import sys, importlib
__all__ = ["plt", "plot_wrapper", "plt_arr", "plot_wrapper_by_arraytype"]

# Two classes that act as wrappers for matplotlib.pyplot (potentially others)
# The first one checks for imported libraries and builds a dictionary accordingly
# The second one only looks at passed array types (less chance of generalizing, but easier code)

class plot_wrapper:
    def __init__(self, library=None):

        if library is None: import matplotlib.pyplot as library
        self.library = library

        self.array_type_dict = {  \
                    "cupy": \
                        [lambda array_lib: array_lib._core.core.ndarray, \
                         lambda array_type, x: getattr(array_type, "get")(x)], \
                    "torch": \
                        [lambda array_lib: array_lib.Tensor, \
                         lambda array_type, x: getattr(array_type, "cpu") (getattr(array_type, "detach")(x))] \
                                     }
        self.array_dict = None
        self.array_types = None

    def __getattr__(self, attr):
        func_to_be_wrapped = getattr(self.library, attr)

        @wraps(func_to_be_wrapped)
        def _wrapping(*args, **kwargs):

            if self.array_dict is None: self.check_imported_libraries()

            args = [self.to_numpy(arr) \
                    for arr in args]

            kwargs = {key:self.to_numpy(arr) \
                        for key, arr in kwargs.items()}

            return func_to_be_wrapped(*args, **kwargs)

        return _wrapping

    def to_numpy(self, arr):
        return self.array_dict.get(type(arr), lambda x: x)(arr) \
               if isinstance(arr, self.array_types) else arr

    def check_imported_libraries(self):
        imported_libraries = [lib for lib in self.array_type_dict.keys() \
                              if lib in sys.modules]

        self.array_dict = {}
        self.array_types = tuple()

        for lib in imported_libraries:
            array_type, array_to_numpy_func = self.fill_dictionary_from_library(lib)
            self.array_dict[array_type] = array_to_numpy_func
            self.array_types += (array_type,)

    def fill_dictionary_from_library(self, lib):
        aux = importlib.import_module(lib)
        array_type, array_to_numpy_func = self.array_type_dict[lib]
        return array_type(aux), lambda x: array_to_numpy_func(array_type(aux), x)

    def add_support(self, module_name, array_type_and_to_numpy_func):
        self.array_type_dict[module_name] = array_type_and_to_numpy_func
        self.check_imported_libraries()

plt = plot_wrapper()


class plot_wrapper_by_arraytype:
    def __init__(self, library=None):

        if library is None: import matplotlib.pyplot as library
        self.library = library

        self.array_type_dict = {  \
                    "cupy._core.core": \
                         lambda array_type, x: getattr(array_type, "get")(x), \
                    "torch": \
                         lambda array_type, x: getattr(array_type, "cpu") (getattr(array_type, "detach")(x)) \
                                     } #torch.Tensor
        self.supported_array_types = self.array_type_dict.keys()

    def __getattr__(self, attr):
        func_to_be_wrapped = getattr(self.library, attr)

        @wraps(func_to_be_wrapped)
        def _wrapping(*args, **kwargs):

            args = [arr if type(arr).__module__ not in self.supported_array_types \
                    else self.to_numpy(arr) \
                    for arr in args]

            kwargs = {key:arr if type(arr).__module__ not in self.supported_array_types \
                      else self.to_numpy(arr) \
                      for key, arr in kwargs.items()}

            return func_to_be_wrapped(*args, **kwargs)

        return _wrapping

    def to_numpy(self, arr):
        array_type = type(arr)
        return self.array_type_dict[array_type.__module__](array_type, arr)

    def add_support(self, array_module_name, array_to_numpy_func):
        self.array_type_dict[array_module_name] = array_to_numpy_func
        self.supported_array_types = self.array_type_dict.keys()

plt_arr = plot_wrapper_by_arraytype()
