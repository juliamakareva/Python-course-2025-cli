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

    # selected file or folder
    selected_source = Text("")
    dst_path = Text("")
    output_text = ft.Text("", color="red")

    # pattern for a search function ( filter field)
    search_pattern_input = ft.TextField(hint_text="Enter search pattern", width=200, visible=False)

    def pick_files_result(e: FilePickerResultEvent):
        if e.files:
            selected_source.value = e.files[0].path
            selected_source.update()

            page.update()

    def pick_directory_result(e: FilePickerResultEvent):
        if e.path:
            selected_source.value = e.path
            selected_source.update()

            page.update()

    def pick_destination_result(e: FilePickerResultEvent):
        if e.path:
            dst_path.value = e.path
            dst_path.update()
            page.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    pick_directory_dialog = FilePicker(on_result=pick_directory_result)
    pick_destination_dialog = FilePicker(on_result=pick_destination_result)
    page.overlay.extend([pick_files_dialog, pick_directory_dialog, pick_destination_dialog])

    # operations list
    operations = {
        "copy": ("📋 Copy", copy),
        "move": ("📂 Move File --move", move_file),
        "delete": ("🗑 Delete", delete),
        "search": ("🔍 Search", search),
        "count": ("📁 Count Files -- count", count_files),
        "size": ("📏 Get Size -- size", get_size),
        "analyze": ("📊 Analyze", analyze),
        "organize": ("🗃 Organize", organize)
    }

    operation_input = ft.TextField(hint_text="Define your operation ...", width=200, visible=False)

    def confirm_operation():
        user_input = operation_input.value.strip().lower()
        if user_input in operations:
            output_text.value = f" Press Execute to launch {operations[user_input][0].lower()} operation."
        else:
            output_text.value = "⚠ Invalid operation! Check the Help menu."
            page.update()

    page.add(
        ft.Column([
            image,
            title,
            Row([
                ElevatedButton("Pick File", bgcolor="#36454F", icon=icons.UPLOAD_FILE,
                               on_click=lambda _: pick_files_dialog.pick_files()),
                ElevatedButton("Pick Directory", bgcolor="#36454F", icon=icons.FOLDER_OPEN,
                               on_click=lambda _: pick_directory_dialog.get_directory_path()),
            ], alignment=ft.MainAxisAlignment.CENTER),
            selected_source,
            Row([
                operation_input,

            ], alignment=ft.MainAxisAlignment.CENTER),
            Row([

            ], alignment=ft.MainAxisAlignment.CENTER),
            dst_path,
            search_pattern_input,
            output_text,
        ], expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

    ft.app(target=main)
