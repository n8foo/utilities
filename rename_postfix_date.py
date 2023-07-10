#! /usr/bin/env python3

import os
import argparse
import subprocess
from datetime import datetime

def get_birthtime(file_path, debug=False):
    stat = os.stat(file_path)
    try:
        birthtime = stat.st_birthtime
    except AttributeError:
        # Some macOS versions use st_birthtimespec instead of st_birthtime
        birthtime = stat.st_birthtimespec.tv_sec

    if debug:
        birth_datetime = datetime.fromtimestamp(birthtime)
        print(f"Birthtime for {file_path}: {birth_datetime}")

    return birthtime

def rename_files(file_list, remove_prefix, set_modification_time, debug=False):
    for file_path in file_list:
        if os.path.isfile(file_path):
            directory, filename = os.path.split(file_path)

            birth_time = get_birthtime(file_path, debug=debug)
            birth_datetime = datetime.fromtimestamp(birth_time)
            date_string = birth_datetime.strftime('%Y-%m-%d')

            base_name, extension = os.path.splitext(filename)
            if ' ' in base_name:
                separator = ' - '
            else:
                separator = '_'

            if remove_prefix:
                prefix_parts = base_name.split(separator)
                if len(prefix_parts) > 1 and prefix_parts[0].isdigit():
                    base_name = separator.join(prefix_parts[1:])

            if set_modification_time:
                touch_cmd = ['touch', '-mt', birth_datetime.strftime('%Y%m%d%H%M.%S'), file_path]
                print(touch_cmd)
                subprocess.run(touch_cmd, check=True)

            # Check if date is already present at the end of the filename
            if base_name.endswith(f'{separator}{date_string}'):
                continue  # Skip renaming if date is already appended

            new_name = f'{base_name}{separator}{date_string}{extension}'
            new_file_path = os.path.join(directory, new_name)
            os.rename(file_path, new_file_path)

            if set_modification_time:
                touch_cmd = ['touch', '-mt', birth_datetime.strftime('%Y%m%d%H%M.%S'), new_file_path]
                print(touch_cmd)
                subprocess.run(touch_cmd, check=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename files based on birth or creation date')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+', help='list of files to rename')
    parser.add_argument('-r', '--remove-prefix', action='store_true', help='remove existing year prefix')
    parser.add_argument('-s', '--set-modification-time', action='store_true', help='set modification time to birth or creation time')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debug mode')
    args = parser.parse_args()

    rename_files(args.files, args.remove_prefix, args.set_modification_time, debug=args.debug)
