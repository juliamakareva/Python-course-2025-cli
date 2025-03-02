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
            operation_input.visible = True
            confirm_button.visible = True
            help_button.visible = True
            page.update()

    def pick_directory_result(e: FilePickerResultEvent):
        if e.path:
            selected_source.value = e.path
            selected_source.update()
            operation_input.visible = True
            confirm_button.visible = True
            help_button.visible = True
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

    # buttons settings

    confirm_button = ft.ElevatedButton("Confirm", on_click=lambda e: confirm_operation(), bgcolor="#829F82",
                                       color="white", visible=False)
    help_button = ft.ElevatedButton("Help", on_click=lambda e: show_help(), bgcolor="#B06500", color="white",
                                    visible=False)
    execute_button = ft.ElevatedButton("Execute", on_click=lambda e: execute_operation(), bgcolor="green",
                                       color="white", visible=False)
    cancel_button = ft.ElevatedButton("Cancel", on_click=lambda e: cancel_operation(), bgcolor="red", color="white",
                                      visible=False)
    pick_destination_button = ft.ElevatedButton("Pick Destination", bgcolor="#36454F",
                                                on_click=lambda _: pick_destination_dialog.get_directory_path(),
                                                visible=False)

    # help configuration
    def show_help():
        page.dialog = help_dialog
        help_dialog.open = True
        page.update()

    def close_help(e):
        help_dialog.open = False
        page.update()

    help_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Operations list"),
        content=ft.Column([ft.Text(name) for name, _ in operations.values()], spacing=10),
        actions=[ft.TextButton("OK", on_click=close_help)],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def confirm_operation():
        user_input = operation_input.value.strip().lower()
        if user_input in operations:
            execute_button.visible = True
            cancel_button.visible = True
            confirm_button.visible = False
            help_button.visible = False
            output_text.value = f" Press Execute to launch {operations[user_input][0].lower()} operation."
            if user_input in ["copy", "move"]:
                pick_destination_button.visible = True
            elif user_input == "search":
                search_pattern_input.visible = True  # filter input for search function
            page.update()
        else:
            output_text.value = "⚠ Invalid operation! Check the Help menu."
            page.update()

    def execute_operation():
        user_input = operation_input.value.strip().lower()
        file_path = selected_source.value.strip()

        if user_input in operations:
            operation_name, function = operations[user_input]
            try:
                if user_input in ["copy", "move"]:
                    if dst_path.value == "No destination selected":
                        output_text.value = "⚠ Please select a destination path."
                        page.update()
                        return
                    function(file_path, dst_path.value)
                elif user_input == "search":
                    pattern = search_pattern_input.value.strip()
                    if not pattern:
                        output_text.value = "⚠ Please enter a valid search pattern."
                        page.update()
                        return
                    # Appeler la fonction search() avec le motif
                    search_results = search(file_path, pattern)
                    if search_results:
                        output_text.value = f"🔍 Found the following files:\n" + "\n".join(search_results)
                    else:
                        output_text.value = "⚠ No files found matching the pattern."
                elif user_input == "analyze":
                    result = function(file_path)  # Appeler la fonction d'analyse
                    output_text.value = f"✅ {operation_name} completed! Result: {result if result else 'Check your terminal'}"
                else:
                    result = function(file_path)
                    output_text.value = f"✅ {operation_name} completed! Result: {result if result else 'Done'}"
                page.update()
            except Exception as err:
                output_text.value = f"❌ : {err}"
                page.update()
        else:
            output_text.value = "⚠ Invalid operation! Check the Help menu."
            page.update()

    def cancel_operation():
        """to reset all and back to the welcome page """
        execute_button.visible = False
        cancel_button.visible = False
        pick_destination_button.visible = False
        output_text.value = ""
        operation_input.visible = False
        search_pattern_input.visible = False
        selected_source.value = ""
        dst_path.value = ""
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
                confirm_button,
                help_button
            ], alignment=ft.MainAxisAlignment.CENTER),
            Row([
                execute_button,
                cancel_button
            ], alignment=ft.MainAxisAlignment.CENTER),
            pick_destination_button,
            dst_path,
            search_pattern_input,
            output_text,
        ], expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )


ft.app(target=main)
