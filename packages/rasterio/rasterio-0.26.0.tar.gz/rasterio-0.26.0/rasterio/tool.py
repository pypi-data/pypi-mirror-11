
import code
import collections
import logging

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

import numpy

import rasterio


logger = logging.getLogger('rasterio')

Stats = collections.namedtuple('Stats', ['min', 'max', 'mean'])

# Collect dictionary of functions for use in the interpreter in main()
funcs = locals()


def show(source, cmap='gray'):
    """Show a raster using matplotlib.

    The raster may be either an ndarray or a (dataset, bidx)
    tuple.
    """
    if isinstance(source, tuple):
        arr = source[0].read(source[1])
    else:
        arr = source
    if plt is not None:
        plt.imshow(arr, cmap=cmap)
        plt.show()
    else:
        raise ImportError("matplotlib could not be imported")


def stats(source):
    """Return a tuple with raster min, max, and mean.
    """
    if isinstance(source, tuple):
        arr = source[0].read(source[1])
    else:
        arr = source
    return Stats(numpy.min(arr), numpy.max(arr), numpy.mean(arr))


def main(banner, dataset, alt_interpreter=None):
    """ Main entry point for use with python interpreter """
    local = dict(funcs, src=dataset, np=numpy, rio=rasterio, plt=plt)
    if not alt_interpreter:
        code.interact(banner, local=local)
    elif alt_interpreter == 'ipython':
        import IPython
        IPython.InteractiveShell.banner1 = banner
        IPython.start_ipython(argv=[], user_ns=local)
    else:
        raise ValueError("Unsupported interpreter '%s'" % alt_interpreter)

    return 0
