#!python.exe

import sys
import os
import subprocess

def process(work_root, src, dst, epsg = None, tilesize = 256):
	#gdalwarp = os.path.join(self.gdal_root, "gdalwarp")
	srcfile = os.path.join(work_root, src)
	dstfile = os.path.join(work_root, dst)
	if os.path.exists(dstfile):
		return

	if epsg is not None:
		subprocess.call(["gdalwarp", "-t_srs " + str(epsg), srcfile, dstfile])
	
	subprocess.call(["gdal_translate", "-of", "GTiff", "-co", "TILED=YES", "-co", "BLOCKXSIZE="+str(tilesize),
		 "-co", "BLOCKYSIZE=" + str(tilesize), srcfile, dstfile])

	subprocess.call(["gdaladdo", "-r", "averge", dstfile])

# =============================================================================

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "usage: sys.argv[0] work_root src dst"
	else:
		work_root = sys.argv[1]
		src = sys.argv[2]
		dst = sys.argv[3]
		process(work_root, src, dst)