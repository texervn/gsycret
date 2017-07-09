from __future__ import absolute_import
from __future__ import print_function

import os
import time
import queue
import threading

# custom module
from gsycret.task import Task
from gsycret.drive import Drive

# constant
__temp__ = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'

class Client:
	def __init__(self, q, threads_num):
		self.q = queue.Queue()
		self.drive = Drive()
		self.threads_num = threads_num

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
			self.drive.upload(t.dst, __temp__, t.title)

	def push(self):
		while self.q.qsize() > 0:
			t = self.q.get()
			self.drive.upload(t.dst, t.src, t.title)

	def pull(self):
		while self.q.qsize() > 0:
			t = self.q.get()
			self.drive.download(t.id, t.dst, t.title)