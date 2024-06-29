import flet as ft
from cli import cc

def new_chat():
    def back(e):
        e.page.go("/dashboard")
        
    def handle_search(e):
        e.page.update()
        
    def go_to_private_chat(e):
        e.page.go("/private_chat")
        
    def join_group(e):
        e.page.go("/join_group")
        
    def create_group(e):
        e.page.go("/create_group")
    
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
                ft.Text("New Chat", size=18),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(10),
    )
    search_field = ft.TextField(
        label="Search", 
        width=280, 
        height=40, 
        bgcolor="#a4a4a4, 0.2",
        border_radius=15, 
        border_color=ft.colors.TRANSPARENT, 
        filled=True
    )
    search_button = ft.IconButton(
        icon=ft.icons.SEARCH,
        icon_color=ft.colors.WHITE,
        bgcolor=ft.colors.RED,
        on_click=handle_search,
        width=40,
        height=40,
        padding=10,
    )
    search_bar = ft.Container(
        content=ft.Row(
            controls=[search_field, search_button],
            spacing=0,
        ),
        padding=ft.padding.symmetric(horizontal=10)
    )
    plus_icon = ft.Icon(
        name=ft.icons.ADD,
        size=50,
        color=ft.colors.RED
    )
    create_group_container = ft.Container(
        content=ft.Row(
            controls=[
                plus_icon,
                ft.Column(
                    controls=[
                        ft.Text("Create New Group", size=16),
                        ft.Text("Create Group", size=14, color=ft.colors.GREY)
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                )
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(10),
        on_click=create_group,
        ink=True,
        bgcolor=ft.colors.GREY_100,
        border_radius=15,
        margin=ft.margin.symmetric(horizontal=10)
    )
    profile_icon = ft.Icon(
        name=ft.icons.ACCOUNT_CIRCLE,
        size=50,
        color=ft.colors.GREY
    )
    chat_container = ft.Container(
        content=ft.Row(
            controls=[
                profile_icon,
                ft.Column(
                    controls=[
                        ft.Text("Username", size=16),
                        ft.Text("Last message", size=14, color=ft.colors.GREY)
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                )
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(10),
        on_click=go_to_private_chat,
        ink=True,
        bgcolor=ft.colors.GREY_100,
        border_radius=15,
        margin=ft.margin.symmetric(horizontal=10)
    )
    group_container = ft.Container(
        content=ft.Row(
            controls=[
                profile_icon,
                ft.Column(
                    controls=[
                        ft.Text("Groupname", size=16),
                        ft.Text("Last message", size=14, color=ft.colors.GREY)
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                )
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(10),
        on_click=join_group,
        ink=True,
        bgcolor=ft.colors.GREY_100,
        border_radius=15,
        margin=ft.margin.symmetric(horizontal=10)
    )
    chat_list_view = ft.ListView(
        controls = [
            create_group_container,
            chat_container,
            chat_container,
            group_container,
        ],
        padding=10,
        spacing=10,
        expand=True
    )
    
    return ft.Column(
        controls = [
            top_bar,
            search_bar,
            ft.Container(content=chat_list_view, expand=True)
        ],
        expand=True
    )