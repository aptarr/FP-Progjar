import flet as ft
import json
from cli import cc

def join_group(id, name):
    def handle_join_group(e):
        groupname = groupname_field.value
        password = password_field.value
        
        result = cc.proses(f"joingroup {id} {password}")
        if result.startswith("joined"):
            e.page.go(f"/group_chat/{id}")
        else:
            status.value = result
            e.page.update()
        
    def back(e):
        e.page.go("/new_chat")
    
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
                ft.Text("Join Group", size=18),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(10),
    )
    groupname_field = ft.TextField(
        label="Group Name",
        value=name, 
        width=300, 
        height=40, 
        bgcolor="#d84d4d, 0.2", 
        border_radius=15, 
        border_color=ft.colors.TRANSPARENT, 
        filled=True,
        read_only=True
    )
    password_field = ft.TextField(
        label="Password", 
        password=True, 
        width=300, 
        height=40, 
        bgcolor="#d84d4d, 0.2", 
        border_radius=15, 
        border_color=ft.colors.TRANSPARENT, 
        filled=True
    )
    create_button = ft.ElevatedButton(
        text="Join", 
        on_click=handle_join_group, 
        width=300, 
        height = 40,
        bgcolor="#d84d4d", 
        color=ft.colors.WHITE
    )
    status = ft.Text()
    
    return ft.Column(
        controls = [
            top_bar,
            ft.Container(height=160),
            groupname_field,
            password_field,
            ft.Container(height=30),
            create_button,
            status
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )