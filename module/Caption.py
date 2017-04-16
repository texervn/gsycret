import os
import re
import subprocess

# constant
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'

# find caption which match video
def match_caption(video, captions):
	# var
	name = None
	episode = re.findall(r'[eE]\d+', video)

	if episode == []:
		episode = re.findall(r'\d+', video)

	if len(episode) > 0:
		episode = episode[0]
	else:
		print('[%10s] %s' % ('Warning', 'Episode'))
		return None

	name = video[:video.find(episode)]
	name = re.sub('[^0-9a-zA-Z]+', '', name)
	name = name.lower()

	for caption in captions:
		temp = caption[:caption.find(episode)]
		temp = re.sub('[^0-9a-zA-Z]+', '', caption).lower()

		print(temp)

		if name in temp:
			return caption

	return None

# to .ass
def srt_to_ass(var):
	title = var.replace('.srt', '')
	subprocess.call(['ffmpeg', '-i', PATH + var, PATH + title + '.ass'])
	os.remove(var)

def hardcode(video, caption):
	# init
	title = video[:video.rfind('.')]

	subprocess.call(['ffmpeg', '-i', video, '-vf', 'ass=' + caption, '-strict', '-2', title + '-s.mp4'])