# uplot-python

Python wrapper for [μPlot](https://github.com/leeoniya/uPlot) 📈

## Installation

### From PyPI

```console
pip install uplot-python
```

## Usage

The `plot` function has the same API as µPlot's `uPlot.plot`:

```py
import numpy as np
import uplot

t = np.linspace(0.0, 1.0, 10)
data = [t, np.exp(0.42 * t)]
opts = {
    "width": 1920,
    "height": 600,
    "title": "Example with plot",
    "series": [{}, { "stroke": "red", }, ],
}

uplot.plot(opts, data)
```

For convenience, the library also provides a `plot2` function with additional defaults, for an experience closer to `matplotlib.pyplot.plot`:

```py
import numpy as np
import uplot

t = np.linspace(0.0, 1.0, 10)
uplot.plot2(
    t,
    [np.exp(0.1 * t), np.exp(-10.0 * t), np.cos(t)],
    title="Example with plot2",
    left_labels=["exp(A t)", "exp(-B t)", "cos(t)"],
)
```

## See also

- [µPlot](https://github.com/leeoniya/uPlot): A small (~45 KB min), fast chart for time series, lines, areas, ohlc & bars.
- [Matplotlib](https://matplotlib.org/stable/): Comprehensive library for creating static, animated, and interactive visualizations.
- [matplotlive](https://github.com/stephane-caron/matplotlive): Stream live plots to a Matplotlib figure.
