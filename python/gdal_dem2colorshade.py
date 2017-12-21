#!python.exe

import sys
import os
import subprocess

def dem2colorshade(work_root, src, dst):
	#gdaldem = os.path.join(gdal_root, "gdaldem")
	subprocess.call(["python", "gdal_dem2color.py", work_root, src, "color.tif"])
	subprocess.call(["python", "gdal_dem2shade.py", work_root, src, "shade.tif"])
	subprocess.call(["python", "gdal_hsv_merge.py", work_root, "color.tif", "shade.tif", dst])

# =============================================================================

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "usage: sys.argv[0] work_root demfile demcolorshade file"
	else:
		work_root = sys.argv[1]
		demfile = sys.argv[2]
		colorshadefile = sys.argv[3]
		dem2colorshade(work_root, demfile, colorshadefile)




