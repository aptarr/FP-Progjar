import flet as ft

def dashboard():
    def handle_logout(e):
        e.page.go("/login")
    
    def handle_search(e):
        e.page.update()
    
    def go_to_chat(e):
        e.page.go("/chat")
    
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
    profile_icon = ft.Icon(
        name=ft.icons.ACCOUNT_CIRCLE,
        size=50,
        color=ft.colors.GREY
    )
    username_text = ft.Text("Username", size=16)
    last_message_text = ft.Text("Last message", size=14, color=ft.colors.GREY)
    chat_container = ft.Container(
        content=ft.Row(
            controls=[
                profile_icon,
                ft.Column(
                    controls=[
                        username_text,
                        last_message_text
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.START
                )
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.all(10),
        on_click=go_to_chat,
        ink=True,
        bgcolor=ft.colors.GREY_100,
        border_radius=15,
        margin=ft.margin.symmetric(horizontal=10)
    )
    chat_list_view = ft.ListView(
        controls = [
            chat_container,
            chat_container,
            chat_container,
            chat_container,
            chat_container,
            chat_container,
            chat_container,
            chat_container,
            chat_container,
            chat_container,
            chat_container,
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