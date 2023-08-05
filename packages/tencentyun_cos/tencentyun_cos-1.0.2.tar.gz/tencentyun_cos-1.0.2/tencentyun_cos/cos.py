# -*- coding: utf-8 -*-

import os.path
import time
import json
import sys
import string
import hashlib
import requests
import urllib
from tencentyun_cos import conf
from .auth import Auth

class Cos(object):

	def __init__(self, appid=conf.APPID, secret_id=conf.SECRET_ID, secret_key=conf.SECRET_KEY):
		self.COS_FILE_NOT_EXISTS = -1
		self.COS_NETWORK_ERROR = -2
		self.COS_PARAMS_ERROR = -3
		self.COS_ILLEGAL_SLICE_SIZE_ERROR = -4

		self.EXPIRED_SECONDS = 2592000
		self._secret_id,self._secret_key = secret_id,secret_key
		conf.set_app_info(appid, secret_id, secret_key)

	def generate_res_url(self, bucket, dstpath):
		app_info = conf.get_app_info()
		return app_info['end_point'] + str(app_info['appid']) + '/' + bucket + '/' + dstpath

	def sendRequest(self, method, url, **args):
		r = {}
		try:
			if method.upper() == 'POST' :
				r = requests.post(url, **args)
			else :
				r = requests.get(url, **args)
			ret = r.json()
		except Exception as e:
			if r:
				return {'httpcode':r.status_code, 'code':self.COS_NETWORK_ERROR, 'message':str(e), 'data':{}}
			else:
				return {'httpcode':0, 'code':self.COS_NETWORK_ERROR, 'message':str(e), 'data':{}}
		if 'code' in ret:
			if 0 == ret['code']:
				ret['httpcode'] = r.status_code
				return ret
			else:
				return { 'httpcode':r.status_code, 'code':ret['code'], 'message':ret['message'], 'data':{} }
		else:
			return {'httpcode':r.status_code, 'code':self.COS_NETWORK_ERROR, 'message':str(r.raw), 'data':{}}
		
	"""
	直接上传文件
	适用于较小文件，大文件请采用分片上传
	filepath:         文件本地路径
	bucket:           上传的bcuket名称
	dstpath:          上传的文件存储路径
	bizattr:          文件的属性
	"""
	def upload(self, filepath, bucket, dstpath, bizattr=''):
		filepath = os.path.abspath(filepath);
		if not os.path.exists(filepath):
			return {'httpcode':0, 'code':self.COS_FILE_NOT_EXISTS, 'message':'file not exists', 'data':{}}
		expired = int(time.time()) + self.EXPIRED_SECONDS
		bucket = string.strip(bucket, '/')
		dstpath = urllib.quote(string.strip(dstpath, '/'))
		url = self.generate_res_url(bucket, dstpath)
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_more(bucket, expired)
		sha1 = hashlib.sha1();
		fp = open(filepath, 'rb')
		sha1.update(fp.read())
		fp.close()

		headers = {
			'Authorization':sign,
			'User-Agent':conf.get_ua(),
		}

		files = {'op':'upload','filecontent':open(filepath, 'rb'),'sha':sha1.hexdigest(),'biz_attr':bizattr}

		return self.sendRequest('POST', url, headers=headers, files=files)

	"""
	直接上传文件内容
	适用于较小文件，大文件请采用分片上传
	buffer:           文件内容
	bucket:           上传的bcuket名称
	dstpath:          上传的文件存储路径
	bizattr:          文件的属性
	"""
	def upload_buffer(self, buffer, bucket, dstpath, bizattr=''):
		expired = int(time.time()) + self.EXPIRED_SECONDS
		bucket = string.strip(bucket, '/')
		dstpath = urllib.quote(string.strip(dstpath, '/'))
		url = self.generate_res_url(bucket, dstpath)
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_more(bucket, expired)
		sha1 = hashlib.sha1();
		sha1.update(buffer)

		headers = {
			'Authorization':sign,
			'User-Agent':conf.get_ua(),
		}

		files = {'op':'upload','filecontent':buffer,'sha':sha1.hexdigest(),'biz_attr':bizattr}

		return self.sendRequest('POST', url, headers=headers, files=files)

	"""
	创建目录
	bucket      
	path        创建的目录路径
	bizattr     目录属性
	"""
	def createFolder(self, bucket, path, bizattr=''):
		expired = int(time.time()) + self.EXPIRED_SECONDS
		bucket = string.strip(bucket, '/')
		path = urllib.quote(string.strip(path, '/') + '/')
		url = self.generate_res_url(bucket, path)
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_more(bucket, expired)

		headers = {
			'Authorization':sign,
			'Content-Type':'application/json',
			'User-Agent':conf.get_ua(),
		}

		data = {'op':'create','biz_attr':bizattr}

		return self.sendRequest('POST', url, headers=headers, data=json.dumps(data))
		
	"""
	目录列表,前缀搜索
	bucket      
	path	目录路径
		/			必须以'/'结尾
		/[DirName]/		必须以'/'结尾
		/[DirName]/[prefix] 	列出含prefix此前缀的所有文件,不能以'/'结尾
	num         拉取的总数
	pattern     eListBoth, ListDirOnly, eListFileOnly 默认eListBoth
	order       默认正序(=0), 填1为反序
	offset      透传字段,用于翻页,前端不需理解,需要往前/往后翻页则透传回来
	"""
	def listFiles(self, bucket, path, num=20, pattern='eListBoth', order=0, offset='') :
		expired = int(time.time()) + self.EXPIRED_SECONDS
		bucket = string.strip(bucket, '/')
		path = urllib.quote(string.lstrip(path, '/'))
		url = self.generate_res_url(bucket, path)
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_more(bucket, expired)

		headers = {
			'Authorization':sign,
			'User-Agent':conf.get_ua(),
		}

		data = {'op':'list','num':num,'pattern':pattern,'order':order,'offset':offset}

		return self.sendRequest('GET', url, headers=headers, params=data)
        
	"""
	目录/文件信息 update
	bucket      
	path        目录/文件路径，目录必须以'/'结尾，文件不能以'/'结尾
	bizattr     目录/文件属性
	"""
	def update(self, bucket, path, bizattr=''):
		expired = int(time.time()) + self.EXPIRED_SECONDS
		bucket = string.strip(bucket, '/')
		path = urllib.quote(string.lstrip(path, '/'))
		url = self.generate_res_url(bucket, path)
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_once(bucket, '/'+str(conf.get_app_info()['appid'])+'/'+bucket+'/'+path)

		headers = {
			'Authorization':sign,
			'Content-Type':'application/json',
			'User-Agent':conf.get_ua(),
		}

		data = {'op':'update','biz_attr':bizattr}

		return self.sendRequest('POST', url, headers=headers, data=json.dumps(data))
		
	"""
	删除文件及目录
	参数:
	bucket      
	path        目录/文件路径，目录必须以'/'结尾，文件不能以'/'结尾
	"""
	def delete(self, bucket, path):
		if path == '':
			return {'httpcode':0, 'code':self.COS_PARAMS_ERROR, 'message':'path cannot be empty', 'data':{}}
		expired = int(time.time()) + self.EXPIRED_SECONDS
		bucket = string.strip(bucket, '/')
		path = urllib.quote(string.lstrip(path, '/'))
		url = self.generate_res_url(bucket, path)
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_once(bucket, '/'+str(conf.get_app_info()['appid'])+'/'+bucket+'/'+path)

		headers = {
			'Authorization':sign,
			'Content-Type':'application/json',
			'User-Agent':conf.get_ua(),
		}

		data = {'op':'delete'}

		return self.sendRequest('POST', url, headers=headers, data=json.dumps(data))


	"""
	目录/文件信息 查询
	参数:
	bucket      
	path        目录/文件路径，目录必须以'/'结尾，文件不能以'/'结尾
	"""
	def stat(self, bucket, path):
		expired = int(time.time()) + self.EXPIRED_SECONDS
		bucket = string.strip(bucket, '/')
		path = urllib.quote(string.lstrip(path, '/'))
		url = self.generate_res_url(bucket, path)
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_more(bucket, expired)

		headers = {
			'Authorization':sign,
			'User-Agent':conf.get_ua(),
		}

		data={'op':'stat'}

		return self.sendRequest('GET', url, headers=headers, params=data)


	"""
	分片上传文件
	建议较大文件采用分片上传，参数和返回值同upload函数
	"""
	def upload_slice(self, filepath, bucket, dstpath, bizattr='', slice_size=0, session=''):
		filepath = os.path.abspath(filepath);
		bucket = string.strip(bucket, '/')
		dstpath = urllib.quote(string.strip(dstpath, '/'))
		rsp = self.upload_prepare(filepath,bucket,dstpath,bizattr,slice_size,session)
		if rsp['httpcode'] != 200 or rsp['code'] != 0:  #上传错误
			return rsp
		if rsp.has_key('data'):
			if rsp['data'].has_key('url'):  #秒传命中
				 return rsp
		offset = 0
		data = rsp['data']
		if data.has_key('slice_size'):
			slice_size = int(data['slice_size'])
		if data.has_key('offset'):
			offset = int(data['offset'])
		if data.has_key('session'):
			session = data['session']
		size = os.path.getsize(filepath)
		fp = open(filepath, 'rb')
		fp.seek(offset)
		while size > offset:
			data = fp.read(slice_size)
			retry = 0
			while(True):
				ret = self.upload_data(bucket,dstpath,data,session,offset)
				if ret['httpcode'] != 200 or ret['code'] != 0:
					if retry < 3:
						retry += 1
						continue
					return  ret
				if ret.has_key('data'):
					if ret['data'].has_key('url'):
						return  ret
				break
			offset += slice_size
		return  ret

	#分片上传,控制包/断点续传
	def upload_prepare(self,filepath,bucket,dstpath,bizattr,slice_size,session):
		if not os.path.exists(filepath):
			return {'httpcode':0, 'code':self.COS_FILE_NOT_EXISTS, 'message':'file not exists', 'data':{}}

		url = self.generate_res_url(bucket, dstpath)
		expired = int(time.time()) + self.EXPIRED_SECONDS
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_more(bucket, expired)
		size = os.path.getsize(filepath)
		sha1 = hashlib.sha1();
		fp = open(filepath, 'rb')
		sha1.update(fp.read())

		headers = {
			'Authorization':sign,
			'User-Agent':conf.get_ua(),
		}

		files = {'op': ('upload_slice'),'sha':sha1.hexdigest(),'filesize': str(size)}
		if bizattr != '':
			files['biz_attr'] = bizattr
		if slice_size > 0:
			files['slice_size'] = str(slice_size)
		if session != '':
			files['session'] = session
		return self.sendRequest('POST', url, headers=headers,files=files)
			
	#上传二进制流，用于分片上传
	def upload_data(self,bucket,dstpath,data,session,offset):

		url = self.generate_res_url(bucket,dstpath)
		expired = int(time.time()) + self.EXPIRED_SECONDS
		auth = Auth(self._secret_id, self._secret_key)
		sign = auth.sign_more(bucket, expired)

		sha1 = hashlib.sha1();
		sha1.update(data)

		headers = {
			'Authorization':sign,
			'User-Agent':conf.get_ua(),
		}

		files = {'op': ('upload_slice'),'filecontent': data,'sha':sha1.hexdigest(),'session':session,'offset':str(offset)}
		return self.sendRequest('POST', url, headers=headers, files=files)
