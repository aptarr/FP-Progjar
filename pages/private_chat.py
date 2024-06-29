import flet as ft
import json
from cli import cc

def private_chat(id):        
    def back(e):
        e.page.go("/dashboard")
        
    def add_file(e):
        e.page.go("/dashboard")
        
    def send_message(e):
        e.page.go("/dashboard")
        
    def download_file(e):
        e.page.go("/dashboard")
        
    def get_msgs():
        result = cc.proses(f"inbox {id}")
        if result.startswith("Error"):
            return []
        else:
            return json.loads(result)
        
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
                ft.Text([member for member in chat_data["member"] if member != chat_data["name"]][0], size=18)
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(10),
    )
    chat_bubbles = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            message['message'],
                            size=14,
                            color=ft.colors.WHITE if message['sender'] != chat_data['name'] else ft.colors.BLACK
                        ),
                        padding=ft.padding.all(10),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=ft.colors.RED_300 if message['sender'] != chat_data['name'] else ft.colors.GREY_200,
                        margin=ft.margin.all(5),
                        width=200,
                    )
                ],
                alignment=ft.MainAxisAlignment.START if message['sender'] != chat_data['name'] else ft.MainAxisAlignment.END
            )
            for message in chat_data['message']
        ],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )
    add_file = ft.Container(
        content=ft.Icon(
            name=ft.icons.ADD,
            size=30,
            color=ft.colors.GREY
        ),
        on_click=add_file
    )
    message_field = ft.TextField(
        label="Your message", 
        width=240, 
        height=50, 
        bgcolor="#f7f7fc", 
        border_radius=15, 
        border_color=ft.colors.TRANSPARENT, 
        filled=True
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
                add_file,
                message_field,
                send_button
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(10),
        bgcolor=ft.colors.GREY_100
    )
    
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