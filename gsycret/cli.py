import argparse

import argparse

# constant
__version__ = '1.0'
__description__ = 'gsycret - script for google drive api with encryption'
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
		dest='mode',
		help='mode help'
	)

	# push
	parser_push = subparsers.add_parser('push')
	parser_push.add_argument('source')
	parser_push.add_argument('destination')
	parser_pull.add_argument('--password', action='store', help='password for encryption')
	parser_pull.add_argument('--auto', action='store_true', help='automatic encryption', default=False)
	parser_pull.add_argument('--threads_num', action='store', help='number of threads', type=int, default=4)

	# pull
	parser_pull = subparsers.add_parser('pull')
	parser_pull.add_argument('source')
	parser_pull.add_argument('destination')
	parser_pull.add_argument('--password', action='store', help='password for decryption')
	parser_pull.add_argument('--auto', action='store_true', help='automatic decryption', default=False)
	parser_pull.add_argument('--threads_num', action='store', help='number of threads', type=int, default=4)

	results = parser.parse_args()

	return results.__dict__