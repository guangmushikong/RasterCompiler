# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 12:54:58 2017

@author: cyg
"""
import sys
import os
import subprocess
try:
	from osgeo import gdal
	from osgeo import osr
except:
	import gdal
	sys.exit(1)


def Create(gdal_root):
	return CateyeGdal(gdal_root)

class CateyeGdal():
	def __init__(self, gdal_root):
		self.gdal_root = gdal_root

	def Process(self, work_root, command, params):
		#os.chdir(self.gdal_root)
		argv = ["python", command, work_root]
		for p in params:
			argv.append(p)
		return subprocess.call(argv)

	def warp(self, src, dst, epsg):
		gdalwarp = os.path.join(self.gdal_root, "gdalwarp")
		argv = [gdalwarp, "-t_srs " + str(epsg), src, dst]
		return subprocess.call(argv)

	def translate(self, src, dst):
		gdal_translate = os.path.join(self.gdal_root, "gdal_translate")
		argv = [gdal_translate, "-of", "GTiff", "-co", "TILED=YES", "-co", "BLOCKXSIZE=256", "-co", "BLOCKYSIZE=256", src, dst]
		return subprocess.call(argv)

	def build_pyramid(self, src, _from, _to):
		argv = ["gdaladdo", "-r average", src]
		for i in range(_from, _to):
			argv.append(str(i* 2))
		print argv
		return subprocess.call(argv)

	def dem2color(self, src, dst):
		gdaldem = os.path.join(self.gdal_root, "gdaldem")
		argv = [gdaldem,'color-relief', srcfile, 'terrain.txt', dstfile]
		return subprocess.call(argv)

	def dem2shade(srcfile, dstfile):
		gdaldem = os.path.join(self.gdal_root, "gdaldem")
		argv = [gdaldem, "hillshade", srcfile, dstfile, '-z', '5.0', 
		'-s', '111120.0','-az', '90.0', '-alt', '90.0']
		return subprocess.call(argv)

	def hsv_merge(self, colorfile, shadefile, mergefile):
		argv = ['python','hsv_merge.py', colorfile, shadefile, mergefile]
		return subprocess.call(argv)
