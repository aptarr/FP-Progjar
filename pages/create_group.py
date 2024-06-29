import flet as ft
from cli import cc

def create_group():
    def handle_create_group(e):
        groupname = groupname_field.value
        password = password_field.value
        confirm = confirm_field.value
        
        if password == confirm:
            e.page.go("/group_chat")
        else:
            status.value = 'Confirm password salah'
            e.page.upate()
            
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
                ft.Text("Create New Group", size=18),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.all(10),
    )
    groupname_field = ft.TextField(
        label="Group Name", 
        width=300, 
        height=40, 
        bgcolor="#d84d4d, 0.2", 
        border_radius=15, 
        border_color=ft.colors.TRANSPARENT, 
        filled=True
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
    confirm_field = ft.TextField(
        label="Confirm Password", 
        password=True, 
        width=300, 
        height=40, 
        bgcolor="#d84d4d, 0.2", 
        border_radius=15, 
        border_color=ft.colors.TRANSPARENT, 
        filled=True
    )
    create_button = ft.ElevatedButton(
        text="Create", 
        on_click=handle_create_group, 
        width=300, 
        height = 40,
        bgcolor="#d84d4d", 
        color=ft.colors.WHITE
    )
    status = ft.Text()
    
    return ft.Column(
        controls = [
            top_bar,
            ft.Container(height=110),
            groupname_field,
            password_field,
            confirm_field,
            ft.Container(height=30),
            create_button,
            status
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )