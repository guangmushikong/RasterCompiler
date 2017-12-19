# -*- coding: utf-8 -*-
"""
/*
* \file 		: cateye_googlemap.py
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

def Create(workdir):
	return CateyeMercator(workdir)

class CateyeGoogleMap():
	def __init__(self, workdir):
		self.baseurl = "http://www.google.cn/maps/vt?lyrs=s@747&gl=cn"
		self.workdir = workdir
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
				dstfile = os.path.join(self.workdir, str(tz), str(tx), "%s.jpg" % ty)

				basic.DownloadFile1(srcfile, dstfile)
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

	def Process(self, out_root, minLon, minLat, maxLon, maxLat, minZoom, maxZoom):
		self.workdir = out_root
		self.DownLoadFromLonLat([minLon, maxLon], [minLat, maxLat], [minZoom, maxZoom])
