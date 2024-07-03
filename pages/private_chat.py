import flet as ft
import json
import os
import shutil
import base64
from cli import cc

def private_chat(page: ft.Page, id):
    def back(e):
        e.page.go("/dashboard")

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            file_path = file.name
            shutil.copy(file.path, file_path)
            result = cc.proses(f"sendfile {id} {file_path} {file}")
            print(result)
            update_chat()
            chat_bubbles.scroll_to(offset=-1, duration=300)
            page.update()
            os.remove(file_path)

    def download_file(file_path):
        file_name = os.path.basename(file_path)
        result = cc.proses(f"getfile {id} {file_name}")
        print(result)

    def send_message(e):
        message = message_field.value
        if (message != ''):
            cc.proses(f"sendmsg {id} {message}")
            message_field.value = ""
            update_chat()
            e.page.update()

    def get_msgs():
        result = cc.proses(f"inbox {id}")
        if result.startswith("Error"):
            return []
        else:
            return json.loads(result)

    def update_chat():
        nonlocal chat_data, chat_bubbles
        chat_data = get_msgs()
        chat_bubbles.controls = []

        for message in chat_data['message']:
            if message['isFile']:
                file_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(message['message'], size=14, color=ft.colors.WHITE if message['sender'] == chat_data['name'] else ft.colors.BLACK),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Text("Download", size=14, color=ft.colors.RED_300),
                                        ft.Icon(ft.icons.DOWNLOAD, size=18, color=ft.colors.RED_300)
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=ft.border_radius.all(15),
                                bgcolor=ft.colors.RED_50,
                                margin=ft.margin.symmetric(vertical=5),
                                width=200,
                                on_click=lambda _: download_file(message['message'])
                            )
                        ]
                    ),
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(15),
                    bgcolor=ft.colors.RED_300 if message['sender'] == chat_data['name'] else ft.colors.GREY_200,
                    margin=ft.margin.all(5),
                    width=200,
                )
                bubble = file_container
            else:
                bubble = ft.Container(
                    content=ft.Text(
                        message['message'],
                        size=14,
                        color=ft.colors.WHITE if message['sender'] == chat_data['name'] else ft.colors.BLACK
                    ),
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(15),
                    bgcolor=ft.colors.RED_300 if message['sender'] == chat_data['name'] else ft.colors.GREY_200,
                    margin=ft.margin.all(5),
                    width=200,
                )
            
            chat_bubbles.controls.append(
                ft.Row(
                    controls=[bubble],
                    alignment=ft.MainAxisAlignment.START if message['sender'] == chat_data['name'] else ft.MainAxisAlignment.END
                )
            )
        
        if hasattr(chat_bubbles, '__page') and chat_bubbles.__page:
            chat_bubbles.update()

    chat_data = get_msgs()

    top_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(
                        name=ft.icons.ARROW_BACK_IOS,
                        size=18,
                        color=ft.colors.BLACK,
                    ),
                    on_click=back
                ),
                ft.Text(chat_data['name'], size=18)
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(10),
    )

    chat_bubbles = ft.Column(
        controls=[],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    add_file_button = ft.Container(
        content=ft.Icon(name=ft.icons.ADD, size=30, color=ft.colors.GREY),
        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True),
    )

    message_field = ft.TextField(
        label="Your message", 
        width=240, 
        height=50, 
        bgcolor="#f7f7fc", 
        border_radius=15, 
        border_color=ft.colors.TRANSPARENT, 
        filled=True,
        color=ft.colors.BLACK
    )

    send_button = ft.Container(
        content=ft.Icon(
            name=ft.icons.SEND,
            size=30,
            color=ft.colors.RED_300
        ),
        on_click=send_message
    )

    send_message_container = ft.Container(
        content=ft.Row(
            controls=[
                add_file_button,
                message_field,
                send_button
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(10),
        bgcolor=ft.colors.GREY_100
    )
    
    update_chat()

    return ft.Column(
        controls=[
            top_bar,
            chat_bubbles,
            send_message_container,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True
    )
