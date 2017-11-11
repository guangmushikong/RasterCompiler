# -*- coding: utf-8 -*-
"""
/*
* \file 		: bound.py
* \brief        : 
*
* Project		:
* Purpose		: 
* Author		: MagicPixel	cyg1030@foxmail.com
* Created		: 2017-11-11 12:11
* Modified by	:
*/
"""

class Bound:
    """			
    /**!brief 	initialize a Bound obj

	\param[in]	x_min 			minimum value in x coordinate 
	\param[in]	y_min 			minimum value in y coordinate
	\param[in]	x_max		    maximum value in x coordinate
	\param[in]	y_max 		    maximum value in y coordinate

	\return 	Bound
	*/
    """
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    """			
    /**!brief 	compare bound a and bound b

	\return 	a == b
	*/
    """
    def __eq__(self, obj):
        return ( int(self.x_min) == int(obj.x_min) and
                 int(self.x_max) == int(obj.x_max) and
                 int(self.y_min) == int(obj.y_min) and
                 int(self.y_max) == int(obj.y_max))

    """			
    /**!brief 	compare bound a and bound b

	\return 	a > b
	*/
    """
    def __gt__(self, obj):
        return self.contain(obj)

    """			
    /**!brief 	compare bound a and bound b

	\return 	a < b
	*/
    """
    def __lt__(self, obj):
        return obj.contain(self)

    """			
    /**!brief 	see union

	\return 	Bound
	*/
    """
    def __add__(self, obj):
        return self.union(obj)

    """
    /**!brief   see intersection

    \return     Bound
    """
    def __sub__(self, obj):
        return self.intersection(obj)

    def contain(self, obj):
        return ( self.x_min < obj.x_min and
                 self.x_max > obj.x_max and
                 self.y_min < obj.y_min and
                 self.y_max > obj.y_max)

    def area(self):
        return (self.x_max - self.x_min) * (self.y_max - self.y_min)

    def union(self, obj):
        x_min = min(self.x_min, obj.x_min)
        x_max = max(self.x_max, obj.x_max)
        y_min = min(self.y_min, obj.y_min)
        y_max = max(self.y_max, obj.y_max)
        return Bound(x_min, x_max, y_min, y_max)

    def intersection(self, obj):
        x_min = max(self.x_min, obj.x_min)
        x_max = min(self.x_max, obj.x_max)
        y_min = max(self.y_min, obj.y_min)
        y_max = min(self.y_max, obj.y_max)
        return Bound(x_min, x_max, y_min, y_max)


