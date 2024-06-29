import flet as ft
from pages.login import login
from pages.register import register
from pages.dashboard import dashboard
from pages.new_chat import new_chat
from pages.create_group import create_group
from pages.join_group import join_group
from pages.private_chat import private_chat
from pages.group_chat import group_chat

def main(page: ft.Page):
    page.title = "Chat Application"
    page.window.width = 360
    page.window.height = 640
    page.window.title_bar_hidden = False
    
    routes = {
        "/login": login,
        "/register": register,
        "/dashboard": dashboard,
        "/new_chat": new_chat,
        "/create_group": create_group,
        "/join_group": join_group,
        "/private_chat": private_chat,
        "/group_chat": group_chat,
    }
    
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        page.views.append(
            ft.View(
                e.route,
                [routes[e.route]()]
            )
        )
        page.update()
    
    page.on_route_change = route_change
    page.go("/login")

ft.app(main)