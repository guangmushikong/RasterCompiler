# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 11:42:01 2017

@author: cyg
"""

import gdal2tiles

def Create(workdir):
	return CateyeMercator(workdir)

class CateyeMercator():
	def __init__(self, workdir):
		self.workdir = workdir

	def Process(self, imagefile, tilesize, tiledriver, tileext):
		#get the resolution of the imagefile
		if imagefile is not None:
			argv = ["gdal2tiles.py", "--profile=mercator", imagefile, self.workdir]
			print argv
			p = gdal2tiles.GDAL2Tiles(argv[1:])
			p.set_format(tilesize, tiledriver, tileext)
			p.process()
			#self.ProcessArgv(argv)

	def ProcessArgv(self, argv):
		gdal2tiles.run(argv)




