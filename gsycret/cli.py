import argparse

# constant
__version__ = '1.0'
__description__ = 'gsycret - script for google drive with encryption'
__epilog__ = 'Report bugs to <cjyeh@cs.nctu.edu.tw>'

def parse_argv():
	# init
	parser = argparse.ArgumentParser(
		description=__description__,
		epilog=__epilog__
	)

	# main parser
	parser.add_argument(
		'-v', '-V', '--version', 
		action='version', 
		help='Print program version', 
		version='v{}'.format(__version__)
	)

	# sub parser
	subparsers = parser.add_subparsers(
		dest='command',
		help='command help'
	)
	subparsers.required = True

	# push
	parser_push = subparsers.add_parser('push')
	parser_push.add_argument('source')
	parser_push.add_argument('destination')
	parser_push.add_argument(
		'-r', '--recursive',
		action = 'store_true',
		help = 'copy directories recursively'
	)
	parser_push.add_argument(
		'-p', '--password', 
		action = 'store', 
		help = 'password for encryption'
	)
	parser_push.add_argument(
		'-a', '--auto', 
		action = 'store_true', 
		help = 'automatic encryption', 
		default = False
	)
	parser_push.add_argument(
		'-t', '--threads_num', 
		action = 'store', 
		help = 'number of threads', 
		type=int, 
		default=4
	)

	# pull
	parser_pull = subparsers.add_parser('pull')
	parser_pull.add_argument('source')
	parser_pull.add_argument('destination')
	parser_pull.add_argument(
		'-p', '--password', 
		action = 'store', 
		help = 'password for decryption'
	)
	parser_pull.add_argument(
		'-a', '--auto', 
		action = 'store_true', 
		help = 'automatic decryption', 
		default = False
	)
	parser_pull.add_argument(
		'-t', '--threads_num', 
		action = 'store', 
		help = 'number of threads', 
		type = int, 
		default = 4
	)

	# merge
	parser_merge = subparsers.add_parser('merge')
	parser_merge.add_argument('source')
	parser_merge.add_argument('destination')
	parser_merge.add_argument(
		'-a', '--auto', 
		action = 'store_true', 
		help = 'automatic encryption and decryption', 
		default = False
	)
	parser_merge.add_argument(
		'-t', '--threads_num', 
		action = 'store', 
		help = 'number of threads', 
		type = int, 
		default = 4
	)

	results = parser.parse_args()

	return results