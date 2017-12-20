#!python.exe

import sys
import os
import subprocess

def dem2color(work_root, src, dst):
	#gdaldem = os.path.join(gdal_root, "gdaldem")
	srcfile = os.path.join(work_root, src)
	dstfile = os.path.join(work_root, dst)
	argv = ["gdaldem","color-relief", srcfile, "terrain.txt", dstfile]
	return subprocess.call(argv)
# =============================================================================

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "usage: sys.argv[0] gdal_root demfile color file"
	else:
		work_root = sys.argv[1]
		demfile = sys.argv[2]
		colorfile = sys.argv[3]
		dem2color(work_root, demfile, colorfile)




