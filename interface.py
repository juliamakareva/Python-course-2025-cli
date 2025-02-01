import sys
import argparse
from manager import copy, delete, move_file, show_files, search, count_files, rename,rename_with_recursion, get_creation_time, get_size
from datetime import datetime
import shutil
import os
import sys
import re


def main():
    parser = argparse.ArgumentParser(prog='File_Manager',
                                     description='A simple program working with files in Python',
                                     epilog='Text at the bottom of help')

    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_copy = subparsers.add_parser("copy", help="Copy a file")
    parser_copy.add_argument("src", help="Source file")
    parser_copy.add_argument("dst", help="Destination file")

    # Добавление команды для удаления
    parser_delete = subparsers.add_parser("delete", help="Delete a file or folder")
    parser_delete.add_argument("src", help="Source file or folder to delete")

    # Добавление команды для перемещения
    parser_move = subparsers.add_parser("move", help="Move a file or folder")
    parser_move.add_argument("src", help="Source file or folder")
    parser_move.add_argument("dst", help="Destination location")

    parser_show_files = subparsers.add_parser("show", help="Show a file or folder")
    parser_show_files.add_argument("src", help="Source file or folder to show")

    parser_search = subparsers.add_parser("search", help="Search a file or a folder with a specific filter")
    parser_search.add_argument("src", help="Source folder")
    parser_search.add_argument("pattern", help="Which filter should be used for a search")

    parser_count_files = subparsers.add_parser("count", help="Count the number of files")
    parser_count_files.add_argument("src", help="Filepath")

    parser_rename = subparsers.add_parser("rename", help="Rename a file")
    parser_rename.add_argument("filepath", help="File")
    parser_rename.add_argument("--recursive", action="store_true",help="Rename a whole folder")

    parser_get_size = subparsers.add_parser("get_size", help="Show the size of files")
    parser_get_size.add_argument("filepath", help="Filepath")

    args = parser.parse_args()

    # Вызов соответствующей команды в зависимости от аргументов
    if args.command == "copy":
        copy(args.src, args.dst)
    elif args.command == "delete":
        delete(args.src)
    elif args.command == "move":
        move_file(args.src, args.dst)
    elif args.command == "show":
        show_files(args.src)
    elif args.command == "search":
        search(args.src, args.pattern)
    elif args.command == "count":
        print(count_files(args.src))

    elif args.command == "rename":
        if args.recursive:
            rename_with_recursion(args.filepath)
        else:
            rename(args.filepath)
    elif args.command == "get_size":
        print(get_size(args.filepath))

    else:
        print("Error : wrong arguments")


if __name__ == "__main__":
    main()
