import flet as ft

import api


def login_screen(page: ft.Page, state: dict) -> ft.View:
    email = ft.TextField(label="Email", autofocus=True)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    error = ft.Text(color=ft.Colors.RED)

    async def handle_login(e):
        error.value = ""
        try:
            user = api.login(email.value or "", password.value or "")
        except api.ApiError as exc:
            error.value = str(exc)
            page.update()
            return
        state["user"] = user["email"]
        await page.push_route("/home")

    password.on_submit = handle_login

    async def handle_text(e):
        await page.push_route("/register")


    body = ft.Column(
        width=360,
        controls=[
            ft.Text("Welcome back", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Log in to find resources near you"),
            email,
            password,
            error,
            ft.Button("Log in", on_click=handle_login),
            ft.TextButton("Create an account", on_click= handle_text),
        ],
    )

    return ft.View(
        route="/login",
        controls=[body]
    )