import os
import sys
import json
import argparse

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
	parser.add_argument('-m', help='mode choices', choices=('push', 'pull', 'merge'))
	parser.add_argument('-s', action='store', help='source folder')
	parser.add_argument('-d', action='store', help='destination folder')
	parser.add_argument('-p', action='store', help='password')
	parser.add_argument('-a', action='store_true', help='auto encrypt', default=False)
	parser.add_argument('-t', action='store', help='number of threads', type=int, default=4)
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
	except Exception as e:
		print('[%10s] %s' % ('Error', str(e)))
		exit()

if __name__ == '__main__':
	# var
	tasks = []

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
		matched = getattr(Drive, task['mode'])(task['source'], task['destination'])
		
		print('[%10s] %d files found' % ('Match', len(matched)))

		# to queue
		list(map(Thread.q.put, matched))

		Thread.run({
			'mode': task['mode'],
			'auto': task['auto'],
			'password': task['password'],
			'threads_num': task['threads_num']
		})