from __future__ import absolute_import
from __future__ import print_function

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# module
from module.task import Task

# pattern
ls_pattern = '"{id}" in parents and trashed = false'
log_pattern = '{func:<10}{msg}'
file_pattern = '{path}/{title}'

class Drive:
	def __init__(self):
		# var
		self.drive = None

		# init
		self.auth()

	def auth(self):
		# var
		gauth = GoogleAuth()
		gauth.LoadCredentialsFile('mycreds.txt')

		# load cache failed
		if gauth.credentials is None:
			gauth.LocalWebserverAuth()
		# refresh if expired
		elif gauth.access_token_expired:
			try:
				gauth.Refresh()
			except:
				gauth.LocalWebserverAuth()
		else:
			gauth.Authorize()

		# save credentials
		gauth.SaveCredentialsFile('mycreds.txt')

		# init
		self.drive = GoogleDrive(gauth)

		# log
		print(log_pattern.format(func='auth', msg='done'))

	def ls(self, id):
		# log
		print(log_pattern.format(
			func = 'ls',
			msg = id
		))

		try:
			return self.drive.ListFile({'q': ls_pattern.format(id=id)}).GetList()
		except Exception as e:
			print(log_pattern.format(
				func = 'ls',
				msg = str(e)
			))

	def download(self, id, path, title):
		# log
		print(log_pattern.format(
			func = 'download',
			msg = title
		))

		try:
			file = self.drive.CreateFile({'id': id})
			file.GetContentFile(file_pattern.format(
				path = path,
				title = title
			))
		except Exception as e:
			print(log_pattern.format(
				func = 'download',
				msg = str(e)
			))


	def upload(self, id, path, title):
		# log
		print(log_pattern.format(
			func = 'upload',
			msg = title
		))

		try:
			file = self.drive.CreateFile({
				'title': title, 
				'parents': [{
					'kind': 'drive#fileLink', 
					'id': id
				}]
			})
			file.SetContentFile(file_pattern.format(
				path = path,
				title = title	
			))
			file.Upload()
		except Exception as e:
			print(log_pattern.format(
				func = 'upload',
				msg = str(e)
			))

	def mkdir(self, id, title):
		folder = self.drive.CreateFile({
			'title': title, 
			'parents':  [{'id': id}], 
			'mimeType': 'application/vnd.google-apps.folder'
		})
		folder.Upload()
		return folder

# rename
drive = Drive()