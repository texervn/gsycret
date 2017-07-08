class gsycret():
	def __init__(self):
		self.api = api()

class api:
	def merge(var):
		while q.qsize() > 0:
			# init
			obj = q.get()

			try:
				Drive.download(obj)
			except Exception as e:
				print('[%10s] %s' % ('Download', str(e)))

			# swap
			obj.source, obj.destination = obj.destination, obj.source

			if var['auto'] or var['password']:
				try:
					Encryption.encrypt(obj, obj.destination if var['auto'] else var['password'])
					obj.title += '.zip'

					# test
					os.remove(obj.source + obj.title[:obj.title.rfind('.')])
				except Exception as e:
					print('[%10s] %s' % ('Encrypt', str(e)))

			try:
				Drive.upload(obj)
				# testing
				os.remove(obj.source + obj.title)
			except Exception as e:
				print('[%10s] %s' % ('Upload', str(e)))

			print('[%10s] %d %s' % ('Merge', q.qsize(), 'files left'))

	def push(var):
		while q.qsize() > 0:
			# init
			obj = q.get()

			if var['auto'] or var['password']:
				try:
					Encryption.encrypt(obj, obj.destination if var['auto'] else var['password'])
					obj.title += '.zip'
				except Exception as e:
					print('[%10s] %s' % ('Encrypt', str(e)))

			try:
				Drive.upload(obj)
			except Exception as e:
				print('[%10s] %s' % ('Upload', str(e)))

			print('[%10s] %d %s' % ('Push', q.qsize(), 'files left'))

	def pull(var):
		while q.qsize() > 0:
			# init
			obj = q.get()

			try:
				Drive.download(obj)
			except Exception as e:
				print('[%10s] %s' % ('Download', str(e)))

			if var['auto'] or var['password']:
				try:
					Encryption.decrypt(obj, obj.source if var['auto'] else var['password'])
					obj.title = obj.title[:obj.title.rfind('.')]
				except Exception as e:
					print('[%10s] %s' % ('Decrypt', str(e)))

			print('[%10s] %d %s' % ('Pull', q.qsize(), 'files left'))