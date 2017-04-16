def encrypt(self):
		print('[%10s] %s' % ('Encrypt', self.title))
		subprocess.call(['zip', '--password', PATH + self.parents[0]['id'], PATH + self.title + '.zip', PATH + self.title])
