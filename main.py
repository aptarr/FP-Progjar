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
    }

    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        route = e.route
        if route.startswith("/private_chat/"):
            id = route.split("/private_chat/")[1]
            page.views.append(
                ft.View(route, [private_chat(id)])
            )
        elif route.startswith("/group_chat/"):
            id = route.split("/group_chat/")[1]
            page.views.append(
                ft.View(route, [group_chat(id)])
            )
        elif route.startswith("/join_group/"):
            _, _, id, name = route.split("/")
            page.views.append(
                ft.View(route, [join_group(id, name)])
            )
        else:
            if route in routes:
                page.views.append(
                    ft.View(route, [routes[route]()])
                )
        
        page.update()
    
    page.on_route_change = route_change
    page.go("/login")

ft.app(main)