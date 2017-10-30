# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 11:42:01 2017

@author: cyg
"""

def Create(workdir):
    return CateyeMercator(workdir)

class CateyeMercator():
    def __init__(self,  workdir):
        self.workdir = workdir


    def Process(self, imagefile, LonFromTo = None, LatFromTo = None):
        if imagefile is not None:
            argv = ["gdal2tiles.py", "--profile=mercator", "-z 0-10", imagefile,
                    self.workdir]
            print argv
            self.ProcessArgv(argv)

    def ProcessArgv(self, argv):
        import gdal2tiles
        gdal2tiles.run(argv)




