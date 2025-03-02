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

    page.add(
        ft.Column([
            image,
            title,
            Row([
                ElevatedButton("Pick File", bgcolor="#36454F", icon=icons.UPLOAD_FILE,
                               on_click=lambda _: pick_files_dialog.pick_files()),  # Bouton pour choisir un fichier
                ElevatedButton("Pick Directory", bgcolor="#36454F", icon=icons.FOLDER_OPEN,
                               on_click=lambda _: pick_directory_dialog.get_directory_path()),
                # Bouton pour choisir un répertoire
            ], alignment=ft.MainAxisAlignment.CENTER),  # Centrer les boutons dans la ligne

        ],
            expand=True,  # Permet à la colonne d'occuper tout l'espace disponible
            alignment=ft.MainAxisAlignment.CENTER,  # Centrer le contenu de la colonne verticalement
            horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centrer horizontalement
        )
 )

ft.app(target=main)
