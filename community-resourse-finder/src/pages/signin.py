import flet as ft

import api


def signin_screen(page: ft.Page, state: dict) -> ft.View:
    email = ft.TextField(label="Email", autofocus=True)
    password = ft.TextField(label="Password (min 6 characters)", password=True, can_reveal_password=True)
    confirm = ft.TextField(label="Confirm password", password=True, can_reveal_password=True)
    error = ft.Text(color=ft.Colors.RED)

    async def handle_register(e):
        error.value = ""
        if password.value != confirm.value:
            error.value = "Passwords do not match."
            page.update()
            return
        try:
            user = api.register(email.value or "", password.value or "")
        except api.ApiError as exc:
            error.value = str(exc)
            page.update()
            return
        state["user"] = user["email"]
        await page.push_route("/home")


    confirm.on_submit = handle_register

    async def handle_text(e):
        await page.push_route("/login")

    body = ft.Column(
        width=360,
        controls=[
            ft.Text("Create your account", size=28, weight=ft.FontWeight.BOLD),
            email,
            password,
            confirm,
            error,
            ft.Button("Sign up", on_click=handle_register),
            ft.TextButton("I already have an account", on_click=handle_text),
        ],
    )

    return ft.View(
        route="/register",
        controls=[body])