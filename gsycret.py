from gsycret.cli import *
from gsycret.match import *
from gsycret.client import *

def main():
	# var
	args = parse_argv()

	client = Client()

	if args.command == 'push':
		client.push.init(
			src = args.source,
			dst = args.destination
		)
		client.push.run(
			auto = args.auto,
			password = args.password,
			threads_num = args.threads_num
		)
	elif args.command == 'pull':
		client.push.init(
			src = args.source,
			dst = args.destination
		)
		client.push.run(
			auto = args.auto,
			password = args.password,
			threads_num = args.threads_num
		)
	elif args.command == 'merge':
		client.merge.init(
			src = args.source,
			dst = args.destination
		)
		client.merge.run(
			threads_num = args.threads_num
		)

if __name__ == '__main__':
	main()