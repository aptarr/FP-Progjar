import flet as ft
from cli import cc

def login():
    def handle_login(e):
        username = username_field.value
        password = password_field.value
        result = cc.proses(f"login {username} {password}")
        if cc.tokenid:
            e.page.go("/dashboard")
        else:
            status.value = result
            e.page.update()

    logo = ft.Container(
        content = ft.Image(src="img/logo.png", width=100, height=100),
        alignment = ft.alignment.center,
        margin = ft.margin.only(bottom=30, top=0)
    )
    username_field = ft.TextField(
        label="Username", 
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
    login_button = ft.ElevatedButton(
        text="Login", 
        on_click=handle_login, 
        width=300, 
        height = 40,
        bgcolor="#d84d4d", 
        color=ft.colors.WHITE
    )
    register_row = ft.Row(
        controls=[
            ft.Text("New around here?", size=12),
            ft.TextButton(text="Register", on_click=lambda e: e.page.go("/register"))
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    status = ft.Text()

    return ft.Column(
        controls = [
            ft.Container(height=140),
            logo,
            username_field,
            password_field,
            ft.Container(height=30),
            login_button,
            register_row,
            status
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )