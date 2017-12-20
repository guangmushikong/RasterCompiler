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

	def ProcessFromJson(self, jsonfile):
		import json
		jsonvalues = json.load(file(jsonfile))
		
		self.root = jsonvalues["root"]
		
		bound_type = jsonvalues["bound"]["type"]
		
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

	def work_done(self, work):
		print self.root["work"]
		tilemapresource = os.path.join(self.root["work"], work["name"], "tilemapresource.xml")
		if os.path.exists(tilemapresource):
			return True 
		return False

	def process(self, work):
		if self.work_done(work):
			return
		
		srcfile = os.path.join(self.root["work"], work["src"]["value"])
		print srcfile
		if not os.path.exists(srcfile):
			datatype = work["src"]["type"]
			s = drivers[datatype].Create(self.root[datatype])
			if "commands" in work["src"]:
				commands =  work["src"]["commands"]
				for command in commands:
					print command
					s.Process(self.root["work"], command["command"], command["params"])
			else:	
				s.Process(self.work_root, self.minLon, self.minLat, self.maxLon, self.maxLat)
		
		out_root = os.path.join(self.root["work"], work["name"])	
		d = drivers[work['dst']['type']].Create(out_root)
		tiledriver = self.tiledriver
		tileext = self.tileext
	
		if "tiledriver" in work["dst"]:
			tiledriver = work["dst"]["tiledriver"]
		if "tileext" in work["dst"]:
			tileext = work["dst"]["tileext"]
		d.Process(srcfile, self.tilesize, tiledriver, tileext)

	def process_dem(self, dem):
		s = drivers[dem["src"]["type"]].Create(dem["src"]["root"])
		s.Process(self.work_root, self.minLon, self.minLat, self.maxLon, self.maxLat)
		dem = os.path.join(self.work_root, "dem.vrt")
		d = drivers[dem["dst"]["type"]].Create(dem["dst"]["root"])
		d.Process(dem, 256, 'GTiff', 'tif')

	def process_color_shade(self, shade):
		s = drivers[shade["src"]["type"]].Create(shade["src"]["root"])
		s.Process(self.work_root, self.minLon, self.minLat, self.maxLon, self.maxLat)
		shade = os.path.join(self.work_root, "color_shade.tif")
		d = drivers[shade["dst"]["type"]].Create(shade["dst"]["root"])
		d.Process(shade, 256, 'PNG', 'png')	

	def process_raster(self, raster):
		d = drivers[raster["dst"]["type"]].Create(raster["dst"]["root"])
		d.Process(raster["src"]["root"], self.tilesize, self.tiledriver, self.tileext)

	def postProcess(self):
		pass


if __name__=='__main__':
	if len(sys.argv) < 2:
		print " Usage: MapTiler.py work.json"
	else:
		filepath = sys.argv[1]
		m = MapTiler()
		m.ProcessFromJson(filepath)

