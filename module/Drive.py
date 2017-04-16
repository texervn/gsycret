import os
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# constant
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'

# global var
drive = None

class Object:
	def __init__(self, var):
		self.id = var['id']
		self.title = var['title']
		self.parents = var['parents']

		# remove file
		os.remove(PATH + self.title)
		
	def download(self):
		print('[%10s] %s' % ('Download', self.title))
		file = drive.CreateFile({'id': self.id})
		file.GetContentFile(PATH + self.title)

	def upload(self):
		print('[%10s] %s' % ('Upload', self.title))
		file = drive.CreateFile({"title": self.title, "parents": [{"kind": "drive#fileLink", "id": self.parents[0]['id']}]})
		file.SetContentFile(PATH + self.title)
		file.Upload()

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

def match(source, dst):
	# var
	matched = []

	# list files
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
				matched.extend(match(i['id'], temp['id']))
			else:
				temp = dst_files[dst_titles.index(i['title'])]
				matched.extend(match(i['id'], temp['id']))
		# not folder
		elif i['title'] not in dst_titles:
			i['parents'] = [{"kind": "drive#fileLink", "id": dst}]
			#print(i)
			matched.append(Object(i))

	return matched
