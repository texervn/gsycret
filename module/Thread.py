import time
import queue
import threading

# custom module
from . import Drive
from . import Encryption

# constant
ENCRYPTION = None
THREADS_NUM = None

# global var
q = queue.Queue()

class Object:
	def merge():
		while q.qsize() > 0:
			obj = q.get()

			try:
				Drive.download(obj)
			except Exception as e:
				print('[%10s] %s' % ('Error', str(e)))

			if ENCRYPTION:
				try:
					Encryption.encrypt(obj.title, obj.destination)
					obj.title += '.zip'
					#Encryption.decrypt(obj.title, obj.parents[0]['id'])
					#obj.title = obj.title[:obj.title.rfind('.')]
				except:
					print('[%10s] %s' % ('Error', str(e)))

			try:
				Drive.upload(obj)
			except Exception as e:
				print('[%10s] %s' % ('Error', str(e)))

			time.sleep(1)

	def push():
		while q.qsize() > 0:
			obj = q.get()

			if ENCRYPTION:
				try:
					Encryption.encrypt(obj, obj.destination)
					obj.title += '.zip'
				except Exception as e:
					print('[%10s] %s' % ('Error', str(e)))

			try:
				Drive.upload(obj)
			except Exception as e:
				print('[%10s] %s' % ('Error', str(e)))

			time.sleep(1)

	def pull():
		while q.qsize() > 0:
			obj = q.get()

			try:
				Drive.download(obj)
			except Exception as e:
				print('[%10s] %s' % ('Error', str(e)))

			time.sleep(1)

def run(var):
	# init
	threads = []
	for i in range(0, THREADS_NUM):
		t = threading.Thread(target=var, name='T' + str(i))
		threads.append(t)

	# run
	for i in range(0, len(threads)):
		threads[i].start()

	# wait until finish
	while any(thread.is_alive() for thread in threads):
		time.sleep(1)