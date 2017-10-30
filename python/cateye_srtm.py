# -*- coding: utf-8	-*-
"""
Created	on Mon Oct 09 15:57:09 2017

@author: cyg
"""

import os
import os.path

import basic

def Create(workdir):
	return CateyeSRTM(workdir)

class CateyeSRTM():
	def	__init__(self, workdir):
		self.workdir = workdir
		self.ext = ".zip"
		self.imgfmt	= ".tif"
		self.resolution	= 5.0
		self.tileX = [1, 72]
		self.tileY = [1, 24]
		self.baseurl = (
		"http://srtm.csi.cgiar.org/SRT-ZIP/SRTM_V41/SRTM_Data_GeoTiff/")
		self.name =	'srtm'

	def	getResolution(self):
		return self.resolution

	def	getTilesX(self,	LonFromTo):
		return self._lonToTileX(LonFromTo[0]), self._lonToTileX(LonFromTo[1])

	def	getTilesY(self,	LatFromTo):
		y1,	y2 = self._latToTileY(LatFromTo[0]), self._latToTileY(LatFromTo[1])
		return min(y1, y2),	max(y1,	y2)

	def	_lonToTileX(self, longitude):
		tilex = int((longitude +	180) / self.resolution) + 1

		if tilex > self.tileX[1]:
			tilex = self.tileX[1]
		if tilex < self.tileX[0]:
			tilex = self.tileX[0]

		return tilex

	def	_latToTileY(self, latitude):

		tiley = int((60 - latitude) / self.resolution) +	1
		if tiley > self.tileY[1]:
			tiley = self.tileY[1]
		if tiley < self.tileY[0]:
			tiley = self.tileY[0]

		return tiley

	def	lonlatToTile(self, longitude, latitude):
		tileX =	self._lonToTileX(longitude)
		tileY =	self._latToTileY(latitude)

		return (tileX, tileY)

	def	lonlatToPixel(self,	longitude, latitude):
		tileX =	self._lonToTileX(longitude)
		tileY =	self._latToTileY(latitude)

		pixelX = self._lonToPixelX(longitude)
		pixelY = self._latToPixelY(latitude)

		return (tileX, tileY, pixelX, pixelY)


	def	downloadLonLat(self, lon, lat):
		(x,	y) = (self._lonToTileX(lon), self._latToTileY(lat))
		self.downloadTile(x, y)

	def	downloadTile(self, tileX, tileY):
		filename = "srtm_%02d_%02d"	% (tileX, tileY)
		self.downloadName(filename)

	def	downloadName(self, filename):
		#check if there	exists the directory
		filedir	= os.path.join(self.workdir, filename)
		if not os.path.exists(filedir):
			os.mkdir(filedir)
			srcurl = os.path.join(self.baseurl,	filename + self.ext)
			dstfile	= os.path.join(self.workdir, filename +	self.ext)
			if not os.path.exists(dstfile):
				basic.DownloadFile(srcurl, dstfile)
			basic.DecodeZipfile(dstfile, filedir)
			os.remove(dstfile)
		print filename + " is ok!"

	def	downloadTilesFromTo(self, txmin, txmax,	tymin, tymax):
		imagefiles = []
		for	tx in range(txmin, txmax + 1):
			for	ty in range(tymin,tymax + 1):
				filename = "srtm_%02d_%02d"	% (tx, ty)
				print filename
				self.downloadName(filename)
				imagefile =	os.path.join(self.workdir, filename, filename +	self.imgfmt)
				if os.path.exists(imagefile):
					imagefiles.append(imagefile)
		return imagefiles

	def	downloadFromTo(self, LonFromTo,	LatFromTo):
		txmin, txmax = self.getTilesX(LonFromTo)
		tymin, tymax = self.getTilesY(LatFromTo)
		return self.downloadTilesFrom(txmin, txmax,	tymin, tymax)

	def	getImageFromTiles(self,	txmin, txmax, tymin, tymax):
		print (txmin, txmax, tymin,	tymax)
		return self.downloadTilesFromTo(txmin, txmax, tymin, tymax)

	def	getImage(self, LonFromTo, LatFromTo):
		txmin, txmax = self.getTilesX(LonFromTo)
		tymin, tymax = self.getTilesY(LatFromTo)
		return self.getImageFromTiles(txmin, txmax,	tymin, tymax)

	def	getImageFromAll(self):
		txmin, txmax = self.getTilesX(self.lonFromTo)
		tymin, tymax = self.getTilesY(self.latFromTo)
		print (txmin, txmax, tymin,	tymax)
		self.getImageFromTiles(txmin, txmax, tymin,	tymax)

	def	downloadAll(self):
		self.downloadFromTo(self.lonFromTo,	self.latFromTo)

	def	Process(self, imagefile, lonFromTo,	latFromTo):
		#A.	get	imagefiles
		imagefiles = self.getImage(lonFromTo, latFromTo)
		import gdal_vrtmerge
		argv = ['gdal_vrtmerge.py','-o', imagefile,]
		for	imagefile in imagefiles:
			argv.append(imagefile)
		#print argv
		gdal_vrtmerge.run(argv)

if __name__	== "__main__":
	print "**"

	#srtm =	SRTM("D:/person/srtm")
	#srtm.download(112.5000005,37.5000001)
	#srtm.getImageFromAll()
	#srtm.getImageFromTiles(58,	60,	4, 6)
	#srtm.downloadTilesFromTo(58, 60, 4, 6)
	#srtm.downloadTile(58, 05)
	#srtm.downloadTile(58, 06)
	#srtm.downloadTile(59, 04)
	#srtm.downloadTile(59, 05)
	#srtm.downloadTile(59, 06)
	#srtm.downloadTile(60, 04)
	#srtm.downloadTile(60, 05)
	#srtm.downloadTile(60, 06)
	#srtm.downloadAll()
	#print "success"