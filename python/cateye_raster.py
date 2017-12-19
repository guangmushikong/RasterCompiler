# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 13:02:18 2017

@author: caiyuangang
"""


try:
	from osgeo import gdal
	from osgeo import osr
except ImportError:
	import gdal

try:
	progress = gdal.TermProgress_nocb
except:
	progress = gdal.TermProgress


import sys
import math
import os

def Create(filepath):
	return CateyeRaster(filepath)

class CateyeRaster:
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
		self.lrx = self.ulx + self.geotransform[1] * self.xsize + self.geotransform[2] * self.ysize
		self.lry = self.uly + self.geotransform[4] * self.xsize + self.geotransform[5] * self.ysize

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

	def copy_info(self, dst):
		#copy projection & geo transform
		dst.SetGeoTransform(self.geotransform )
		dst.SetProjection(self.projection)

	def addBand(self, bandfile, dstfile):
		band = gdal.Open(bandfile, gdal.GA_ReadOnly)
		xsize = band.RasterXSize
		ysize = band.RasterYSize
		_band = band.RasterCount

		if not (xsize == self.xsize and ysize == self.ysize):
			print "rgb file and alpha file do not have the same size "
			return

		dst_drv = gdal.GetDriverByName("GTiff")
		dst = dst_drv.Create(dstfile, self.xsize, self.ysize, self.bands + _band)

		data = self.dataset.ReadRaster(0, 0, xsize, ysize, xsize, ysize)


		banddata = band.ReadRaster(0, 0, xsize, ysize, xsize, ysize)

		# Use the ReadRaster result directly in tiles ('nearest neighbour' query)
		dst.WriteRaster(0, 0, xsize, ysize, data, band_list=list(range(1, self.bands + 1)))
		dst.WriteRaster(0, 0, xsize, ysize, banddata,
						band_list=list(range(self.bands + 1, self.bands + _band + 1)))

		dst.SetGeoTransform(self.geotransform)
		dst.SetProjection(self.projection)
		del dst

	def repoject(self, dst_epsg, dstfile):
		dst_drv = gdal.GetDriverByName("GTiff")
		dst = dst_drv.Create(dstfile, self.xsize, self.ysize, self.bands)

		dst_srs = osr.SpatialReference()
		dst_srs.ImportFromEPSG(dst_epsg)
		dst_srs_wkt = dst_srs.ExportToWkt()
		dst = gdal.AutoCreateWarpedVRT(self.dataset, self.projection, dst_srs_wkt)
		del dst

	def PixelToMeters(self, px, py):
		trans = self.geotransform
		mx = trans[0] + px * trans[1] + py * trans[2]
		my = trans[3] + px * trans[4] + py * trans[5]
		return mx, my

	def	MetersToLonLat(self, mx, my):
		prosrs = osr.SpatialReference()
		prosrs.ImportFromWkt(self.projection)
		geosrs = prosrs.CloneGeogCS()
		ct = osr.CoordinateTransformation(prosrs, geosrs)
		coords = ct.TransformPoint(mx, my)
		return coords[0], coords[1]

	def LonLatToMeters(self, lon, lat):
		prosrs = osr.SpatialReference()
		prosrs.ImportFromWkt(self.projection)
		geosrs = prosrs.CloneGeogCS()
		ct = osr.CoordinateTransformation(geosrs,prosrs)
		coords = ct.TransformPoint(lon, lat)
		return coords[0], coords[1]

	def MetersBound(self):
		#ulx uly
		return self.ulx, self.uly, self.lrx, self.lry

	def LatLonBound(self):
		minx, miny, maxx, maxy = self.MetersBound()
		minLon, minLat = self.MetersToLonLat(minx, miny)
		maxLon, maxLat = self.MetersToLonLat(maxx, maxy)
		return minLon, minLat, maxLon, maxLat

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

	def Process(self, out_root, minLon, minLat, maxLon, maxLat, minZoom, maxZoom):
		pass

	def write(self, filepath, dataset):
		pass

	def resize(self, dstX,  dstY):
		pass
