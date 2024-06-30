import flet as ft
import json
from cli import cc

def new_chat():
    def back(e):
        e.page.go("/dashboard")
        
    def handle_search(e):
        search_value = search_field.value
        if search_value == '':
            filtered_chat_data = chat_data
        else:
            filtered_chat_data = [chat for chat in chat_data if search_value.lower() in chat["name"].lower()]
        
        chat_list_view.controls.clear()
        chat_list_view.controls.append(create_group_container)
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
                                ft.Text("Join this group", size=14, color=ft.colors.GREY) if chat["type"] == "group" else ft.Text("Start new chat", size=14, color=ft.colors.GREY)
                            ],
                            spacing=5,
                            alignment=ft.MainAxisAlignment.START
                        )
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.all(10),
                on_click=join_group(chat["id"], chat["name"]) if chat["type"] == "group" else go_to_private_chat(chat["name"]),
                ink=True,
                bgcolor=ft.colors.GREY_100,
                border_radius=15,
                margin=ft.margin.symmetric(horizontal=10)
            )
            chat_list_view.controls.append(chat_container)
        e.page.update()
        
    def go_to_private_chat(username):
        def navigate(e): 
            result = cc.proses(f"createchat {username}")
            data = json.loads(result)
            id = data["id"]
            e.page.go(f"/private_chat/{id}")
        return navigate
        
    def join_group(id, name):
        def navigate(e):
            e.page.go(f"/join_group/{id}/{name}")
        return navigate
        
    def create_group(e):
        e.page.go("/create_group")
        
    def get_new_chat():
        result = cc.proses(f"getnewchat")
        if result.startswith("Error"):
            return []
        else:
            return json.loads(result)
    
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
    
    chat_data = get_new_chat()
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
                            ft.Text(chat["name"], size=16),
                            ft.Text("Join this group", size=14, color=ft.colors.GREY) if chat["type"] == "group" else ft.Text("Start new chat", size=14, color=ft.colors.GREY)
                        ],
                        spacing=5,
                        alignment=ft.MainAxisAlignment.START
                    )
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(10),
            on_click=join_group(chat["id"], chat["name"]) if chat["type"] == "group" else go_to_private_chat(chat["name"]),
            ink=True,
            bgcolor=ft.colors.GREY_100,
            border_radius=15,
            margin=ft.margin.symmetric(horizontal=10)
        )
        chat_containers.append(chat_container)
    
    chat_list_view = ft.ListView(
        controls = [create_group_container] +  chat_containers,
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