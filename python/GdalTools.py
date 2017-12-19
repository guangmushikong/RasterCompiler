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

GDAL_ROOT = ""

def process(argv):
	return subprocess.call(argv)

def warp(epsg, src, dst):
	gdalwarp = os.path.join(GDAL_ROOT, "gdalwarp")
	argv = [gdalwarp, "-t_srs " + str(epsg), src, dst]
	return subprocess.call(argv)

def translate(src, dst):
	gdal_translate = os.path.join(GDAL_ROOT, "gdal_translate")
	argv = [gdal_translate, "-of GTiff", "-co TILED=YES", src, dst]
	return subprocess.call(argv)

def build_pyramid(src, _from, _to):
	argv = ["gdaladdo", "-r average", src]
	for i in range(_from, _to):
		argv.append(str(i* 2))
	print argv
	return subprocess.call(argv)

def dem_color(src, dst):
	gdaldem = os.path.join(GDAL_ROOT, "gdaldem")
	argv = [gdaldem,'color-relief', srcfile, 'terrain.txt', dstfile]
	return subprocess.call(argv)

def dem_hillshade(srcfile, dstfile):
	gdaldem = os.path.join(GDAL_ROOT, "gdaldem")
	argv = [gdaldem, "hillshade", srcfile, dstfile, '-z', '5.0', 
	'-s', '111120.0','-az', '90.0', '-alt', '90.0']
	return subprocess.call(argv)

def hsv_merge(colorfile, shadefile, mergefile):
	argv = ['python','hsv_merge.py', colorfile, shadefile, mergefile]
	return subprocess.call(argv)
