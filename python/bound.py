# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:02:12 2017

@author: cyg
"""

class Bound:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
    
    def __eq__(self, ohter):
        return ( int(self.x_min) == int(other.x_min) and
                 int(self.x_max) == int(other.x_max) and
                 int(self.y_min) == int(other.y_min) and
                 int(self.y_max) == int(ohter.y_max))

    def contain(self, other):
        return ( self.x_min < other.x_min and 
                 self.x_max > other.x_max and
                 self.y_min < other.y_min and
                 self.y_max > other.y_max)
    
    