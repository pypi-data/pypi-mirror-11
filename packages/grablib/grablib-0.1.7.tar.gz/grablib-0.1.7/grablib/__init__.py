import argparse

from .grab import grab
from .version import VERSION

parser = argparse.ArgumentParser(description="""grablib

Utility for defining then downloading, concatenating and minifying your
projects external library files eg. Javascript, CSS.

grablib Version: %s
(https://github.com/samuelcolvin/grablib).
All optional arguments can also be set in the definition file.

""" % VERSION, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-d', '--download-root', action='store', dest='download_root',
                    help='Root directory to put downloaded files in, defaults to "./static/".')

parser.add_argument('-m', '--minified-root', action='store', dest='minified_root',
                    help='Root directory to put minified and concatenated files in, defaults to "./static/minifed/".')

parser.add_argument('-w', '--overwrite', action='store_true', dest='overwrite',
                    help='Overwrite existing files, default is not to download a library if the file already exists')

parser.add_argument('-p', '--file-permissions', action='store', dest='file_permissions',
                    help='Explicitly set file permission for each file downloaded, eg. 666')

parser.add_argument('-v', '--verbosity', action='store', choices=['0', '1', '2', '3'], dest='verbosity',
                    help='Verbosity Level 0 (nothing except errors), 1 (a little), 2 (default), 3 (everything)')

parser.add_argument('--no-colour', action='store_false', default=True, dest='colour_print',
                    help='Do not use color term to colourise output')

parser.add_argument('lib_def', metavar='file-path-or-json', default='grablib.json', nargs='?',
                    help='path to JSON or python file or valid JSON string, defaults to "grablib.json".')


def run_cmd_arguments(args_namespace=None, from_command_line=True):
    args_namespace = args_namespace or parser.parse_args()
    options = vars(args_namespace)
    return grab(from_command_line=from_command_line, **options)
