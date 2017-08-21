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

class Client:
	def __init__(self, args):
		self.drive = drive
		self.crypto = Crypto()
		self.q = queue.Queue()
		self.threads_num = args['threads_num']
		self.password = args['password']
		self.auto = args['auto']

	def run(self, command):
		# init
		threads = []
		for i in range(0, self.threads_num):
			t = threading.Thread(name='T' + str(i), target=getattr(self, command))
			threads.append(t)

		# run
		for i in range(0, len(threads)):
			threads[i].start()

		# wait until finish
		while any(thread.is_alive() for thread in threads):
			time.sleep(1)

	def merge(self):
		while self.q.qsize() > 0:
			t = self.q.get()
			self.drive.download(t.id, __temp__, t.title)
			
			# crypto
			if self.auto:
				self.crypto.decrypt(__temp__, t.title, t.src)
				self.crypto.encrypt(__temp__, t.title, t.dst)
			
			self.drive.upload(t.dst, __temp__, t.title)
			os.remove(file_pattern.format(path=__temp__, title=t.title))

	def push(self):
		while self.q.qsize() > 0:
			t = self.q.get()

			# crypto
			if self.auto:
				self.crypto.encrypt(t.src, t.title, t.dst)
			elif self.password != None:
				self.crypto.encrypt(t.src, t.title, self.password)
			
			self.drive.upload(t.dst, t.src, t.title)

	def pull(self):
		while self.q.qsize() > 0:
			t = self.q.get()
			self.drive.download(t.id, t.dst, t.title)
			
			# crypto
			if self.auto:
				self.crypto.decrypt(t.dst, t.title, t.src)
			elif self.password != None:
<<<<<<< HEAD
				self.crypto.decrypt(t.dst, t.title, self.password, t.dst)
=======
				self.crypto.decrypt(t.dst, t.title, self.password, t.dst)
>>>>>>> fa4c71d8d52ea87f1bf8b607ca2b9c1da13c906b
