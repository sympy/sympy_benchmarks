from __future__ import print_function, division

from sympy import Rational
from sympy.geometry import (Line, Point,
                            Polygon)
from random import randint

class PolygonTests:
	def setup(self):
		self.listOfPolygons = [Polygon(Point(0+w,0+w),
		Point(3+w,0+w),
		Point(3+w,3+w),
		Point(0+w,3+w)) for w in range(10)]
		self.cutListOfPolygons = [Polygon((-1, -1), (1, Rational(5, 2)), (2, 1), (3, Rational(5, 2)), (4, 2), (5, 3), (-1, 3)) for w in range(10)]
		self.cutLines = [Line((0, 0), (Rational(9, 2), 3)) for w in range(10)]

	def time_create_polygon(self):
	    "Creating Polygon"
	    Polygon(Point(0, 0), Point(3, -1),Point(6, 0), Point(4, 5))

	def polygon_area(self):
	   "Polygon.area for w in range(10)"
	   [self.listOfPolygons[w].area for w in range(10)]

	def time_polygon_perimeter(self):
	    "Polygon.perimeter for w in range(10)"
	    [self.listOfPolygons[w].perimeter for w in range(10)]

	def time_polygon_sides(self):
	    "Polygon.sides for w in range(10)"
	    [self.listOfPolygons[w].sides for w in range(10)]

	def time_polygon_centroid(self):
	    "Polygon.centroid for w in range(10)"
	    [self.listOfPolygons[w].centroid for w in range(10)]

	def time_polygon_second_moment(self):
	    "Polygon.second_moment_of_area() for w in range(10)"
	    [self.listOfPolygons[w].second_moment_of_area() for w in range(10)]

	def time_polygon_first_moment(self):
	   "Polygon.first_moment_of_area for w in range(10)"
	   [self.listOfPolygons[w].first_moment_of_area() for w in range(10)]

	def time_polygon_polar_second_moment(self):
	    "Polygon.polar_second_moment_of_area for w in range(10)"
	    [self.listOfPolygons[w].polar_second_moment_of_area() for w in range(10)]

	def time_polygon_section_modulus(self):
	    "Polygon.section_modulus for w in range(10)"
	    [self.listOfPolygons[w].section_modulus() for w in range(10)]

	def time_polygon_is_convex(self):
	    "Polygon.is_convex() for w in range(10)"
	    [self.listOfPolygons[w].is_convex() for w in range(10)]

	def time_polygon_encloses_point(self,Point2=Point(randint(0,10),randint(0,10))):
	   "Polygon.encloses_point for w in range(10)"
	   [self.listOfPolygons[w].encloses_point(Point2) for w in range(10)]

	def time_polygon_arbitrary_point(self):
	    "Polygon.arbitrary_point for w in range(10)"
	    [self.listOfPolygons[w].arbitrary_point() for w in range(10)]

	def time_polygon_cut_section(self):
	    "Polygon.cut_section for w in range(10)"
	    [self.cutListOfPolygons[w].cut_section(self.cutLines[w]) for w in range(10)]

	def time_polygon_distance(self):
	    "Polygon.distance() for w in range(10)"
	    [self.listOfPolygons[w].distance(Point(randint(0,10),randint(0,10))) for w in range(10)]

