import os
import re
import shutil
from datetime import datetime
from functools import wraps


def copy(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
        print(f"The folder '{src}' has been copied to '{dst}'")
    elif os.path.isfile(src):
        shutil.copy(src, dst)
        print(f"Your file '{src}' has been copied to '{dst}'")
    else:
        print(f"Error: file or folder doesn't exist")


def move_file(src, dst):
    """The function is used to move files"""
    shutil.move(src, dst)
    print(f"Your file/folder'{src}' has been moved to  '{dst}'")


def delete(src):
    if os.path.isdir(src):  # Проверяем, является ли `src` папкой
        shutil.rmtree(src)  # Удаляем папку и всё её содержимое
        print(f"Папка '{src}' удалена")
    elif os.path.isfile(src):  # Проверяем, является ли `src` файлом
        os.remove(src)  # Удаляем файл
        print(f"Файл '{src}' удалён")
    else:
        print("Ошибка: файл или папка не найдены")


def count_files(src):
    total = 0
    for root, dirs, files in os.walk(src):
        total += len(files)
    return total


def show_files(src):
    print(*os.listdir(src))


def search(src, pattern):
    searched_files = []
    for address, dirs, files in os.walk(src):
        for file in files:
            if re.search(pattern, file):
                searched_files.append(os.path.join(address, file))
    print(searched_files)


def get_creation_time(path):
    creation_time = os.path.getctime(path)
    return datetime.fromtimestamp(creation_time).strftime('%d-%m-%Y_%H-%M-%S')


def rename(src):
    creation_time = get_creation_time(src)
    name, ext = os.path.splitext(src)
    new_filename = f"{name}_{creation_time}{ext}"
    os.rename(src, new_filename)


def rename_with_recursion(src):
    for root, dirs, files in os.walk(src):
        for file in files:
            file_path = os.path.join(root, file)
            rename(file_path)


def convert_size(func):
    """ Decorator that converts the size of a file/a folder from bytes to KB, MB, GB etc"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        size_in_bytes = func(*args, **kwargs)
        if size_in_bytes < 1024:
            return f"{size_in_bytes} B"
        elif size_in_bytes < 1024 ** 2:
            return f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 ** 3:
            return f"{size_in_bytes / 1024 ** 2:.2f} MB"
        elif size_in_bytes < 1024 ** 4:
            return f"{size_in_bytes / 1024 ** 3:.2f} GB"
        else:
            return f"{size_in_bytes / 1024 ** 4:.2f} TB"

    return wrapper


@convert_size
def get_size(src):
    total_size = 0
    if os.path.isfile(src):
        total_size = os.path.getsize(src)
    elif os.path.isdir(src):
        for root, dirs, files in os.walk(src):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
    return total_size


def analyze(src):
    files = {}

    # Проходим по файлам/папкам в указанной директории
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        size = get_size(file_path)
        files[file] = size  # Сохраняем имя файла и его размер в словарь

    for file, size in files.items():
        print(f"{file}: {size}")

