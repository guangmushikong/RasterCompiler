# -*- coding: utf-8 -*-
"""
/*
* \file 		: GoogleImage.h
* \brief
*
* Project		:
* Purpose		:
* Author		: MagicPixel	cyg1030@foxmail.com
* Created		: 2017-10-16 12:11
* Modified by	:
*/
"""

import os
import gdal2tiles
import basic

class GoogleImageDownLoad:
    def __init__(self, output):
        self.baseurl = "http://www.google.cn/maps/vt?lyrs=s@747&gl=cn"
        self.output = output
        self.mercator = gdal2tiles.GlobalMercator()

    def progressbar(self, complete = 0.0):
        gdal2tiles.gdal.TermProgress_nocb(complete)

    def DownLoadFromTile(self, tx_min, tx_max, ty_min, ty_max, tz):
        print "download tiles from zoom :" + str(tz)
        tcount = (1 + abs(tx_max - tx_min)) * (1 + abs(ty_max - ty_min))
        #print tcount
        ti = 0
        for ty in range(ty_max, ty_min - 1, -1): #range(tminy, tmaxy+1):
            for tx in range(tx_min, tx_max + 1):
                ti += 1
                gx, gy = self.mercator.GoogleTile(tx, ty, tz)
                srcfile = self.baseurl + "&x=" + str(gx) + "&y=" + str(gy) + "&z=" + str(tz)
                dstfile = os.path.join(self.output, str(tz), str(tx), "%s.jpg" % ty)

                basic.DownloadFile(srcfile, dstfile)
                self.progressbar( ti / float(tcount) )
    				# Create directories for the tile
        print "**********************************************"

    def DownLoadFromLonLat(self, LonFromTo, LatFromTo, ZoomFromTo):
        lon_min = LonFromTo[0]
        lon_max = LonFromTo[1]
        lat_min = LatFromTo[0]
        lat_max = LatFromTo[1]
        mx_min, my_min = self.mercator.LatLonToMeters(lat_min, lon_min)
        mx_max, my_max = self.mercator.LatLonToMeters(lat_max, lon_max)

        for tz in range(ZoomFromTo[0], ZoomFromTo[1]):
            tx_min, ty_min = self.mercator.MetersToTile(mx_min, my_min, tz)
            tx_max, ty_max = self.mercator.MetersToTile(mx_max, my_max, tz)
            # crop tiles extending world limits (+-180,+-90)
            tx_min, ty_min = max(0, tx_min), max(0, ty_min)
            tx_max, ty_max = min(2**tz-1, tx_max), min(2**tz-1, ty_max)
            self.DownLoadFromTile(tx_min, tx_max, ty_min, ty_max, tz)

import sys
if __name__=='__main__':
    if len(sys.argv) < 8:
        print " Usage: GoogleImageDownLoad.py output LonFrom LonTo LatFrom LatTo ZoomFrom ZoomTo"
    else:
        Output = sys.argv[1]
        LonFromTo = [float(sys.argv[2]), float(sys.argv[3])]
        LatFromTo = [float(sys.argv[4]), float(sys.argv[5])]
        ZoomFromTo = [float(sys.argv[6]), float(sys.argv[7])]
        d = GoogleImageDownLoad(Output)
        d.DownLoadFromLonLat(LonFromTo, LatFromTo, ZoomFromTo)
    #example
    #download = GoogleImageDownLoad("D:/person/work/bejing/google")
    #download.DownLoadFromLonLat([112.5000005 - 5, 112.5000005 + 5.0],[37.5000001 - 5.0, 37.5000001 + 5.0],[12, 17])