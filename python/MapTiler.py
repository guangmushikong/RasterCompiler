# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:31:20 2017

@author: cyg
"""

import os
import sys
import basic

drivers = basic.LoadEngine()

print drivers

class MapTiler():
	def __init__(self, work_root, strSrc = 'cateye_srtm', strDst = 'cateye_mercator'):
		self.srcDriver = drivers[strSrc]
		self.dstDriver = drivers[strDst]
		self.work_root = work_root
		self.srcDataDir = os.path.join(work_root, strSrc)
		if not os.path.exists(self.srcDataDir):
			os.mkdir(self.srcDataDir)
		self.dstDataDir = os.path.join(work_root, strDst)
		if not os.path.exists(self.dstDataDir):
			os.mkdir(self.dstDataDir)


	def run(self, LonFromTo, LatFromTo):
		 s = self.srcDriver.Create(self.srcDataDir)
		 d = self.dstDriver.Create(self.dstDataDir)
		 imagefile = os.path.join(self.work_root, "merge_color.vrt")
		 s.Process(imagefile, LonFromTo, LatFromTo)
		 #d.Process(imagefile, LonFromTo, LatFromTo)

	def postProcess(self):
		pass


if __name__=='__main__':
	if len(sys.argv) < 6:
		print " Usage: MapTiler.py MapRoot LonFrom LonTo LatFrom LatTo"
	else:
		MapRoot = sys.argv[1]
		LonFromTo = [float(sys.argv[2]), float(sys.argv[3])]
		LatFromTo = [float(sys.argv[4]), float(sys.argv[5])]
		m = MapTiler(MapRoot)
		m.run(LonFromTo, LatFromTo)
	#example
	maptiler = MapTiler("D:/person/work")
	maptiler.run([-180, 180], [-60, 60])
	#maptiler.run([112.5000005 - 5, 112.5000005 + 5.0], [37.5000001 - 5.0, 37.5000001 + 5.0])
