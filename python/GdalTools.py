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
	print('You are using "old gen" bindings. gdal2tiles needs "new gen" bindings.')
	sys.exit(1)


def process(argv):
	return subprocess.call(argv)

def gdalwarp(epsg, src, dst):
	argv = ["gdalwarp", "-t_srs " + str(epsg), src, dst]
	return subprocess.call(argv)

def translate(src, dst):
	argv = ["gdal_translate", "-of GTiff", "-co TILED=YES", src, dst]
	return subprocess.call(argv)

def build_pyramid(src, _from, _to):
	argv = ["gdaladdo", "-r average", src]
	for i in range(_from, _to):
		argv.append(str(i* 2))
	print argv
	return subprocess.call(argv)


