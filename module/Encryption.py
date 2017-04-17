import os
import subprocess

# constant
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'

def encrypt(file, password):
	print('[%10s] %s' % ('Encrypt', file))
	print('ENCODE %s %s' % (file, password))
	subprocess.call(['zip', '--password', password, PATH + file + '.zip', PATH + file])
	os.remove(PATH + file)

def decrypt(file, password):
	print('[%10s] %s' % ('Decrypt', file))
	print('DECODE %s %s' % (file, password))
	subprocess.call(['unzip', '-j', '-P', password, PATH + file])
	print(' '.join(['unzip', '-j', '-P', password, '-d', PATH[:-1], PATH + file]))
	#os.remove(PATH + file)