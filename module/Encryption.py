import os
import subprocess

# custom
from . import Drive

def encrypt(file, password):
	print('[%10s] %s with pw: %s' % ('Encrypt', file.path + file.title, password))
	subprocess.call(['zip', '-q', '-j', '--password', password, file.path + file.title + '.zip', file.path + file.title])
	
def decrypt(file, password):
	print('[%10s] %s with pw: %s' % ('Decrypt', file.path + file.title, password))
	subprocess.call(['unzip', '-q', '-j', '-P', password, file.path + file.title])