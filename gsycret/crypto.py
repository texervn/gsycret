import subprocess

# module
from gsycret.settings import *

class Crypto:
	def __init__(self):
		return

	def encrypt(self, path, title, password):
		self.log('encrypt', title)
		try:
			subprocess.call([
				'zip', 
				'-q', 
				'-j', 
				'--password', 
				password, 
				file_pattern.format(
					path = path,
					title = title + '.zip'
				),
				file_pattern.format(
					path = path,
					title = title
				) 
			])
		except Exception as e:
			self.log('encrypt', str(e))
		
	def decrypt(self, src, title, password, dst):
		self.log('decrypt', title)

		# var
		ext = title[title.rfind('.') + 1:]

		try:
			if ext == 'rar':
				subprocess.call([
					'unrar',
					'x',
					'-p%s' % password,
					'-inul',
					file_pattern.format(
						path = src,
						title = title
					),
					dst
				])
			else:
				subprocess.call([
					'unzip', 
					'-q', 
					'-j',
					'-f',
					'-P', 
					password, 
					'-d', 
					dst, 
					file_pattern.format(
						path = src,
						title = title
					)
				])

			os.remove(file_pattern.format(
				path = src,
				title = title
			))
		except Exception as e:
			self.log('decrypt', str(e))

	def log(self, func, msg):
		print(log_pattern.format(
			module = 'crypto',
			func = func,
			msg = msg
		)) 

# rename
crypto = Crypto()