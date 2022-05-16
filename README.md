# plt
A matplotlib.pyplot wrapper for gpu arrays (cupy, pytorch, etc.) without any of the `.get` / `.detach` / `.cpu` abracadabra.

<!-- ### **Decision Boundary Viewer** (`boundviewer`) -->
## Installation and usage
`plt` can be installed with PyPI:

```
pip install plt-wrapper
```

To use `plt`: simply import the module

```python
from plt import plt
```

and proceed with `plt` as if you had just gone through the now-classic import `import matplotlib.pyplot as plt`. For example:

```python
from plt import plt
import cupy as cp
arr = cp.arange(10)
plt.plot(arr)
plt.show()
```

The wrapper will automatically detect the type of the arrays in your pyplot call (both args and kwargs) and cast them to cpu on numpy.
To test with numpy or pytorch here you would simply change `import X as cp` and run the exact same lines of code.
Support for cupy and pytorch at the moment, but contributions welcome.

<!-- ### **Decision Boundary Viewer** (`boundviewer`) -->
## Other
To wrap any other library or matplotlib module "lib" with to-cpu casting do:

```python
from plt import plt_wrapper
import module as lib
plt = plt_wrapper(lib)
```

To add support to other libraries you are very welcome to contribute here or proceed it for yourself only:

```python
from plt import plt
plt.add_support("cupy", [lambda array_lib: array_lib._core.core.ndarray, \
                         lambda array_type, x: getattr(array_type, "get")(x)])
```
where here we would have added cupy support if it did not already exist.

`from plt import plt` imports an already-initialized class `plt_wrapper(matplotlib.pyplot)`.
`plt_wrapper` looks for the cupy and pytorch libraries in your env to do the setup.
Alternatively, `plt_wrapper_by_arraytype`, and its initialized equivalent `plt_arr`, achieve the same wrapping results but fetching directly by array type in the `.__module__`:

```python
from plt import plt_arr as plt
plt.add_support("cupy._core.core", \
                         lambda array_type, x: getattr(array_type, "get")(x))
```
