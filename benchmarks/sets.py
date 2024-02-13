import sympy as sp
from sympy import Interval,S,Reals
"""
list of benchmarking set properties:
1)set.boundary
2)set.closure
3)set.inf
4)set.interior
5)set.is_closed
6)set.is_open
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
"""
list of benchmarking set functions:
1)set.complement()
2)set.contains()
3)set.intersect()/set.intersection()-> as intersection() is alias for intersect().
4)set.is_disjoint()
5)
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


