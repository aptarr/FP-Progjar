import flet as ft
from cli import cc

def group_chat():        
    def back(e):
        e.page.go("/dashboard")
        
    def add_file(e):
        e.page.go("/dashboard")
        
    def send_message(e):
        e.page.go("/dashboard")
        
    def download_file(e):
        e.page.go("/dashboard")
    
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
                ft.Text("Group Chat", size=18),
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
                        content=ft.Column(
                            controls=[
                                ft.Text("Yanto", size=14, color=ft.colors.WHITE),
                                ft.Text(
                                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed varius feugiat elementum.",
                                    size=14,
                                    color=ft.colors.WHITE
                                )
                            ]
                        ),
                        padding=ft.padding.all(10),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=ft.colors.RED_300,
                        margin=ft.margin.all(5),
                        width=200,
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed varius feugiat elementum.",
                            size=14,
                            color=ft.colors.BLACK
                        ),
                        padding=ft.padding.all(10),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=ft.colors.GREY_200,
                        margin=ft.margin.all(5),
                        width=200,
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Lorem ipsum dolor sit amet.",
                            size=14,
                            color=ft.colors.BLACK
                        ),
                        padding=ft.padding.all(10),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=ft.colors.GREY_200,
                        margin=ft.margin.all(5),
                        width=200,
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Agus", size=14, color=ft.colors.WHITE),
                                ft.Row(
                                    controls=[
                                        ft.Text("file.txt", size=14, color=ft.colors.WHITE),
                                        ft.Text("200 Kb", size=14, color=ft.colors.WHITE),            
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
                                    bgcolor=ft.colors.GREY_200,
                                    margin=ft.margin.symmetric(vertical=5),
                                    width=200,
                                    on_click=download_file
                                )
                            ]
                        ),
                        padding=ft.padding.all(10),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=ft.colors.RED_300,
                        margin=ft.margin.all(5),
                        width=200,
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Agus", size=14, color=ft.colors.WHITE),
                                ft.Text(
                                    "Lorem ipsum dolor sit amet.",
                                    size=14,
                                    color=ft.colors.WHITE
                                )
                            ]
                        ),
                        padding=ft.padding.all(10),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=ft.colors.RED_300,
                        margin=ft.margin.all(5),
                        width=200,
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("file.txt", size=14, color=ft.colors.RED_300),
                                        ft.Text("200 Kb", size=14, color=ft.colors.RED_300),            
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
                                    on_click=download_file
                                )
                            ]
                        ),
                        padding=ft.padding.all(10),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=ft.colors.GREY_200,
                        margin=ft.margin.all(5),
                        width=200,
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
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