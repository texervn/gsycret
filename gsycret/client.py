from __future__ import absolute_import
from __future__ import print_function

import os
import time
import queue
import threading

# custom module
from gsycret.task import *
from gsycret.drive import *
from gsycret.crypto import *
from gsycret.settings import *

# constant
__temp__ = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'

class Merge:
	def __init__(self):
		self.q = queue.Queue()
		self.drive = drive
		self.crypto = Crypto()
		
	def init(self, **kwargs):
		src_files = self.drive.ls(kwargs['src'])
		dst_files = self.drive.ls(kwargs['dst'])

		for i in src_files:
			# folder
			if i['mimeType'] == 'application/vnd.google-apps.folder':
				if any(j for j in dst_files if j['title'] == i['title']):
					temp = next(j for j in dst_files if j['title'] == i['title'])
					self.merge(i['id'], temp['id'])
				else:
					temp = self.drive.mkdir(dst, i['title'])
					self.merge(i['id'], temp['id'])
			# not folder
			elif not any(j for j in dst_files if j['title'] == i['title'] or j['title'][:j['title'].rfind('.')] == i['title']):
				self.q.push(Task({
					'id': i['id'],
					'title': i['title'],
					'src': None,
					'dst': kwargs['dst']
				}))

	def run(self):
		while self.q.qsize() > 0:
			t = self.q.get()
			self.drive.download(t.id, __temp__, t.title)
			
			# crypto
			if self.auto:
				self.crypto.decrypt(__temp__, t.title, t.src)
				self.crypto.encrypt(__temp__, t.title, t.dst)
			
			self.drive.upload(t.dst, __temp__, t.title)
			os.remove(file_pattern.format(
				path = __temp__, 
				title = t.title)
			)

class Push:
	def __init__(self):
		self.q = queue.Queue()
		self.drive = drive
		self.crypto = Crypto()

	def init(self, **kwargs):
		src_files = os.listdir(kwargs['src'])
		dst_files = self.drive.ls(kwargs['dst'])

		for i in src_files:
			# is folder
			if os.path.isdir(os.path.join(kwargs['src'], i)):		
				if any(j for j in dst_files if j['title'] == i):
					temp = next(j for j in dst_files if j['title'] == i)
					self.q.push(os.path.join(src, i), temp['id'])
				else:
					# create folder
					temp = self.drive.mkdir(dst, i)
					self.q.push(os.path.join(src, i), temp['id'])
			# is file
			else:
				if not any(j for j in dst_files if j['title'] == i):
					self.q.push(Task({
						'id': None,
						'title': i,
						'src': kwargs['src'],
						'dst': kwargs['dst']
					}))

	def run(self):
		while self.q.qsize() > 0:
			t = self.q.get()

			# crypto
			if self.auto:
				self.crypto.encrypt(t.src, t.title, t.dst)
			elif self.password != None:
				self.crypto.encrypt(t.src, t.title, self.password)
			
			self.drive.upload(t.dst, t.src, t.title)

class Pull:
	def __init__(self):
		self.q = queue.Queue()
		self.drive = drive
		self.crypto = Crypto()

	def init(self, **kwargs):
		src_files = self.drive.ls(kwargs['src'])
		dst_files = os.listdir(kwargs['dst'])
		
		for i in src_files:
			# folder
			if i['mimeType'] == 'application/vnd.google-apps.folder':
				# existed
				if any(j for j in dst_files if j == i['title'] and os.path.isdir(os.path.join(dst, j))):
					temp = next(j for j in dst_files if j == i['title'])
					self.init(
						src = i['id'], 
						det = os.path.join(kwargs['dst'], temp)
					)
				# not existed
				else:
					os.mkdir(os.path.join(kwargs['dst'], i['title']))
					self.init(
						src = i['id'], 
						dst = os.path.join(kwargs['dst'], i['title'])
					)
			# not folder
			elif not any(j for j in dst_files if j == i['title'] and not os.path.isdir(os.path.join(kwargs['dst'], j))):
				self.q.put(Task({
					'id': i['id'],
					'title': i['title'],
					'src': None,
					'dst': kwargs['dst']
				}))

	def next(self, **kwargs):
		while self.q.qsize() > 0:
			t = self.q.get()
			self.drive.download(t.id, t.dst, t.title)
			
			# crypto
			if kwargs['auto']:
				self.crypto.decrypt(t.dst, t.title, t.src)
			elif kwargs['password'] != None:
				self.crypto.decrypt(t.dst, t.title, self.password, t.dst)

	def run(self, **kwargs):
		# init
		threads = []
		for i in range(0, kwargs['threads_num']):
			t = threading.Thread(
				name = 'T' + str(i), 
				target = self.next(
					auto = kwargs['auto'],
					password = kwargs['password']
				)
			)
			threads.append(t)

		# run
		for i in range(0, len(threads)):
			threads[i].start()

		# wait until finish
		while any(thread.is_alive() for thread in threads):
			time.sleep(1)

class Client:
	def __init__(self, **kwargs):
		self.drive = drive
		self.push = Push()
		self.pull = Pull()
		self.merge = Merge()