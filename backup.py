import os
import sys
import time
import json
import queue
import argparse
import threading
import subprocess
from os import listdir
from os.path import isfile, join
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# custom module
from module import Drive
from module import Thread
from module import Encryption

# constant
PATH = os.path.dirname(os.path.abspath(__file__))

def parse_argv():
	# init
	parser = argparse.ArgumentParser()

	# add argument
	parser.add_argument('-m', help='choose operation', choices=('push', 'pull', 'merge'))
	parser.add_argument('-s', action='store', help='source')
	parser.add_argument('-d', action='store', help='destination')
	parser.add_argument('-p', action='store', help='password')
	parser.add_argument('-a', action='store_true', help='auto encryption', default=False)
	parser.add_argument('-t', action='store', help='threads_num', type=int, default=4)
	results = parser.parse_args()
	
	return {
		'name': 'Default',
		'mode': results.m,
		'source': results.s,
		'destination': results.d,
		'password': results.p,
		'auto': results.a,
		'threads_num': results.t
	}

def load_config(file):
	try:
		with open(PATH + '/' + file, 'r') as config:
			para = json.load(config)
			return para
	except:
		print('[%10s] %s' % ('Error', 'load_config()'))
		exit()

if __name__ == '__main__':
	# var
	tasks = []
	source = None
	destination = None

	# load config
	config = load_config('config.json')
	Thread.ENCRYPTION, Thread.THREADS_NUM = config['encryption'], config['threads_num']

	# check argv
	if len(sys.argv) == 1:
		tasks = load_config('backup.json')	
	else:
		tasks = [parse_argv()]

	# init
	Drive.auth()

	for task in tasks:
		# var
		matched = []

		# init
		if task['mode'] == 'push':
			matched = Drive.push(task['source'], task['destination'])
		elif task['mode'] == 'pull':
			matched = Drive.pull(task['source'], task['destination'])
		elif task['mode'] == 'merge':
			matched = Drive.merge(task['source'], task['destination'])
		
		print('[%10s] %d files found' % ('Match', len(matched)))

		# to queue
		list(map(Thread.q.put, matched))

		Thread.run(getattr(Thread.Object, task['mode']))