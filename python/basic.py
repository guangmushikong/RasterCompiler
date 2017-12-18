# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 11:02:12 2017

@author: cyg
"""

import os
import os.path
import requests
import threading


def FileStreamIO(start, end, url, filename):
	headers = {'Range': 'bytes=%d-%d' % (start, end)}
	r = requests.get(url, headers = headers, stream = True)
	# 写入文件对应位置
	with open(filename, "r+b") as fp:
		fp.seek(start)
		#var = fp.tell()
		#print var
		fp.write(r.content)


def DownloadFile1(url, dst):
	print 'downfile'
	response = requests.get(url, stream=True)
	print response
	status = response.status_code
	if status == 200:
		#total_size = int(response.headers['Content-Length'])
		with open(dst, 'wb') as of:
			for chunk in response.iter_content(chunk_size=1024):
				if chunk:
					of.write(chunk)

def DownloadFile(url, dst, num_thread = 4):
	if os.path.exists(dst):
		return
	if not os.path.exists(os.path.dirname(dst)):
		os.makedirs(os.path.dirname(dst))

	r = requests.head(url)
	try:
		#file_name = url.split('/')[-1]
		# Content-Length获得文件主体的大小，当http服务器使用Connection:keep-alive时，不支持Content-Length
		file_size = int(r.headers['content-length'])
	except:
		print(u"检查URL，或不支持对线程下载")
		return


	#  创建一个和要下载文件一样大小的文件
	fp = open(dst, "wb")
	fp.truncate(file_size)
	fp.close()

	# 启动多线程写文件
	thread_list = []    #线程存放列表
	part = file_size // num_thread  # 如果不能整除，最后一块应该多几个字节
	for i in range(num_thread):
		start = part * i
		if i == num_thread - 1:   # 最后一块
			end = file_size
		else:
			end = start + part

		t = threading.Thread(
			target = FileStreamIO,
			kwargs={'start': start, 'end': end, 'url': url, 'filename': dst})

		t.setDaemon(True)
		thread_list.append(t)


	for t in thread_list:
		t.start()

	for t in thread_list:
		t.join()

def DecodeZipfile(srcfile, dstdir):
	import zipfile
	try:
		files = zipfile.ZipFile(srcfile,'r')
		for filename in files.namelist():
			data = files.read(filename)
			file = open(os.path.join(dstdir,filename), 'w+b')
			file.write(data)
			file.close()
		files.close()
	except:
		print "cannot Decode the zip file: " + srcfile
		return

def LoadEngine():
	import re
	DataDriver = {}
	#get all the py file
	files = os.listdir(os.getcwd())

	for filei in files:
		match =  re.match(re.compile('cateye_(.*?).py'), filei)
		if match is not None:

			drvier_name = "cateye_" + match.group(1)
			drvier_module = __import__(drvier_name)
			DataDriver[match.group(1)] = drvier_module

	return DataDriver
