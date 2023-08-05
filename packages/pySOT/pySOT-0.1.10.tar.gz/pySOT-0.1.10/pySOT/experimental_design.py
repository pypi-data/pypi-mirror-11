"""
.. module:: experimental_design
  :synopsis: Methods for generating an experimental design.
.. moduleauthor:: David Eriksson <dme65@cornell.edu>,
                 Yi Shen <ys623@cornell.edu>

:Module: experimental_design
:Author: David Eriksson <dme65@cornell.edu>,
    Yi Shen <ys623@cornell.edu>
"""

import numpy as np
import pyDOE as pydoe


class LatinHypercube(object):
    """Latin Hypercube experimental design

    :ivar dim: Number of dimensions
    :ivar npts: Number of desired sampling points
    :ivar criterion: A string that tells lhs how to sample the
        points (default: None which simply randomizes the points
        within the intervals):
            - "center" or "c": center the points within the sampling intervals
            - "maximin" or "m": maximize the minimum distance
                between points, but place the point in a randomized
                location within its interval
            - "centermaximin" or "cm": same as "maximin", but
                centered within the intervals
            - "correlation" or "corr": minimize the maximum
                correlation coefficient
    """

    def __init__(self, dim, npts, criterion='c'):
        self.dim = dim
        self.npts = npts
        self.criterion = criterion

    def generate_points(self):
        """Generate a matrix with the initial sample points,
        scaled to the unit cube

        :return: Latin hypercube design in the unit cube
        """
        return pydoe.lhs(self.dim, self.npts, self.criterion)


class SymmetricLatinHypercube(object):
    """Symmetric Latin Hypercube experimental design

    :ivar dim: Number of dimensions
    :ivar npts: Number of desired sampling points
    """
    def __init__(self, dim, npts):
        self.dim = dim
        self.npts = npts

    def _slhd(self):
        """Generate matrix of sample points in the unit box"""

        # Generate a one-dimensional array based on sample number
        points = np.zeros([self.npts, self.dim])
        points[:, 0] = np.arange(1, self.npts+1)

        # Get the last index of the row in the top half of the hypercube
        middleind = self.npts//2

        # special manipulation if odd number of rows
        if self.npts % 2 == 1:
            points[middleind, :] = middleind + 1

        # Generate the top half of the hypercube matrix
        for j in range(1, self.dim):
            for i in range(middleind):
                if np.random.random() < 0.5:
                    points[i, j] = self.npts-i
                else:
                    points[i, j] = i + 1
            np.random.shuffle(points[:middleind, j])

        # Generate the bottom half of the hypercube matrix
        for i in range(middleind, self.npts):
            points[i, :] = self.npts + 1 - points[self.npts - 1 - i, :]

        return points/self.npts

    def generate_points(self):
        """Generate a matrix no rank deficiency with the initial
        sample points, scaled to the unit cube

        :return: Symmetric Latin hypercube design in the unit cube
        """
        rank_pmat = 0
        pmat = np.ones((self.npts, self.dim+1))
        xsample = None
        while rank_pmat != self.dim + 1:
            xsample = self._slhd()
            pmat[:, 1:] = xsample
            rank_pmat = np.linalg.matrix_rank(pmat)
        return xsample


# ========================= For Test =======================

def _main():
    print("========================= LHD =======================")
    lhs = LatinHypercube(4, 10, criterion='c')
    print(lhs.generate_points())

    print("\n========================= SLHD =======================")
    slhd = SymmetricLatinHypercube(3, 10)
    print(slhd.generate_points())

if __name__ == "__main__":
    _main()
