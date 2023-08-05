from __future__ import division
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt


class MultiHistBase(object):

    def similar_blank_hist(self):
        newhist = deepcopy(self)
        newhist.histogram = np.zeros_like(self.histogram)
        return newhist

    @property
    def n(self):
        """Returns number of data points loaded into histogram"""
        return np.sum(self.histogram)

    # Overload binary numeric operators to work on histogram
    # TODO: logical operators

    def __getitem__(self, item):
        return self.histogram[item]

    def __setitem__(self, key, value):
        self.histogram[key] = value

    def __len__(self):
        return len(self.histogram)

    def __add__(self, other):
        return self.__class__.from_histogram(self.histogram.__add__(other), self.bin_edges, self.axis_names)

    def __sub__(self, other):
        return self.__class__.from_histogram(self.histogram.__sub__(other), self.bin_edges, self.axis_names)

    def __mul__(self, other):
        return self.__class__.from_histogram(self.histogram.__mul__(other), self.bin_edges, self.axis_names)

    def __truediv__(self, other):
        return self.__class__.from_histogram(self.histogram.__truediv__(other), self.bin_edges, self.axis_names)

    def __floordiv__(self, other):
        return self.__class__.from_histogram(self.histogram.__floordiv__(other), self.bin_edges, self.axis_names)

    def __mod__(self, other):
        return self.__class__.from_histogram(self.histogram.__mod__(other), self.bin_edges, self.axis_names)

    def __divmod__(self, other):
        return self.__class__.from_histogram(self.histogram.__divmod__(other), self.bin_edges, self.axis_names)

    def __pow__(self, other):
        return self.__class__.from_histogram(self.histogram.__pow__(other), self.bin_edges, self.axis_names)

    def __lshift__(self, other):
        return self.__class__.from_histogram(self.histogram.__lshift__(other), self.bin_edges, self.axis_names)

    def __rshift__(self, other):
        return self.__class__.from_histogram(self.histogram.__rshift__(other), self.bin_edges, self.axis_names)

    def __and__(self, other):
        return self.__class__.from_histogram(self.histogram.__and__(other), self.bin_edges, self.axis_names)

    def __xor__(self, other):
        return self.__class__.from_histogram(self.histogram.__xor__(other), self.bin_edges, self.axis_names)

    def __or__(self, other):
        return self.__class__.from_histogram(self.histogram.__or__(other), self.bin_edges, self.axis_names)

    def __neg__(self):
        return self.__class__.from_histogram(-self.histogram, self.bin_edges, self.axis_names)

    def __pos__(self):
        return self.__class__.from_histogram(+self.histogram, self.bin_edges, self.axis_names)

    def __abs__(self):
        return self.__class__.from_histogram(abs(self.histogram), self.bin_edges, self.axis_names)

    def __invert__(self):
        return self.__class__.from_histogram(~self.histogram, self.bin_edges, self.axis_names)


class Hist1d(MultiHistBase):
    axis_names = None

    @classmethod
    def from_histogram(cls, histogram, bin_edges, axis_names=None):
        """Make a Hist1D from a numpy bin_edges + histogram pair
        :param histogram: Initial histogram
        :param bin_edges: Bin edges of histogram. Must be one longer than length of histogram
        :param axis_names: Ignored. Sorry :-)
        :return:
        """
        if len(bin_edges) != len(histogram) + 1:
            raise ValueError("Bin edges must be of length %d, you gave %d!" % (len(histogram) + 1, len(bin_edges)))
        self = cls(bins=bin_edges)
        self.histogram = np.array(histogram)
        return self

    def __init__(self, data=None, bins=10, range=None, weights=None):
        """
        :param data: Initial data to histogram.
        :param bins: Number of bins, or list of bin edges (like np.histogram)
        :param weights: Weights for initial data.
        :param range: Range of histogram.
        :return: None
        """
        if data is None:
            data = []
        self.histogram, self.bin_edges = np.histogram(data, bins=bins, range=range, weights=weights)

    def add(self, data, weights=None):
        hist, _ = np.histogram(data, self.bin_edges, weights=weights)
        self.histogram += hist

    @property
    def bin_centers(self):
        return 0.5*(self.bin_edges[1:] + self.bin_edges[:-1])

    @property
    def density(self):
        """Gives emprical PDF, like np.histogram(...., density=True)"""
        h = self.histogram.astype(np.float)
        bindifs = np.array(np.diff(self.bin_edges), float)
        return h/(bindifs * self.n)

    @property
    def normalized_histogram(self):
        """Gives histogram with sum of entries normalized to 1."""
        return self.histogram/self.n

    @property
    def cumulative_histogram(self):
        return np.cumsum(self.normalized_histogram)

    @property
    def cumulative_density(self):
        cs = np.cumsum(self.histogram)
        return cs/cs[-1]

    def items(self):
        """Iterate over (bin_center, hist_value) from left to right"""
        return zip(self.bin_centers, self.histogram)

    @property
    def mean(self):
        """Estimates mean of underlying data, assuming each datapoint was exactly in the center of its bin."""
        return np.average(self.bin_centers, weights=self.histogram)

    @property
    def std(self, bessel_correction=True):
        """Estimates std of underlying data, assuming each datapoint was exactly in the center of its bin."""
        if bessel_correction:
            n = self.n
            bc = n/(n-1)
        else:
            bc = 1
        return np.sqrt(np.average((self.bin_centers-self.mean)**2, weights=self.histogram)) * bc

    def plot(self, normed=False, scale_errors_by=1.0, scale_histogram_by=1.0, plt=plt, **kwargs):
        """Plots the histogram with Poisson (sqrt(n)) error bars
          - scale_errors_by multiplies the error bars by its argument
          - scale_histogram_by multiplies the histogram AND the error bars by its argument
          - plt thing to call .errorbar on (pylab, figure, axes, whatever the matplotlib guys come up with next)
        """
        kwargs.setdefault('linestyle', 'none')
        yerr = np.sqrt(self.histogram)
        if normed:
            y = self.normed_histogram
            yerr /= self.n
        else:
            y = self.histogram.astype(np.float)
        yerr *= scale_errors_by * scale_histogram_by
        y *= scale_histogram_by
        plt.errorbar(
            self.bin_centers,
            y,
            yerr,
            marker='.',
            **kwargs
        )


class Histdd(MultiHistBase):
    """multidimensional histogram object
    """

    @classmethod
    def from_histogram(cls, histogram, bin_edges, axis_names=None):
        """Make a HistdD from numpy histogram + bin edges
        :param histogram: Initial histogram
        :param bin_edges: x bin edges of histogram, y bin edges, ...
        :return: Histnd instance
        """
        bin_edges = np.array(bin_edges)
        self = cls(bins=bin_edges, axis_names=axis_names)
        self.histogram = histogram
        return self

    def __init__(self, *data, bins=10, range=None, weights=None, axis_names=None):
        if len(data) == 0:
            if range is None:
                if bins is None:
                    raise ValueError("Must specify data, bins, or range")
                try:
                    dimensions = len(bins)
                except TypeError:
                    raise ValueError("If you specify no data and no ranges, must specify a bin specification "
                                     "which tells me what dimension you want. E.g. [10, 10, 10] instead of 10.")
            else:
                dimensions = len(range)
            data = np.zeros((0, dimensions)).T
        self.histogram, self.bin_edges = np.histogramdd(np.array(data).T, bins=bins, weights=weights, range=range)
        self.axis_names = axis_names

    def add(self, *data, weights=None):
        self.histogram += np.histogramdd(np.array(data).T, bins=self.bin_edges, weights=weights)[0]

    @property
    def dimensions(self):
        return len(self.bin_edges)

    def get_axis_number(self, axis):
        if self.axis_names is None:
            return axis
        if axis in self.axis_names:
            return self.axis_names.index(axis)
        return axis

    def other_axes(self, axis):
        axis = self.get_axis_number(axis)
        return tuple([i for i in range(self.dimensions) if i != axis])

    def axis_names_without(self, axis):
        """Return axis names without axis, or None if axis_names is None"""
        if self.axis_names is None:
            return None
        return self.axis_names[self.other_axes(axis)]

    @property
    def bin_centers(self, axis=0):
        """Return bin centers along an axis, or if axis=None, list of bin_centers along each axis"""
        axis = self.get_axis_number(axis)
        if axis is None:
            return np.array([self.bin_centers(i) for i in range(self.dimensions)])
        return 0.5*(self.bin_edges[axis, 1:] + self.bin_edges[axis, :-1])

    def projection(self, axis=0):
        """Sums all data along all other axes, then return Hist1D"""
        axis = self.get_axis_number(axis)
        projected_hist = np.sum(self.histogram, axis=self.other_axes(axis))
        return Hist1d.from_histogram(projected_hist, bin_edges=self.bin_edges[axis])

    def average(self, axis=0):
        """Return d-1 dimensional histogram of (estimated) mean value of axis"""
        axis = self.get_axis_number(axis)
        meshgrid = np.meshgrid(*self.bin_centers)
        avg_hist = np.average(meshgrid[axis], weights=self.histogram, axis=axis)
        return Histdd.from_histogram(histogram=avg_hist,
                                     bin_edges=self.bin_centers[self.other_axes(axis)],
                                     axis_names=self.axis_names_without(axis))

    def sum(self, axis=0):
        """Sums all data along axis, returns d-1 dimensional histogram"""
        axis = self.get_axis_number(axis)
        return Histdd.from_histogram(np.sum(self.histogram, axis=axis),
                                     bin_edges=self.bin_edges[self.other_axes(axis)],
                                     axis_names=self.axis_names_without(axis))

    def slice(self, start, stop, axis='x'):
        """Restrict histogram to bins whose data values (not bin numbers) along axis are between start and stop
        (both inclusive). Returns d dimensional histogram."""
        axis = self.get_axis_number(axis)
        bin_edges = self.bin_edges[axis]
        start_bin = np.digitize([start], bin_edges)[0]
        stop_bin = np.digitize([stop], bin_edges)[0]
        if not (1 <= start_bin <= len(bin_edges)-1 and 1 <= stop_bin <= len(bin_edges)-1):
            raise ValueError("Slice start/stop values are not in range of histogram")
        new_bin_edges = bin_edges.copy()
        new_bin_edges[axis] = new_bin_edges[start_bin:stop_bin+2]   # TODO: Test off by one here!
        return Histdd.from_histogram(np.take(self.histogram, np.arange(start_bin, stop_bin + 1)),
                                     bin_edges=new_bin_edges, axis_names=self.axis_names)

    def plot(self, **kwargs):
        if self.dimensions == 1:
            Hist1d.from_histogram(self.histogram, self.bin_edges[0]).plot()
        elif self.dimensions == 2:
            plt.pcolormesh(self.bin_edges[0], self.bin_edges[1], self.histogram.T, **kwargs)
            plt.xlim(np.min(self.bin_edges[0]), np.max(self.bin_edges[0]))
            plt.ylim(np.min(self.bin_edges[1]), np.max(self.bin_edges[1]))
            plt.colorbar()
        else:
            raise ValueError("Can only plot 1- or 2-dimensional histograms!")


if __name__ == '__main__':
    # Create histograms just like from numpy...
    m = Hist1d([0, 3, 1, 6, 2, 9], bins=3)

    # ...or add data incrementally:
    m = Hist1d(bins=100, range=(-3, 4))
    m.add(np.random.normal(0, 0.5, 10**4))
    m.add(np.random.normal(2, 0.2, 10**3))

    # Get the data back out:
    print(m.histogram, m.bin_edges)

    # Access derived quantities like bin_centers, normalized_histogram, density, cumulative_density, mean, std
    plt.plot(m.bin_centers, m.normalized_histogram, label="Normalized histogram", linestyle='steps')
    plt.plot(m.bin_centers, m.density, label="Empirical PDF", linestyle='steps')
    plt.plot(m.bin_centers, m.cumulative_density, label="Empirical CDF", linestyle='steps')
    plt.title("Estimated mean %0.2f, estimated std %0.2f" % (m.mean, m.std))
    plt.legend(loc='best')
    plt.show()

    # Slicing and arithmetic behave just like ordinary ndarrays
    print("The fourth bin has %d entries" % m[3])
    m[1:4] += 4 + 2 * m[-27:-24]
    print("Now it has %d entries" % m[3])

    # Of course I couldn't resist adding a canned plotting function:
    m.plot()
    plt.show()

    # Create and show a 2d histogram. Axis names are optional.
    m2 = Histdd(bins=100, range=[[-5, 3], [-3, 5]], axis_names=['x', 'y'])
    m2.add(np.random.normal(1, 1, 10**6), np.random.normal(1, 1, 10**6))
    m2.add(np.random.normal(-2, 1, 10**6), np.random.normal(2, 1, 10**6))
    m2.plot()
    plt.show()

    # x and y projections return Hist1d objects
    m2.projection('x').plot(label='x projection')
    m2.projection(1).plot(label='y projection')
    plt.legend()
    plt.show()
