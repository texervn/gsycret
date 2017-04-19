import os
import subprocess

# custom
from . import Drive

def encrypt(file, password):
	print('[%10s] %s with pw: %s' % ('Encrypt', file.title, password))
	subprocess.call(['zip', '-q', '-j', '--password', password, file.source + file.title + '.zip', file.source + file.title])
	
def decrypt(file, password):
	print('[%10s] %s with pw: %s' % ('Decrypt', file.title, password))
	subprocess.call(['unzip', '-q', '-j', '-P', password, '-d', file.destination, file.destination + file.title])