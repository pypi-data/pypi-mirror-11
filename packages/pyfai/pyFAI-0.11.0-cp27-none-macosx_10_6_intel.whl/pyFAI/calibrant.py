#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Azimuthal integration
#             https://github.com/pyFAI/pyFAI
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Calibrant

A module containing classical calibrant and also tools to generate d-spacing.

Interesting formula:
http://geoweb3.princeton.edu/research/MineralPhy/xtalgeometry.pdf
"""

from __future__ import absolute_import, print_function, with_statement

__author__ = "Jerome Kieffer"
__contact__ = "Jerome.Kieffer@ESRF.eu"
__license__ = "GPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "22/04/2015"
__status__ = "production"


import os
import logging
import numpy
import itertools
from math import sin, asin, cos, sqrt, pi, ceil, floor
import threading
from .utils import get_calibration_dir
logger = logging.getLogger("pyFAI.calibrant")
epsilon = 1.0e-6  # for floating point comparison

class Cell(object):
    """
    This is a cell object, able to calculate the volume and d-spacing according to formula from:

    http://geoweb3.princeton.edu/research/MineralPhy/xtalgeometry.pdf
    """
    lattices = ["cubic", "tetragonal", "hexagonal", "rhombohedral", "orthorhombic", "monoclinic", "triclinic"]
    types = {"P":"Primitive", "I":"Body centered", "F":"Face centered", "C": "Side centered", "R": "Rhombohedral"}

    def __init__(self, a=1, b=1, c=1, alpha=90, beta=90, gamma=90, lattice="triclinic", lattice_type="P"):
        """
        Crystalographic units are Angstrom for distances and degrees for angles !

        @param a,b,c: unit cell length in Angstrom
        @param alpha, beta, gamma: unit cell angle in degrees

        """
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.lattice = lattice if lattice in self.lattices else "triclinic"
        self.type = lattice_type if lattice_type in self.types else "P"
        self._volume = None
        self.S11 = None
        self.S12 = None
        self.S13 = None
        self.S22 = None
        self.S23 = None

    def __repr__(self, *args, **kwargs):
        return "%s %s cell a=%.4f b=%.4f c=%.4f alpha=%.3f beta=%.3f gamma=%.3f" % \
            (self.types[self.type], self.lattice, self.a, self.b, self.c, self.alpha, self.beta, self.gamma)

    @classmethod
    def cubic(cls, a):
        """
        Factory for cubic lattices
        @param a: unit cell length
        """
        self = cls()
        self.lattice = "cubic"
        a = float(a)
        self.a = a
        self.b = a
        self.c = a
        self.alpha = 90
        self.beta = 90
        self.gamma = 90
        return self

    @classmethod
    def tetragonal(cls, a, c):
        """
        Factory for tetragonal lattices
        @param a: unit cell length
        @param c: unit cell length
        """
        self = cls()
        self.lattice = "tetragonal"
        a = float(a)
        self.a = a
        self.b = a
        self.c = float(c)
        self.alpha = 90
        self.beta = 90
        self.gamma = 90
        return self

    @classmethod
    def orthorhombic(cls, a, b, c):
        """
        Factory for tetragonal lattices
        @param a: unit cell length
        @param b: unit cell length
        @param c: unit cell length
        """
        self = cls()
        self.lattice = "orthorhombic"
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.alpha = 90
        self.beta = 90
        self.gamma = 90
        return self

    @classmethod
    def hexagonal(cls, a, c):
        """
        Factory for hexagonal lattices
        @param a: unit cell length
        @param c: unit cell length
        """
        self = cls()
        self.lattice = "hexagonal"
        a = float(a)
        self.a = a
        self.b = a
        self.c = float(c)
        self.alpha = 90
        self.beta = 90
        self.gamma = 120
        return self

    @classmethod
    def monoclinic(cls, a, b, c, beta):
        """
        Factory for hexagonal lattices
        @param a: unit cell length
        @param b: unit cell length
        @param c: unit cell length
        @param beta: unit cell angle
        """
        self = cls()
        self.lattice = "monoclinic"
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.alpha = 90
        self.beta = float(beta)
        self.gamma = 90
        return self

    @classmethod
    def rhombohedral(cls, a, alpha):
        """
        Factory for hexagonal lattices
        @param a: unit cell length
        @param alpha: unit cell angle
        """
        self = cls()
        self.lattice = "rhombohedral"
        a = float(a)
        alpha = float(a)
        self.a = a
        self.b = a
        self.c = a
        self.alpha = alpha
        self.beta = alpha
        self.gamma = alpha
        return self

    # TODO: continue

    @property
    def volume(self):
        if self._volume is None:
            self._volume = self.a * self.b * self.c
            if self.lattice not in ["cubic", "tetragonal", "orthorhombic"]:
                cosa = cos(self.alpha * pi / 180.)
                cosb = cos(self.beta * pi / 180.)
                cosg = cos(self.gamma * pi / 180.)
                self._volume *= sqrt(1 - cosa ** 2 - cosb ** 2 - cosg ** 2 + 2 * cosa * cosb * cosg)
        return self._volume

    def d(self, hkl):
        """
        Calculate the actual d-spacing for a 3-tuple of
        """
        h, k, l = hkl
        if self.lattice in ["cubic", "tetragonal", "orthorhombic"]:
            invd2 = (h / self.a) ** 2 + (k / self.b) ** 2 + (l / self.c) ** 2
        else:
            if self.S11 is None:
                alpha = self.alpha * pi / 180.
                cosa = cos(alpha)
                sina = sin(alpha)
                beta = self.beta * pi / 180.
                cosb = cos(beta)
                sinb = sin(beta)
                gamma = self.gamma * pi / 180.
                cosg = cos(gamma)
                sing = sin(gamma)

                self.S11 = (self.b * self.c * sina) ** 2
                self.S22 = (self.a * self.c * sinb) ** 2
                self.S33 = (self.a * self.b * sing) ** 2
                self.S12 = self.a * self.b * self.c * self.c * (cosa * cosb - cosg)
                self.S23 = self.a * self.a * self.b * self.c * (cosb * cosg - cosa)
                self.S13 = self.a * self.b * self.b * self.c * (cosg * cosa - cosb)

            invd2 = self.S11 * h * h + \
                    self.S22 * k * k + \
                    self.S33 * l * l + \
                    2 * self.S12 * h * k + \
                    2 * self.S23 * k * l + \
                    2 * self.S13 * h * l
            invd2 /= (self.volume) ** 2
        return sqrt(1 / invd2)

    def d_spacing(self, dmin=1.0):
        """
        @param dmin: minimum value of
        @return: dict d-spacing as string, list of tuple with Miller indices preceded with the numerical value
        """
        hmax = int(ceil(self.a / dmin))
        kmax = int(ceil(self.b / dmin))
        lmax = int(ceil(self.c / dmin))
        res = {}
        for hkl in itertools.product(range(-hmax, hmax + 1),
                                     range(-kmax, kmax + 1),
                                     range(-lmax, lmax + 1)):
            h, k, l = hkl
            if hkl == (0, 0, 0):
                continue
            if self.type == "I" and ((h + k + l) % 2 != 0):
                continue
            if self.type == "C" and ((h + k) % 2 != 0):
                continue
            if self.type == "F" and ((h % 2 + k % 2 + l % 2) not in (0, 3)):
                continue
            if self.type == "R" and ((h - k + l) % 3 != 0):
                continue

            d = self.d(hkl)
            strd = "%.8e" % d
            if d < dmin:
                continue
            if strd in res:
                res[strd].append(hkl)
            else:
                res[strd] = [d, hkl]
        return res

    def save(self, name, long_name=None, doi=None, dmin=1.0, dest_dir=None):
        """
        Save informations about the cell in a d-spacing file, usable as Calibrant

        @param name: name of the calibrant
        @param doi: reference of the publication used to parametrize the cell
        @param dmin: minimal d-spacing
        @param dest_dir: name of the directory where to save the result
        """
        fname = name + ".D"
        if dest_dir:
            fname = os.path.join(dest_dir, fname)
        with open(fname, "w") as f:
            if long_name:
                f.write("# Calibrant: %s (%s)%s" % (long_name, name, os.linesep))
            else:
                f.write("# Calibrant: %s%s" % (name, os.linesep))
            f.write("# %s%s" % (self, os.linesep))
            if doi:
                f.write("# Ref: %s%s" % (doi, os.linesep))
            d = self.d_spacing(dmin)
            ds = [i[0] for i in d.values()]
            ds.sort(reverse=True)
            for k in ds:
                strk = "%.8e" % k
                f.write("%.8f # %s %s%s" % (k, d[strk][-1], len(d[strk]) - 1, os.linesep))


class Calibrant(object):
    """
    A calibrant is a reference compound where the d-spacing (interplanar distances)
    are known. They are expressed in Angstrom (in the file)
    """
    def __init__(self, filename=None, dSpacing=None, wavelength=None):
        object.__init__(self)
        self._filename = filename
        self._wavelength = wavelength
        self._sem = threading.Semaphore()
        self._2th = []
        if dSpacing is None:
            self._dSpacing = []
        else:
            self._dSpacing = list(dSpacing)
        if self._dSpacing and self._wavelength:
            self._calc_2th()

    def __repr__(self):
        name = "undefined"
        if self._filename:
            name = os.path.splitext(os.path.basename(self._filename))[0]
        name += " Calibrant "
        if len(self._dSpacing):
            name += "with %i reflections " % len(self._dSpacing)
        if self._wavelength:
            name += "at wavelength %s" % self._wavelength
        return name

    def load_file(self, filename=None):
        with self._sem:
            if filename:
                self._filename = filename
            if not os.path.isfile(self._filename):
                logger.error("No such calibrant file: %s" % self._filename)
                return
            self._filename = os.path.abspath(self._filename)
            self._dSpacing = numpy.unique(numpy.loadtxt(self._filename))
            self._dSpacing = list(self._dSpacing[-1::-1])  # reverse order
#            self._dSpacing.sort(reverse=True)
            if self._wavelength:
                self._calc_2th()

    def save_dSpacing(self, filename=None):
        """
        save the d-spacing to a file

        """
        if filename == None and self._filename is not None:
            filename = self._filename
        else:
            return
        with open(filename) as f:
            f.write("# %s Calibrant" % filename)
            for i in self.dSpacing:
                f.write("%s\n" % i)

    def get_dSpacing(self):
        if not self._dSpacing and self._filename:
            self.load_file()
        return self._dSpacing

    def set_dSpacing(self, lst):
        self._dSpacing = list(lst)
        self._filename = "Modified"
        if self._wavelength:
            self._calc_2th()
    dSpacing = property(get_dSpacing, set_dSpacing)

    def append_dSpacing(self, value):
        with self._sem:
            delta = [abs(value - v) / v for v in self._dSpacing if v is not None]
            if not delta or min(delta) > epsilon:
                self._dSpacing.append(value)
                self._dSpacing.sort(reverse=True)
                self._calc_2th()
    def append_2th(self, value):
        with self._sem:
            if value not in self._2th:
                self._2th.append(value)
                self._2th.sort()
                self._calc_dSpacing()

    def setWavelength_change2th(self, value=None):
        with self._sem:
            if value:
                self._wavelength = float(value)
                if self._wavelength < 1e-15 or self._wavelength > 1e-6:
                    logger.warning("This is an unlikely wavelength (in meter): %s" % self._wavelength)
                self._calc_2th()

    def setWavelength_changeDs(self, value=None):
        """
        This is probably not a good idea, but who knows !
        """
        with self._sem:
            if value:
                self._wavelength = float(value)
                if self._wavelength < 1e-15 or self._wavelength > 1e-6:
                    logger.warning("This is an unlikely wavelength (in meter): %s" % self._wavelength)
                self._calc_dSpacing()

    def set_wavelength(self, value=None):
        updated = False
        with self._sem:
            if self._wavelength is None:
                if value:
                    self._wavelength = float(value)
                    if (self._wavelength < 1e-15) or (self._wavelength > 1e-6):
                        logger.warning("This is an unlikely wavelength (in meter): %s" % self._wavelength)
                    updated = True
            elif abs(self._wavelength - value) / self._wavelength > epsilon:
                logger.warning("Forbidden to change the wavelength once it is fixed !!!!")
                logger.warning("%s != %s, delta= %s" % (self._wavelength, value, self._wavelength - value))
        if updated:
            self._calc_2th()

    def get_wavelength(self):
        return self._wavelength
    wavelength = property(get_wavelength, set_wavelength)

    def _calc_2th(self):
        if self._wavelength is None:
            logger.error("Cannot calculate 2theta angle without knowing wavelength")
            return
        self._2th = []
        for ds in self._dSpacing:
            try:
                tth = 2.0 * asin(5.0e9 * self._wavelength / ds)
            except ValueError:
                tth = None
                if self._2th:
                    self._dSpacing = self._dSpacing[:len(self._2th)]
                    # avoid turning around...
                    break
            else:
                self._2th.append(tth)

    def _calc_dSpacing(self):
        if self._wavelength is None:
            logger.error("Cannot calculate 2theta angle without knowing wavelength")
            return
        self._dSpacing = [5.0e9 * self._wavelength / sin(tth / 2.0) for tth in self._2th]

    def get_2th(self):
        if not self._2th:
            ds = self.dSpacing  # forces the file reading if not done
            if not ds:
                logger.error("Not d-spacing for calibrant: %s" % self)
            with self._sem:
                if not self._2th:
                    self._calc_2th()
        return self._2th

    def get_2th_index(self, angle):
        """
        return the index in the 2theta angle index
        """
        idx = None
        if angle:
            idx = self._2th.find(angle)
        if idx == -1:
            idx = None
        return idx

    def fake_calibration_image(self, ai, shape=None, Imax=1.0, U=0, V=0, W=0.0001):
        """
        Generates a fake calibration image from an azimuthal integrator

        @param ai: azimuthal integrator
        @param Imax: maximum intensity of rings
        @param U, V, W: width of the peak from Caglioti's law (FWHM^2 = Utan(th)^2 + Vtan(th) + W)

        """
        if shape is None:
            if ai.detector.shape:
                shape = ai.detector.shape
            elif ai.detector.max_shape:
                 shape = ai.detector.max_shape
        if shape is None:
            raise RuntimeError("No shape available")
        tth = ai.twoThetaArray(shape)
        tth_min = tth.min()
        tth_max = tth.max()
        dim = int(numpy.sqrt(shape[0] * shape[0] + shape[1] * shape[1]))
        tth_1d = numpy.linspace(tth_min, tth_max, dim)
        tanth = numpy.tan(tth_1d / 2.0)
        fwhm2 = U * tanth ** 2 + V * tanth + W
        sigma2 = fwhm2 / (8.0 * numpy.log(2.0))
        signal = numpy.zeros_like(sigma2)
        for t in self.get_2th():
            if t >= tth_max:
                break
            else:
                signal += Imax * numpy.exp(-(tth_1d - t) ** 2 / (2.0 * sigma2))
        res = ai.calcfrom1d(tth_1d, signal, shape=shape, mask=ai.mask,
                   dim1_unit='2th_rad', correctSolidAngle=True)
        return res


class calibrant_factory(object):
    """
    Behaves like a dict but is actually a factory:
    Each time one retrieves an object it is a new geniune new calibrant (unmodified)
    """
    def __init__(self, basedir=None):
        """
        Constructor

        @param basedir: directory name where to search for the calibrants
        """
        if basedir is None:
            basedir = get_calibration_dir()
        self.directory = basedir
        if not os.path.isdir(self.directory):
            logger.warning("No calibrant directory: %s" % self.directory)
            self.all = {}
        else:
            self.all = dict([(os.path.splitext(i)[0], os.path.join(self.directory, i))
                             for i in os.listdir(self.directory)
                             if i.endswith(".D")])

    def __getitem__(self, what):
        return Calibrant(self.all[what])

    def get(self, what, notfound=None):
        if what in self.all:
            return Calibrant(self.all[what])
        else:
            return notfound

    def __contains__(self, k):
        return k in self.all

    def __repr__(self):
        return "Calibrants available: %s" % (", ".join(list(self.all.keys())))

    def __len__(self):
        return len(self.all)

    def keys(self):
        return list(self.all.keys())

    def values(self):
        return [Calibrant(i) for i in  self.all.values()]

    def items(self):
        return [(i, Calibrant(j)) for i, j in self.all.items()]

    __call__ = __getitem__

    has_key = __contains__

ALL_CALIBRANTS = calibrant_factory()
