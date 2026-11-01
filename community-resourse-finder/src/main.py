import flet as ft

from pages.home import home_screen
from pages.login import login_screen
from pages.signin import signin_screen

def main(page: ft.Page):
    page.title = "Community Resource Finder"
    page.padding = 20

    state = {"user": None}

    def navigate(e=None):
        route = page.route
        page.views.clear()

        if route == "/register":
            page.views.append(signin_screen(page, state))
        elif route == "/home" and state["user"]:
            page.views.append(home_screen(page, state))
        else: 
            page.views.append(login_screen(page, state))

        page.update()

    page.on_route_change = navigate  
    navigate()


if __name__ == "__main__":
    ft.run(main)