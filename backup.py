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

# constant
PATH = os.path.dirname(os.path.abspath(__file__))

# global var
ENCRYPTION = None
THREADS_NUM = None
q = queue.Queue()

def load_config():
	# load configuration
	try:
		with open(PATH + '/config.json', 'r') as file:
			para = json.load(file)

		ENCRYPTION = para['encryption']
		THREADS_NUM = para['threads_num']
	except:
		print('[%10s] %s' % ('Error', 'Missing config.json'))
		exit()

	return (ENCRYPTION, THREADS_NUM)

def next():
	while q.qsize() > 0:
		job = q.get()
		job.run()
		time.sleep(1)

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
	# check input
	if len(sys.argv) != 3:
		print('[%10s] %s %s' % ('Usage', '<source>', '<destination>'))
		exit()

	# var
	SOURCE = sys.argv[1]
	DESTINATION = sys.argv[2]

	# load config
	ENCRYPTION, THREADS_NUM = load_config()

	# init
	Drive.auth()
	
	# match
	matched = Drive.match(SOURCE, DESTINATION)
	print('[%10s] %d files found' % ('Match', len(matched)))

	# to queue
	list(map(q.put, matched))

	run()
