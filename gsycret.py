from gsycret.cli import *
from gsycret.match import *
from gsycret.client import *

def main():
	# var
	args = parse_argv()

	client = Client()

	client.pull.init(
		src = args.source,
		dst = args.destination
	)

	client.pull.run(
		auto = args.auto,
		password = args.password,
		threads_num = args.threads_num,
	)

if __name__ == '__main__':
	main()