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
	def __init__(self):
		self.tilesize = 256
		self.tiledriver = "PNG"
		self.tileext = "png"
		self.work_root = ""

	def ProcessFromJson(self, jsonfile):
		import json
		jsonvalues = json.load(file(jsonfile))
		print jsonvalues
		self.work_root = jsonvalues["root"]
		print "work_root:" + self.work_root
		bound_type = jsonvalues["bound"]["type"]
		print bound_type
		if bound_type == "raster":
			raster = drivers["raster"].Create(jsonvalues["bound"]["value"])
			self.minLat, self.minLon, self.maxLat, self.maxLon = raster.LatLonBound()
		else:
			self.minLat = float(jsonvalues["bound"]["value"]["minLat"])
			self.minLon = float(jsonvalues["bound"]["value"]["minLon"])
			self.maxLat = float(jsonvalues["bound"]["value"]["maxLat"])
			self.maxLon = float(jsonvalues["bound"]["value"]["maxLon"])

		self.tilesize = int(jsonvalues["tilesize"])
		self.tiledriver = jsonvalues["tiledriver"]
		self.tileext = jsonvalues["tileext"]
		works = jsonvalues["works"]

		for work in works:
			self.process(work)

	def process(self, work):
		srcfile = os.path.join(self.work_root, work["src"]["value"])
		out_root = os.path.join(self.work_root, work["name"])
		if not os.path.exists(srcfile):
			s = drivers[work["src"]["type"]].Create(work["src"]["root"])
			s.Process(out_root, self.minLon, self.minLat, self.maxLon, self.maxLat)
		
		d = drivers[work['dst']['type']].Create(out_root)
		tiledriver = self.tiledriver
		tileext = self.tileext
	
		if "tiledriver" in work["dst"]:
			tiledriver = work["dst"]["tiledriver"]
		if "tileext" in work["dst"]:
			tileext = work["dst"]["tileext"]
		d.Process(srcfile, self.tilesize, tiledriver, tileext)

	def process_dem(self, dem):
		s = drivers[dem['src']['type']].Create(dem['src']['root'])
		bound = dem['src']['bound']
		s.Process(self.work_root, LonFromTo, LatFromTo)
		dem = os.path.join(self.work_root, "dem.vrt")
		d = drivers[dem['dst']['type']].Create(dem['dst']['root'])
		d.Process(dem, 256, 'GTiff', 'tif')

	def process_color_shade(self, shade):
		s = drivers(dem['src']['type']).Create(shade['src']['root'])
		bound = shade['src']['bound']
		s.Process(self.work_root, LonFromTo, LatFromTo)
		shade = os.path.join(self.work_root, "color_shade.tif")
		d = drivers[shade['dst']['type']].Create(dem['dst']['root'])
		d.Process(dem, 256, 'PNG', 'png')	

	def process_raster(self, raster):
		s = drivers(raster['src']['type']).Create(raster['src']['root'])
		minLon, minLat, maxLon, maxLat = s.LatLonBound()
		s.Process(self.work_root, LonFromTo, LatFromTo)
		shade = os.path.join(self.work_root, "color_shade.tif")
		d = drivers[shade['dst']['type']].Create(dem['dst']['root'])
		d.Process(dem, 256, 'PNG', 'png')	
		d = self.dstDriver.Create(self.dstDataDir)
		d.Process(imagefile, None, None)

	def postProcess(self):
		pass


if __name__=='__main__':
	if len(sys.argv) < 2:
		print " Usage: MapTiler.py work.json"
	else:
		filepath = sys.argv[1]
		m = MapTiler()
		m.ProcessFromJson(filepath)

