#!python.exe

import sys
import os
import subprocess

def process(work_root, src, dst, epsg):
	#gdal_translate = os.path.join(self.gdal_root, "gdal_translate")
	srcfile = os.path.join(work_root, src)
	dstfile = os.path.join(work_root, dst)
	if not os.path.exists(dstfile):
		argv = [gdal_translate, "-of", "GTiff", "-co", "TILED=YES", "-co", "BLOCKXSIZE=256", "-co", "BLOCKYSIZE=256", src, dst]
		return subprocess.call(argv)
# =============================================================================

if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "usage: sys.argv[0] work_root src dst"
	else:
		work_root = sys.argv[1]
		src = sys.argv[2]
		dst = sys.argv[3]
		process(work_root, demfile, colorfile)