# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 13:02:18 2017

@author: caiyuangang
"""


try:
    from osgeo import gdal
except ImportError:
    import gdal

try:
    progress = gdal.TermProgress_nocb
except:
    progress = gdal.TermProgress


import sys
import math
import os


class Raster:
    def __init__(self, filepath):
        gdal.AllRegister()

        dataset = gdal.Open( filepath )
        if dataset is None:
            return None
        self.dataset = dataset

        self.filedir = os.path.dirname(filepath)
        (filename,ext) = os.path.splitext(os.path.basename(filepath))

        self.filename = filename
        self.ext = ext
        self.driver = dataset.GetDriver()
        self.bands = dataset.RasterCount
        self.xsize = dataset.RasterXSize
        self.ysize = dataset.RasterYSize
        self.band_type = dataset.GetRasterBand(1).DataType
        self.nodata = []

        self.projection = dataset.GetProjection()
        self.geotransform = dataset.GetGeoTransform()
        self.ulx = self.geotransform[0]
        self.uly = self.geotransform[3]
        self.lrx = self.ulx + self.geotransform[1] * self.xsize
        self.lry = self.uly + self.geotransform[5] * self.ysize


        ct = dataset.GetRasterBand(1).GetRasterColorTable()
        if ct is not None:
            self.ct = ct.Clone()
        else:
            self.ct = None

        for i in range(1, self.bands + 1):
            self.nodata.append(self.dataset.GetRasterBand(i).GetNoDataValue())

    def band_info(self, band):
        print "***************************************"
        print ("(width, height, dataType) : ( %d,%d,%d)" % (band.XSize,
        band.YSize, band.DataType))
        (minValue, maxValue) = band.ComputeRasterMinMax()
        print "(minValue, MaxValue): ( %lf, %lf) " % (minValue, maxValue)
        print "***************************************"

    def file_info(self):
        print "***************************************"
        print "filepath : " + self.filedir + "/" +self.filename + self.ext
        print "***************************************"
        print ("(width, height, band, dataType) : ( %d,%d,%d,%d)" %(self.xsize,
        self.ysize, self.bands, self.band_type))
        print "Projection: "
        print self.projection
        print "***************************************"
        print "GeoTransform"
        print self.geotransform
        print "No data :"
        print self.nodata
        print "***************************************"


    def getPyramidDataSet(self, level):
        zoom = 2 ** level
        dstX = int(self.xsize / zoom)
        dstY = int(self.ysize / zoom)


        filepath = os.path.join(self.filedir, self.filename + "_" + str(level) + self.ext)
        dst = self.driver.Create(filepath, dstX, dstY,  self.bands, self.band_type)

        #for i in range(1, self.bands + 1):
         #   dst.GetRasterBand(i).Fill(255)

        bandlist = list(range(1, self.bands + 1))

        data = self.dataset.ReadRaster(0, 0, self.xsize, self.ysize, dstX, dstY,
        band_list = bandlist)

        dst.WriteRaster(0, 0, dstX, dstY, data, band_list = bandlist)

        pixesize_x = float(self.lrx - self.ulx) / dstX
        pixesize_y = float(self.lry - self.uly) / dstY


        geotransform = [self.ulx, pixesize_x, 0, self.uly, 0, pixesize_y]
        dst.SetGeoTransform( geotransform )
        if self.ct:
            dst.GetRasterBand(1).SetRasterColorTable(self.ct)

        dst.SetProjection(self.projection)

        if self.nodata is not []:
            for i in range(1, self.bands + 1):
                dst.GetRasterBand(i).SetNoDataValue(self.nodata[i - 1])

        del data
        del dst

        return Raster(filepath)

    def write(self, filepath, dataset):
        pass

    def resize(self, dstX,  dstY):
        pass


if __name__=='__main__':
#	if len(sys.argv) < 6:
#		print " Usage: MapTiler.py MapRoot LonFrom LonTo LatFrom LatTo"
#	else:
#		MapRoot = sys.argv[1]
#		LonFromTo = [float(sys.argv[2]), float(sys.argv[3])]
#		LatFromTo = [float(sys.argv[4]), float(sys.argv[5])]
#		m = MapTiler(MapRoot)
#		m.run(LonFromTo, LatFromTo)
	#example
    raster = Raster("/Users/caiyuangang/work/gujiao/gujiao.tif")
    raster.file_info()
    for i in range(4, 9):
        raster.getPyramidDataSet(i).file_info()

    #raster4 = Raster("/Users/caiyuangang/work/gujiao/gujiao_4.tif")
    #raster4.file_info()
