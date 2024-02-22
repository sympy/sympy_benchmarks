import sympy as sp
from sympy import Interval,S,Reals,Union,imageset
from sympy.abc import x
"""
list of benchmarking set properties:
1)set.boundary
2)set.closure
3)set.inf
4)set.interior
5)set.is_closed
6)set.is_open
7)set.kind
8)set.measure
9)set.sup
"""
class TimeSetProperties:
    def setup(self):
        Interval(0,1)
    def time_boundry(self):
        Interval(0,1,True,False).boundary
    def time_closure(self):
        Interval(0,1,True,False).closure
    def time_inf(self):
        Interval(0,1).inf  
    def time_interior(self):
        Interval(0,1).interior
    def time_is_closed(self):
        Interval(0,1).is_closed  
    def time_is_open(self):
        S.Reals.is_open   
    def time_kind(self):
        Interval(0,1).kind 
    def time_measure(self):
        Union(Interval(-1,2),Interval(4,5)).measure  
    def time_sup(self):
        Union(Interval(0,1),Interval(2,3)).sup             
"""
list of benchmarking set functions:
1)set.complement()
2)set.contains()
3)set.intersect()/set.intersection()-> as intersection() is alias  intersect().
4)set.is_disjoint()/set.isdisjoint()->as isdisjoint() is alias is_disjoint().
5)set.is_proper_subset()
6)set.is_proper_superset()
7)set.is_subset()/set.issubset()->as issubset() is alias is_subset().
8)set.is_superset()/set.issuperset()->as issuperset() is alias is_superset().
9)set.powerset()
10)set.symmetric_difference()
11)set.union()
12)imageset()
"""
class TimeSetFunctions:
    def  time_complement(self):
        Interval(0,1).complement(S.UniversalSet) 
    def time_contains(self):
        Interval(0,1).contains(0.5)
    def time_intersect(self):
        Interval(0,1).intersect(Interval(1,2))   
    def time_is_disjoint(self):
        Interval(0, 2).is_disjoint(Interval(3, 4)) 
    def time_is_proper_subset(self):
        Interval(0, 1).is_proper_subset(Interval(0, 0.5))
    def time_is_proper_superset(self):
        Interval(0,1).is_proper_superset(Interval(-1,2))
    def time_is_subset(self):
        Interval(0,1).is_subset(Interval(0,1))
    def time_is_superset(self):
        Interval(0,1).is_superset(Interval(-2,4))
    def time_powerset(self):
        Interval(0,1).powerset()   
    def time_symmetric_difference(self):
        Interval(0,1).symmetric_difference(S.Reals)   
    def time_union(self):
        Interval(0,1).union(Interval(4,5))    
    def time_imageset(self):
        imageset(x, 2*x, Interval(0, 2))    

                                     




