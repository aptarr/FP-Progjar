import flet as ft
import json
from cli import cc

def dashboard():
    def handle_logout(e):
        result = cc.proses("logout")
        if result == "user logged out":
            e.page.go("/login")
            
    def get_all_last_msg():
        result = cc.proses("inboxall")
        if result.startswith("Error"):
            return []
        else:
            return json.loads(result)
    
    def handle_search(e):
        search_value = search_field.value
        if search_value == '':
            filtered_chat_data = chat_data
        else:
            filtered_chat_data = [chat for chat in chat_data if search_value.lower() in chat["name"].lower()]
        
        chat_list_view.controls.clear()
        chat_list_view.controls.append(new_chat_container)
        for chat in filtered_chat_data:
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
                                ft.Text(chat["name"], size=16),
                                ft.Text(chat["message"]["message"], size=14, color=ft.colors.GREY) if chat["message"] else ft.Text()
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.START
                        )
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(10),
                on_click=go_to_group_chat(chat["id"]) if chat["type"] == "group" else go_to_private_chat(chat["id"]),
                ink=True,
                bgcolor=ft.colors.GREY_100,
                border_radius=15,
                margin=ft.margin.symmetric(horizontal=10)
            )
            chat_list_view.controls.append(chat_container)
        e.page.update()
    
    def go_to_private_chat(id):
        def navigate(e):
            e.page.go(f"/private_chat/{id}")
        return navigate
        
    def go_to_group_chat(id):
        def navigate(e):
            e.page.go(f"/group_chat/{id}")
        return navigate
        
    def go_to_new_chat(e):
        e.page.go("/new_chat")
    
    top_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Your Chat", size=18),
                ft.TextButton(text="Logout", on_click=handle_logout),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
        filled=True,
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
    new_chat_container = ft.Container(
        content=ft.Row(
            controls=[
                plus_icon,
                ft.Column(
                    controls=[
                        ft.Text("Start New Chat", size=16, color=ft.colors.BLACK),
                        ft.Text("Find chat to start with", size=14, color=ft.colors.GREY_500)
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                )
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(10),
        on_click=go_to_new_chat,
        ink=True,
        bgcolor=ft.colors.GREY_100,
        border_radius=15,
        margin=ft.margin.symmetric(horizontal=10)
    )
    
    chat_data = get_all_last_msg()
    chat_containers = []
    for chat in chat_data:
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
                            ft.Text(chat["name"], size=16, color=ft.colors.BLACK),
                            ft.Text(chat["message"]["message"], size=14, color=ft.colors.GREY_700) if chat["message"] else ft.Text()
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.START
                    )
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(10),
            on_click=go_to_group_chat(chat["id"]) if chat["type"] == "group" else go_to_private_chat(chat["id"]),
            ink=True,
            bgcolor=ft.colors.GREY_100,
            border_radius=15,
            margin=ft.margin.symmetric(horizontal=10)
        )
        chat_containers.append(chat_container)
    
    chat_list_view = ft.ListView(
        controls=[new_chat_container] + chat_containers,
        padding=10,
        spacing=10,
        expand=True
    )
    
    return ft.Column(
        controls=[
            top_bar,
            search_bar,
            ft.Container(content=chat_list_view, expand=True)
        ],
        expand=True
    )