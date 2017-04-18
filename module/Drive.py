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

		print(self.title + ' @@@ ' + self.path)

		print('[%10s] %s' % ('Upload', self.title))
		file = drive.CreateFile({"title": self.title, "parents": [{"kind": "drive#fileLink", "id": self.destination}]})
		file.SetContentFile(self.path + self.title)
		file.Upload()

		# remove useless
		#os.remove(PATH + self.title)

# OAuth
def auth():
	print('[%10s] %s' % ('Auth', 'Google API'))

	# var
	global drive

	# OAuth
	gauth = GoogleAuth()
	gauth.LoadCredentialsFile('mycreds.txt')

	# load saved failed
	if gauth.credentials is None:
		gauth.LocalWebserverAuth()
	# refresh if expired
	elif gauth.access_token_expired:
		try:
			gauth.Refresh()
		except:
			gauth.LocalWebserverAuth()
	# init new and save
	else:
		gauth.Authorize()

	# save current credentials
	gauth.SaveCredentialsFile('mycreds.txt')

	drive = GoogleDrive(gauth)

def merge(source, dst):
	# var
	matched = []

	# ls
	source_files = drive.ListFile({'q': "'%s' in parents and trashed=false" % source}).GetList()
	dst_files = drive.ListFile({'q': "'%s' in parents and trashed=false" % dst}).GetList()
	dst_titles = [i['title'] for i in dst_files]

	for i in source_files:
		# folder
		if i['mimeType'] == 'application/vnd.google-apps.folder':
			if i['title'] not in dst_titles:
				# create folder
				temp = drive.CreateFile({'title': i['title'], "parents":  [{"id": dst}], "mimeType": "application/vnd.google-apps.folder"})
				temp.Upload()
				matched.extend(merge(i['id'], temp['id']))
			else:
				temp = dst_files[dst_titles.index(i['title'])]
				matched.extend(merge(i['id'], temp['id']))
		# not folder
		elif i['title'] not in dst_titles:
			i['path'] = PATH
			i['destination'] = dst
			matched.append(Object(i))

	return matched

def push(source, dst):
	# var 
	matched = []

	# ls
	local = listdir(source)
	remote = drive.ListFile({'q': "'%s' in parents and trashed=false" % dst}).GetList()
	remote_title = [i['title'] for i in remote]

	#print(remote)
	#print(remote_title)
	
	#return []

	for i in local:
		# is folder
		if os.path.isdir(os.path.join(source, i)):		
			if any(j for j in remote if j['title'] == i):
				temp = next(j for j in remote if j['title'] == i)
				matched.extend(push(i, temp['id']))
			else:
				# create folder
				temp = drive.CreateFile({'title': i, "parents":  [{"id": dst}], "mimeType": "application/vnd.google-apps.folder"})
				temp.Upload()
				print(os.path.join(source, i))
				matched.extend(push(os.path.join(source, i), temp['id']))

		# is file
		else:
			if i not in remote_title:
				matched.append(Object({
					"id": "",
					"path": source + '/',
					"title": i,
					"parents": dst,
					"destination": dst
				}))

	return matched

def pull(source, dst):
	return
