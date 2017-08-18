from . import drive

def merge(source, destination):
	# var
	matched = []

	# ls
	s_files = drive.ListFile({'q': "'%s' in parents and trashed=false" % source}).GetList()
	d_files = drive.ListFile({'q': "'%s' in parents and trashed=false" % destination}).GetList()
	
	for i in s_files:
		# folder
		if i['mimeType'] == 'application/vnd.google-apps.folder':
			if any(j for j in d_files if j['title'] == i['title']):
				temp = next(j for j in d_files if j['title'] == i['title'])
				matched.extend(merge(i['id'], temp['id']))
			else:
				# create folder
				temp = drive.CreateFile({'title': i['title'], "parents":  [{"id": destination}], "mimeType": "application/vnd.google-apps.folder"})
				temp.Upload()
				matched.extend(merge(i['id'], temp['id']))
		# not folder
		elif not any(j for j in d_files if j['title'] == i['title'] or j['title'][:j['title'].rfind('.')] == i['title']):
			matched.append(Object({
				'id': i['id'],
				'title': i['title'],
				'source': destination,
				'destination': os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'
			}))

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
				matched.extend(push(os.path.join(source, i), temp['id']))
		# is file
		else:
			if not any(j for j in d_files if j['title'] == i):
				matched.append(Object({
					'id': '',
					'title': i,
					'source': source + '/',
					'destination': destination
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
				'id': i['id'],
				'title': i['title'],
				'source': i['parents'][0]['id'],
				'destination': destination + '/'
			}))

	return matched