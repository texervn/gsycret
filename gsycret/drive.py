from __future__ import absolute_import
from __future__ import print_function

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# module
from gsycret.task import Task
from gsycret.settings import *

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

	def ls(self, id):
		self.log('ls', id)
		try:
			return self.drive.ListFile({'q': ls_pattern.format(id=id)}).GetList()
		except Exception as e:
			self.log('ls', str(e))

	def download(self, id, path, title):
		self.log('download', title)
		try:
			file = self.drive.CreateFile({'id': id})
			file.GetContentFile(file_pattern.format(
				module = 'drive',
				path = path,
				title = title
			))
		except Exception as e:
			self.log('download', str(e))

	def upload(self, id, path, title):
		self.log('upload', title)
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
			self.log('upload', str(e))

	def mkdir(self, id, title):
		folder = self.drive.CreateFile({
			'title': title, 
			'parents':  [{'id': id}], 
			'mimeType': 'application/vnd.google-apps.folder'
		})
		folder.Upload()
		return folder

	def log(self, func, msg):
		print(log_pattern.format(
			module = 'drive',
			func = func,
			msg = msg
		))

# rename
drive = Drive()