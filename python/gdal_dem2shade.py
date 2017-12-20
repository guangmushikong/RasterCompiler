#!python.exe

import sys
import os
import subprocess

def dem2shade(work_root, src, dst):
	#gdaldem = os.path.join(gdal_root, "gdaldem")
	srcfile = os.path.join(work_root, src)
	dstfile = os.path.join(work_root, dst)
	argv = ["gdaldem", "hillshade", srcfile, dstfile, '-z', '5.0', 
	'-s', '111120.0','-az', '90.0', '-alt', '90.0']
	return subprocess.call(argv)
# =============================================================================

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "usage: sys.argv[0]  work_root demfile shadefile"
	else:
		#gdal_root = sys.argv[1]
		work_root = sys.argv[1]
		demfile = sys.argv[2]
		shadefile = sys.argv[3]
		dem2shade(work_root, demfile, shadefile)




