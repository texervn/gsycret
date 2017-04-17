import os
import subprocess

# constant
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'

def encrypt(file, password):
	print('[%10s] %s with pw: %s' % ('Encrypt', file, password))
	subprocess.call(['zip', '-q', '-j', '--password', password, PATH + file + '.zip', PATH + file])
	os.remove(PATH + file)

def decrypt(file, password):
	print('[%10s] %s with pw: %s' % ('Decrypt', file, password))
	subprocess.call(['unzip', '-q', '-j', '-P', password, PATH + file])
	os.remove(PATH + file)