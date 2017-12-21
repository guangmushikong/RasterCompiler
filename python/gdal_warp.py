#!python.exe

import sys
import os
import subprocess

def process(work_root, src, dst, epsg):
	srcfile = os.path.join(work_root, src)
	dstfile = os.path.join(work_root, dst)
	if not os.path.exists(dstfile):
		argv = ["gdalwarp", "-t_srs " + str(epsg), src, dst]
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