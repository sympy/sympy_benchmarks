from __future__ import print_function, division
from distutils.version import LooseVersion
from sympy import Rational
import sympy
from sympy.geometry import (Line, Point,
                            Polygon)
from random import randint
listOfPolygons = [Polygon(Point(0+w,0+w),
                          Point(3+w,0+w),
                          Point(3+w,3+w),
                          Point(0+w,3+w)) for w in range(10)]
cutListOfPolygons = [Polygon((-1, -1), (1, Rational(5, 2)), (2, 1), (3, Rational(5, 2)), (4, 2), (5, 3), (-1, 3)) for w in range(10)]
cutLines = [Line((0, 0), (Rational(9, 2), 3)) for w in range(10)]

class PolygonAttributes:
    def time_create(self):
        "Creating Polygon"
        Polygon(Point(0, 0), Point(3, -1),Point(6, 0), Point(4, 5))

    def time_area(self):
        "Polygon.area for w in range(10)"
        [listOfPolygons[w].area for w in range(10)]

    def time_perimeter(self):
        "Polygon.perimeter for w in range(10)"
        [listOfPolygons[w].perimeter for w in range(10)]

    def time_sides(self):
        "Polygon.sides for w in range(10)"
        [listOfPolygons[w].sides for w in range(10)]

    def time_centroid(self):
        "Polygon.centroid for w in range(10)"
        [listOfPolygons[w].centroid for w in range(10)]

class PolygonIsConvex:
    def time_bench01(self):
        "Polygon.is_convex() for w in range(10)"
        [listOfPolygons[w].is_convex() for w in range(10)]

class PolygonEnclosesPoint:
    def time_bench01(self,Point2=Point(randint(0,10),randint(0,10))):
        "Polygon.encloses_point for w in range(10)"
        [listOfPolygons[w].encloses_point(Point2) for w in range(10)]

class PolygonArbitraryPoint:
    def time_bench01(self):
        "Polygon.arbitrary_point for w in range(10)"
        [listOfPolygons[w].arbitrary_point() for w in range(10)]

class PolygonDistance:
    def time_bench01(self):
        "Polygon.distance() for w in range(10)"
        [listOfPolygons[w].distance(Point(randint(0,10),randint(0,10))) for w in range(10)]

class PolygonSecondMoment:
    def setup(self):
        if LooseVersion(sympy.__version__) < LooseVersion("1.3.0"):
            raise NotImplementedError
    def time_bench01(self):
        "Polygon.second_moment_of_area() for w in range(10)"
        [listOfPolygons[w].second_moment_of_area() for w in range(10)]

class PolygonFirstMoment:
    def setup(self):
        if LooseVersion(sympy.__version__) < LooseVersion("1.5.0"):
            raise NotImplementedError
    def time_bench01(self):
        "Polygon.first_moment_of_area for w in range(10)"
        [listOfPolygons[w].first_moment_of_area() for w in range(10)]

class PolygonPolarSecondMoment:
    def setup(self):
        if LooseVersion(sympy.__version__) < LooseVersion("1.5.0"):
            raise NotImplementedError
    def time_bench01(self):
        "Polygon.polar_second_moment_of_area for w in range(10)"
        [listOfPolygons[w].polar_second_moment_of_area() for w in range(10)]

class PolygonSectionModulus:
    def setup(self):
        if LooseVersion(sympy.__version__) < LooseVersion("1.5.0"):
            raise NotImplementedError
    def time_bench01(self):
        "Polygon.section_modulus for w in range(10)"
        [listOfPolygons[w].section_modulus() for w in range(10)]

class PolygonCutSection:
    def setup(self):
        if LooseVersion(sympy.__version__) < LooseVersion("1.5.0"):
            raise NotImplementedError
    def time_bench01(self):
        "Polygon.cut_section for w in range(10)"
        [cutListOfPolygons[w].cut_section(cutLines[w]) for w in range(10)]
