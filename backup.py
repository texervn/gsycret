import os
import sys
import time
import json
import queue
import threading
import subprocess
from os import listdir
from os.path import isfile, join
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# customized module
from module import Drive
from module import Encryption

# constant
PATH = os.path.dirname(os.path.abspath(__file__))

# global var
CASE = None
ENCRYPTION = None
THREADS_NUM = None
q = queue.Queue()

def load_config(file):
	try:
		with open(PATH + '/' + file, 'r') as config:
			para = json.load(config)
			return para
	except:
		print('[%10s] %s' % ('Error', 'load_config()'))
		exit()

def merge():
	while q.qsize() > 0:
		obj = q.get()

		try:
			obj.download()
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
			obj.upload()
		except Exception as e:
			print('[%10s] %s' % ('Error', str(e)))

		time.sleep(1)

def push():
	while q.qsize() > 0:
		obj = q.get()

		if ENCRYPTION:
			try:
				Encryption.encrypt(obj.title, obj.destination)
				obj.title += '.zip'
			except:
				print('[%10s] %s' % ('Error', str(e)))

		try:
			obj.upload()
		except Exception as e:
			print('[%10s] %s' % ('Error', str(e)))

		time.sleep(1)

def next():
	
	if CASE == 'merge':
		merge()
	elif CASE == 'push':
		push()

def run():
	# init
	threads = []
	for i in range(0, THREADS_NUM):
		t = threading.Thread(target=next, name='T' + str(i))
		threads.append(t)

	# run
	for i in range(0, len(threads)):
		threads[i].start()

	# wait until finish
	while any(thread.is_alive() for thread in threads):
		time.sleep(1)

if __name__ == '__main__':
	# var
	tasks = []
	source = None
	destination = None

	# load config
	config = load_config('config.json')
	ENCRYPTION, THREADS_NUM = config['encryption'], config['threads_num']

	# check argv
	if len(sys.argv) == 1:
		tasks = load_config('backup.json')	
	elif len(sys.argv) == 3:
		tasks = [{
			"name": "Default",
			"source": sys.argv[1],
			"destination": sys.argv[2]
		}]
	else:
		print('[%10s] %s' % ('Usage', '<source> <destination>'))
		exit()

	# init
	Drive.auth()

	for task in tasks:
		# match
		CASE = 'push'
		matched = Drive.push(task['source'], task['destination'])
		print('[%10s] %d files found' % ('Match', len(matched)))

	# to queue
	list(map(q.put, matched))

	run()