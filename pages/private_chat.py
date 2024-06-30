import flet as ft
import json
import os
import shutil
import base64
from cli import cc

def private_chat(page: ft.Page, id):
    # Function to handle navigating back
    def back(e):
        e.page.go("/dashboard")

    # Function to handle file picking result
    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]  # Get the first selected file

            upload_dir = "uploaded_files"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save the file locally
            file_path = os.path.join(upload_dir, file.name)
            shutil.copy(file.path, file_path)

            # Process file sending
            result = cc.proses(f"sendfile {id} {file_path} {file}")
            print(result)
            
            # Update chat interface and scroll to latest message
            update_chat()
            chat_bubbles.scroll_to(offset=-1, duration=300)
            page.update()

            # Delete the file after copying
            os.remove(file_path)

    # Function to handle file downloading
    def download_file(file_path):
        file_name = os.path.basename(file_path)

        # Process file sending
        result = cc.proses(f"getfile {id} {file_name}")
        print(result)

    # Function to handle sending a message
    def send_message(e):
        message = message_field.value
        cc.proses(f"sendmsg {id} {message}")
        message_field.value = ""
        update_chat()
        e.page.update()

    # Function to fetch messages from server
    def get_msgs():
        result = cc.proses(f"inbox {id}")
        if result.startswith("Error"):
            return []
        else:
            return json.loads(result)

    # Function to update chat interface
    def update_chat():
        nonlocal chat_data, chat_bubbles
        chat_data = get_msgs()
        chat_bubbles.controls = []

        for message in chat_data['message']:
            if message['isFile']:
                # File bubble
                file_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(message['message'], size=14, color=ft.colors.RED_300),
                                    # Add file size if available
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
                    bgcolor=ft.colors.GREY_200,
                    margin=ft.margin.all(5),
                    width=200,
                )
                bubble = file_container
            else:
                # Regular chat bubble
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
        
        # Update chat_bubbles if it's added to the page
        if hasattr(chat_bubbles, '__page') and chat_bubbles.__page:
            chat_bubbles.update()

    # Initialize chat data
    chat_data = get_msgs()

    # Create top bar control
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

    # Create chat bubbles control
    chat_bubbles = ft.Column(
        controls=[],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    # Create file picker dialog
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    # Add file picker dialog to page overlay
    page.overlay.append(pick_files_dialog)

    # Create add file button control
    add_file_button = ft.Container(
        content=ft.Icon(name=ft.icons.ADD, size=30, color=ft.colors.GREY),
        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True),
    )

    # Create message field control
    message_field = ft.TextField(
        label="Your message", 
        width=240, 
        height=50, 
        bgcolor="#f7f7fc", 
        border_radius=15, 
        border_color=ft.colors.TRANSPARENT, 
        filled=True
    )

    # Create send button control
    send_button = ft.Container(
        content=ft.Icon(
            name=ft.icons.SEND,
            size=30,
            color=ft.colors.RED_300
        ),
        on_click=send_message
    )

    # Create send message container control
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
    
    # Initialize chat interface on page load
    update_chat()

    # Return main column control with all components
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
