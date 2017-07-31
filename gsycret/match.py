from __future__ import absolute_import
from __future__ import print_function

import os

# module
from gsycret.task import Task
from gsycret.drive import Drive
from gsycret.settings import *

class Match:
	def __init__(self):
		self.drive = Drive()

	def merge(self, src, dst):
		# var
		matched = []
		src_files = self.drive.ls(src)
		dst_files = self.drive.ls(dst)

		for i in src_files:
			# folder
			if i['mimeType'] == 'application/vnd.google-apps.folder':
				if any(j for j in dst_files if j['title'] == i['title']):
					temp = next(j for j in dst_files if j['title'] == i['title'])
					matched.extend(self.merge(i['id'], temp['id']))
				else:
					temp = self.drive.mkdir(dst, i['title'])
					matched.extend(self.merge(i['id'], temp['id']))
			# not folder
			elif not any(j for j in dst_files if j['title'] == i['title'] or j['title'][:j['title'].rfind('.')] == i['title']):
				matched.append(Task({
					'id': i['id'],
					'title': i['title'],
					'src': None,
					'dst': dst
				}))

		return matched

	def push(self, src, dst):
		# var 
		matched = []
		src_files = os.listdir(src)
		dst_files = self.drive.ls(dst)

		for i in src_files:
			# is folder
			if os.path.isdir(os.path.join(src, i)):		
				if any(j for j in dst_files if j['title'] == i):
					temp = next(j for j in dst_files if j['title'] == i)
					matched.extend(self.push(os.path.join(src, i), temp['id']))
				else:
					# create folder
					temp = self.drive.mkdir(dst, i)
					matched.extend(self.push(os.path.join(src, i), temp['id']))
			# is file
			else:
				if not any(j for j in dst_files if j['title'] == i):
					matched.append(Task({
						'id': None,
						'title': i,
						'src': src,
						'dst': dst
					}))

		return matched

	def pull(self, src, dst):
		# var
		matched = []

		# ls
		src_files = self.drive.ls(src)
		dst_files = os.listdir(dst)
		
		for i in src_files:
			# folder
			if i['mimeType'] == 'application/vnd.google-apps.folder':
				# existed
				if any(j for j in dst_files if j == i['title'] and os.path.isdir(os.path.join(dst, j))):
					temp = next(j for j in dst_files if j == i['title'])
					matched.extend(self.pull(i['id'], os.path.join(dst, temp)))
				# not existed
				else:
					os.mkdir(os.path.join(dst, i['title']))
					matched.extend(self.pull(i['id'], os.path.join(dst, i['title'])))
			# not folder
			elif not any(j for j in dst_files if j == i['title'] and not os.path.isdir(os.path.join(dst, j))):
				matched.append(Task({
					'id': i['id'],
					'title': i['title'],
					'src': None,
					'dst': dst
				}))

		return matched

# rename
match = Match()