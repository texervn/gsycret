import os

# constant
__temp__ = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + '/temp/'

# pattern
ls_pattern = '"{id}" in parents and trashed = false'
log_pattern = '{module}.{func}: {msg}'
file_pattern = '{path}/{title}'