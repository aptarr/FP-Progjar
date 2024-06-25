import flet as ft
from cli import ChatClient

chat_client = ChatClient()

def login():
    def handle_login(e):
        username = username_field.value
        password = password_field.value
        result = chat_client.proses(f"auth {username} {password}")
        if chat_client.tokenid:
            e.page.go("/dashboard")
        else:
            login_status.value = result
            e.page.update()

    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    login_status = ft.Text()

    return ft.Column(
        controls=[
            ft.Text("Login Page"),
            username_field,
            password_field,
            ft.ElevatedButton(text="Login", on_click=handle_login),
            ft.TextButton(text="Register", on_click=lambda e: e.page.go("/register")),
            login_status
        ]
    )