import os
import subprocess
from os import listdir
from os.path import join
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# constant
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'

# global var
drive = None

class Object:
	def __init__(self, var):
		self.id = var['id']
		self.path = var['path']
		self.title = var['title']
		self.parents = var['parents']
		self.destination = var['destination']
		
	def download(self):
		print('[%10s] %s' % ('Download', self.title))
		file = drive.CreateFile({'id': self.id})
		file.GetContentFile(self.path + self.title)

	def upload(self):
		print('[%10s] %s' % ('Upload', self.title))
		file = drive.CreateFile({"title": self.title, "parents": [{"kind": "drive#fileLink", "id": self.destination}]})
		file.SetContentFile(self.path + self.title)
		file.Upload()

# OAuth
def auth():
	print('[%10s] %s' % ('Auth', 'Google API'))

	# var
	global drive

	# OAuth
	gauth = GoogleAuth()
	gauth.LoadCredentialsFile('mycreds.txt')

	# load failed
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

	# save current credentials
	gauth.SaveCredentialsFile('mycreds.txt')

	drive = GoogleDrive(gauth)

def merge(source, destination):
	# var
	matched = []

	# ls
	s_files = drive.ListFile({'q': "'%s' in parents and trashed=false" % source}).GetList()
	d_files = drive.ListFile({'q': "'%s' in parents and trashed=false" % destination}).GetList()
	
	for i in s_files:
		# folder
		if i['mimeType'] == 'application/vnd.google-apps.folder':
			if any(j for j in d_files if j['title'] == i):
				temp = next(j for j in d_files if j['title'] == i)
				matched.extend(merge(i['id'], temp['id']))
			else:
				# create folder
				temp = drive.CreateFile({'title': i['title'], "parents":  [{"id": destination}], "mimeType": "application/vnd.google-apps.folder"})
				temp.Upload()
				matched.extend(merge(i['id'], temp['id']))
		# not folder
		elif not any(j for j in d_files if j['title'] == i):
			i['path'] = PATH
			i['destination'] = destination
			matched.append(Object(i))

	return matched

def push(source, destination):
	# var 
	matched = []

	# ls
	s_files = listdir(source)
	d_files = drive.ListFile({'q': "'%s' in parents and trashed=false" % destination}).GetList()

	for i in s_files:
		# is folder
		if os.path.isdir(os.path.join(source, i)):		
			if any(j for j in d_files if j['title'] == i):
				temp = next(j for j in d_files if j['title'] == i)
				matched.extend(push(os.path.join(source, i), temp['id']))
			else:
				# create folder
				temp = drive.CreateFile({'title': i, "parents":  [{"id": destination}], "mimeType": "application/vnd.google-apps.folder"})
				temp.Upload()
				print(os.path.join(source, i))
				matched.extend(push(os.path.join(source, i), temp['id']))
		# is file
		else:
			if not any(j for j in d_files if j['title'] == i):
				matched.append(Object({
					"id": "",
					"path": source + '/',
					"title": i,
					"parents": destination,
					"destination": destination
				}))

	return matched

def pull(source, destination):
	# var
	matched = []

	# ls
	s_files = drive.ListFile({'q': "'%s' in parents and trashed=false" % source}).GetList()
	d_files = listdir(destination)
	
	for i in s_files:
		# folder
		if i['mimeType'] == 'application/vnd.google-apps.folder':
			# existed
			if any(j for j in d_files if j == i['title'] and os.path.isdir(os.path.join(destination, j))):
				temp = next(j for j in d_files if j == i['title'])
				matched.extend(pull(i['id'], os.path.join(destination, temp)))
			# not existed
			else:
				os.mkdir(os.path.join(destination, i['title']))
				matched.extend(pull(i['id'], os.path.join(destination, i['title'])))
		# not folder
		elif not any(j for j in d_files if j == i['title'] and not os.path.isdir(os.path.join(destination, j))):
			matched.append(Object({
				"id": i['id'],
				"path": destination + '/',
				"title": i['title'],
				"parents": source,
				"destination": destination
			}))

	return matched