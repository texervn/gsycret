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
	parser.add_argument('--password', action='store', help='password')
	parser.add_argument('--auto', action='store_true', help='auto encrypt', default=False)
	parser.add_argument('--threads_num', action='store', help='number of threads', type=int, default=4)
	results = parser.parse_args()
	
	return {
		'name': 'Default',
		'mode': results.m,
		'source': results.s,
		'destination': results.d,
		'password': results.password,
		'auto': results.auto,
		'threads_num': results.threads_num
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

	for task in tasks:
		# var
		matched = []

		# auth
		Drive.auth()

		# init
		print('[%10s] %s' % ('Match', 'Start'))
		matched = getattr(Drive, task['mode'])(task['source'], task['destination'])
		print('[%10s] %s' % ('Match', '%d files found' % len(matched)))

		# to queue
		list(map(Thread.q.put, matched))

		Thread.run({
			'mode': task['mode'],
			'auto': task['auto'],
			'password': task['password'],
			'threads_num': task['threads_num']
		})