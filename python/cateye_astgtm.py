# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 14:39:40 2017

@author: cyg
"""

import os
import os.path

import basic
try:
	from osgeo import gdal
	from osgeo import osr
except:
	import gdal
	print('You are using "old gen" bindings. gdal2tiles needs "new gen" bindings.')
	sys.exit(1)

from selenium import webdriver
#from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import Select
import time


def Create(workdir):
	return CateyeASTGTM(workdir)

class CateyeASTGTM:
	def __init__(self, workdir):
		self.workdir = workdir
		self.ext = ".zip"
		self.imgfmt	= ".img"
		self.lonfromto = [-180, 180]
		self.latfromto = [-80, 84]
		self.resolution	= 1.0
		self.baseurl = "http://www.gscloud.cn/sources/download/310/"
		self.outputfile = os.path.join(workdir, "astgtm.txt")

		self.driver = webdriver.Chrome()#chrome_options=options)
		#time.sleep(1)
		self.driver.maximize_window()  # 最大化浏览器
		self.driver.implicitly_wait(8) # 设置隐式时间等待
		self.driver.get(self.baseurl)
		#self.driver.find_element_by_xpath("//input[@class='nav_r_txt']").click()
		usename = self.driver.find_element_by_id("userid")
		usename.send_keys("cyg1030@foxmail.com")
		password = self.driver.find_element_by_id("password")
		password.send_keys("1030king1030")
		button = self.driver.find_element_by_xpath("//input[@type='submit']")
		button.click()

	def progressbar(self, complete = 0.0):
		gdal.TermProgress_nocb(complete)

	def lonlatToTile(self, lon, lat):
		tileX =	int(lon / self.resolution)
		tileY =	int(lat / self.resolution)
		return tileX, tileY

	def get_name(self, tx, ty):
		strLon = " "
		strLat = " "
		if tx < 0:
			strLon = "W"
		else:
			strLon = "E"
		if ty < 0:
			strLat = "S"
		else:
			strLat = "N"
		return "ASTGTM_%s%02d%s%03d"  % (strLat, abs(ty), strLon, abs(tx))

	def DownloadTileBound(self, tx_min, tx_max, ty_min, ty_max):
		print "download tiles "
		tcount = (1 + abs(tx_max - tx_min)) * (1 + abs(ty_max - ty_min))
		#print tcount
		ti = 0
		fp = open(self.outputfile, "w")
		for ty in range(ty_max, ty_min - 1, -1): #range(tminy, tmaxy+1):
			for tx in range(tx_min, tx_max + 1):
				ti += 1
				filename = self.get_name(tx, ty)
				srcfile = os.path.join(self.baseurl,  filename + "/bj")
				dstfile = os.path.join(self.workdir, filename + ".zip")
				print srcfile
				print dstfile
				#srcfile = "http://bjdl.gscloud.cn/download?sid=HztPz_YIoItX_0Ddxwg8tUbFbyOMLWAQzRYRHN4L7dg65mr8rMPbcQYX3Fp61zjtCn4hitcIbrnVl7cmC64C8mupzUl6W1uQbVrQb9LVL2EPBdGriXQu30nZYWvWxWDNe-w"
				#print response.headers

				#import sys
				#from selenium import webdriver
				#driver = webdriver.Chrome()
				#driver.maximize_window()  # 最大化浏览器
				#driver.implicitly_wait(8) # 设置隐式时间等待
				#print self.driver.get_cookie(srcfile)

				#print self.driver.session_id
				self.driver.get(srcfile)
				fp.write(self.driver.current_url + "/n")
				#print self.driver.current_url
				time.sleep(20)


				#with open(dstfile, 'wb') as of:
					#of.write(self.driver.get(srcfile))
				#time.sleep(20)
				#break
				#driver.quit()
				#basic.DownloadFile1(srcfile, dstfile)
				self.progressbar( ti / float(tcount) )
		fp.close()
		print "**********************************************"

	def DownloadLonLatBound(self, LonFromTo, LatFromTo):
		tx_min, ty_min = self.lonlatToTile(LonFromTo[0], LatFromTo[0])
		tx_max, ty_max = self.lonlatToTile(LonFromTo[1], LatFromTo[1])
		self.DownloadTileBound(tx_min, tx_max, ty_min, ty_max)

	def DownloadFromTo(self, LonFromTo,	LatFromTo):
		txmin, txmax = self.getTilesX(LonFromTo)
		tymin, tymax = self.getTilesY(LatFromTo)
		return self.downloadTilesFrom(txmin, txmax,	tymin, tymax)

import sys
if __name__=='__main__':
	if len(sys.argv) < 6:
		print " Usage: cateye_astgtm.py output LonFrom LonTo LatFrom LatTo"
	else:
		Output = sys.argv[1]
		LonFromTo = [float(sys.argv[2]), float(sys.argv[3])]
		LatFromTo = [float(sys.argv[4]), float(sys.argv[5])]
		s = CateyeASTGTM(Output)
		s.DownloadLonLatBound(LonFromTo, LatFromTo)
	#example
	download = CateyeASTGTM("D:/person/work/bejing")
	download.DownloadLonLatBound([112.5000005 - 5, 112.5000005 + 5.0],
								[37.5000001 - 5.0, 37.5000001 + 5.0])