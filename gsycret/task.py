class Task:
	def __init__(self, **kwargs):
		self.id = kwargs['id']
		self.title = kwargs['title']
		self.src = kwargs['src']
		self.dst = kwargs['dst']