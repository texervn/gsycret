from module.cli import *
from module.match import *
from module.client import *

def main():
	# var
	args = parse_argv()
	client = Client(None, args['threads_num'])
	
	print(args)

	if args['command'] == 'pull':
		list(map(client.q.put, match.pull(args['source'], args['destination'])))
		client.run('pull')
	elif args['command'] == 'push':
		list(map(client.q.put, match.push(args['source'], args['destination'])))
		client.run('push')
	elif args['command'] == 'merge':
		list(map(client.q.put, match.merge(args['source'], args['destination'])))
		client.run('merge')

if __name__ == '__main__':
	main()