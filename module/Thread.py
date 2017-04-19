import time
import queue
import threading

# custom module
from . import Drive
from . import Encryption

# global var
q = queue.Queue()

class Object:
	def merge(var):
		while q.qsize() > 0:
			# init
			obj = q.get()

			try:
				Drive.download(obj)
			except Exception as e:
				print('[%10s] %s' % ('Error', str(e)))

			if var['auto'] or var['password']:
				try:
					Encryption.encrypt(obj, obj.destination if var['auto'] else var['password'])
					obj.title += '.zip'
				except:
					print('[%10s] %s' % ('Error', str(e)))


			try:
				Drive.upload(obj)
			except Exception as e:
				print('[%10s] %s' % ('Error', str(e)))

			time.sleep(1)

	def push(var):
		while q.qsize() > 0:
			# init
			obj = q.get()

			if var['auto'] or var['password']:
				try:
					Encryption.encrypt(obj, obj.destination if var['auto'] else var['password'])
					obj.title += '.zip'
				except Exception as e:
					print('[%10s] %s' % ('Error', str(e)))

			try:
				Drive.upload(obj)
			except Exception as e:
				print('[%10s] %s' % ('Error', str(e)))

			time.sleep(1)

	def pull(var):
		while q.qsize() > 0:
			# init
			obj = q.get()

			try:
				Drive.download(obj)
			except Exception as e:
				print('[%10s] %s' % ('Error', str(e)))

			if var['auto'] or var['password']:
				try:
					Encryption.decrypt(obj, obj.source if var['auto'] else var['password'])
					obj.title = obj.title[:obj.title.rfind('.')]
				except Exception as e:
					print('[%10s] %s' % ('Error', str(e)))

			time.sleep(1)

def run(var):
	# init
	threads = []
	for i in range(0, var['threads_num']):
		t = threading.Thread(name='T' + str(i), target=getattr(Object, var['mode'])({
			'auto': var['auto'],
			'password': var['password']
		}))
		threads.append(t)

	# run
	for i in range(0, len(threads)):
		threads[i].start()

	# wait until finish
	while any(thread.is_alive() for thread in threads):
		time.sleep(1)