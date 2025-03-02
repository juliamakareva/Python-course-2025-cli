import flet as ft
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Row,
    Text,
    icons,
)

from manager import copy, delete, move_file, search, count_files, get_size, analyze, organize

def main(page: ft.Page):
    page.title = "File Manager"
    image_path = "Smartphone_icon_17_File_Manager-512.webp"
    image = ft.Image(src=image_path, width=150, height=150)
    page.window_width = 600
    page.window_height = 700
    page.bgcolor = "white"

    title = ft.Text(
        value="Welcome to the File Manager!",
        color="#36454F",
        size=28,
        italic=True,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )




ft.app(target=main)
