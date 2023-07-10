#! /usr/bin/env python3

import os
import argparse


def update_modification_time(filename, field):
    # Get the selected time field (birthtime or ctime)
    if field == "birthtime":
        time_field = os.stat(filename).st_birthtime
    elif field == "ctime":
        time_field = os.stat(filename).st_ctime
    else:
        print("Invalid time field selected.")
        return

    # Update the modification time of the file
    os.utime(filename, (time_field, time_field))
    print(f"Updated modification time of '{filename}' using {field}.")


def main():
    parser = argparse.ArgumentParser(description="Update modification time using birthtime or ctime.")
    parser.add_argument("files", nargs="+", help="Filename(s) to update modification time")
    parser.add_argument(
        "-b",
        "--birthtime",
        action="store_true",
        help="Use birthtime (creation time) to update modification time",
    )
    parser.add_argument(
        "-c",
        "--ctime",
        action="store_true",
        help="Use ctime (metadata change time) to update modification time",
    )

    args = parser.parse_args()

    files = args.files
    birthtime = args.birthtime
    ctime = args.ctime

    if birthtime and ctime:
        print("Only one time field can be selected. Choose either birthtime or ctime.")
        return

    if not birthtime and not ctime:
        print("No time field selected. Use either --birthtime or --ctime.")
        return

    field = "birthtime" if birthtime else "ctime"

    for file in files:
        if os.path.exists(file):
            update_modification_time(file, field)
        else:
            print(f"'{file}' does not exist.")


if __name__ == "__main__":
    main()
