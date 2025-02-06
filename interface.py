import argparse
from manager import copy, delete, move_file, show_files, search, count_files, rename, rename_with_recursion, \
    get_creation_time, get_size, analyze, organize


def main():
    parser = argparse.ArgumentParser(prog='File_Manager',
                                     description='A simple program working with files in Python')

    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_copy = subparsers.add_parser("copy", help="Copy a file")
    parser_copy.add_argument("src", help="Source file")
    parser_copy.add_argument("dst", help="Destination file")

    # Adding a command for delete
    parser_delete = subparsers.add_parser("delete", help="Delete a file or folder")
    parser_delete.add_argument("src", help="Source file or folder to delete")

    # Adding a move command
    parser_move = subparsers.add_parser("move", help="Move a file or folder")
    parser_move.add_argument("src", help="Source file or folder")
    parser_move.add_argument("dst", help="Destination location")

    # Adding a command to show files
    parser_show_files = subparsers.add_parser("show", help="Show a file or folder")
    parser_show_files.add_argument("src", help="Source file or folder to show")

    # Adding a command to search files/folder with a filter

    parser_search = subparsers.add_parser("search", help="Search a file or a folder with a specific filter")
    parser_search.add_argument("src", help="Source folder")
    parser_search.add_argument("pattern", help="Which filter should be used for a search")

    # Adding a command to count files
    parser_count_files = subparsers.add_parser("count", help="Count the number of files")
    parser_count_files.add_argument("src", help="Filepath")
    # Adding a command to rename files
    parser_rename = subparsers.add_parser("rename", help="Rename a file")
    parser_rename.add_argument("src", help="File's source")
    parser_rename.add_argument("--recursive", action="store_true", help="Rename a whole folder")
    # Adding a command to get a size
    parser_get_size = subparsers.add_parser("get_size", help="Show the size of files")
    parser_get_size.add_argument("src", help="Filepath")
    # Adding a command to analyze the size of files
    parser_analyze = subparsers.add_parser("analyze", help="Analyze the size of files")
    parser_analyze.add_argument("src", help="Filepath")

    parser_organize = subparsers.add_parser("organize", help="Organize the files using their extensions")
    parser_organize.add_argument("unorganized_folder", help="Insert the path to an unorganized_folder")

    args = parser.parse_args()

    #
    if args.command == "copy":
        copy(args.src, args.dst)
    elif args.command == "delete":
        delete(args.src)
    elif args.command == "move":
        move_file(args.src, args.dst)
    elif args.command == "show":
        show_files(args.src)
    elif args.command == "search":
        print(search(args.src, args.pattern))
    elif args.command == "count":
        print(count_files(args.src))

    elif args.command == "rename":
        if args.recursive:
            rename_with_recursion(args.src)
        else:
            rename(args.src)
    elif args.command == "get_size":
        print(get_size(args.src))
    elif args.command == "analyze":
        analyze(args.src)

    elif args.command == "organize":
        organize(args.unorganized_folder)

    else:
        print("Error : wrong arguments")


if __name__ == "__main__":
    main()
