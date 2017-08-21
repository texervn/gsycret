from gsycret.cli import *
from gsycret.match import *
from gsycret.client import *

def main():
	# var
	args = parse_argv()
	client = Client(args)
	
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