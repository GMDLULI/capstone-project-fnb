import flet as ft

import api


def signin_screen(page: ft.Page, state: dict) -> ft.View:
    email = ft.TextField(
        label="Email",
        autofocus=True,
        bgcolor="#EBE2CC",
        color="#728E6D",
        border_color="#EBE2CC",
        text_style=ft.TextStyle(color="#EBE2CC"),
        width=page.width * 0.5,
        helper_style=ft.TextStyle(color=ft.Colors.RED),
        border_radius=ft.BorderRadius.all(20)
        ,)
    password = ft.TextField(
        label="Password",
        password=True, 
        bgcolor="#EBE2CC",
        color="#728E6D",
        border_color="#EBE2CC",
        can_reveal_password=True,
        text_style=ft.TextStyle(color="#EBE2CC"),
        width=page.width * 0.5,
        helper_style=ft.TextStyle(color=ft.Colors.RED),
        border_radius=ft.BorderRadius.all(20),
        )
    confirm = ft.TextField(
        label="Confirm Password",
        password=True, 
        bgcolor="#EBE2CC",
        color="#728E6D",
        border_color="#EBE2CC",
        can_reveal_password=True,
        text_style=ft.TextStyle(color="#EBE2CC"),
        width=page.width * 0.5,
        helper_style=ft.TextStyle(color=ft.Colors.RED),
        border_radius=ft.BorderRadius.all(20),)
        
    error = ft.Text(
        size=25,
        visible=False,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED
        )

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

    body = ft.Container(
        expand=True,
        bgcolor="#728E6D",
        alignment=ft.Alignment.CENTER,
        height=page.height,
        width=page.width,

         content=ft.Container(
            height=page.height * 0.85,
            width=page.width * 0.5,
            bgcolor="#728E6D",
            border_radius=ft.BorderRadius.all(20),
            padding=ft.Padding.all(40),

            content= ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                     ft.Container(
                        padding = ft.Padding(0,20,0,40),
                        content=ft.Text(
                            "Create your account",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color="#EBE2CC"
                        )
                    ),

                    ft.Row(
                        controls=[
                            ft.Icon(
                            icon=ft.Icons.MAIL_ROUNDED,
                                size=25,
                                color="#EBE2CC"
                            ),
                            ft.Text(
                                "Email:",
                                size=20,
                                color="#EBE2CC"
                            )
                        ]
                    ),
                    email,
                    ft.Row(
                        controls=[
                            ft.Icon(
                            icon=ft.Icons.LOCK_ROUNDED,
                                size=25,
                                color="#EBE2CC"
                            ),
                            ft.Text(
                                "Password:",
                                size=20,
                                color="#EBE2CC"
                            )
                        ]
                    ),
                    password,
                    ft.Row(
                        controls=[
                            ft.Icon(
                            icon=ft.Icons.LOCK_ROUNDED,
                                size=25,
                                color="#EBE2CC"
                            ),
                            ft.Text(
                                "Password:",
                                size=20,
                                color="#EBE2CC"
                            )
                        ]
                    ),
                    confirm,
                    error,
                     ft.Container(
                        padding=ft.Padding(0,20,0,0),
                        content = ft.Button(
                                content='sign up',
                                bgcolor="#EBE2CC",
                                color="#728E6D",
                                width = page.width * 0.3,
                                height = 50,
                                on_click = handle_register
                            )
                    ),
                    ft.TextButton(
                        "I already have an account",
                        on_click=handle_text,
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(
                                color="#EBE2CC",
                                weight=ft.FontWeight.BOLD
                            )
                        )
                    ),
                ],
            )
                    
        )

    )

    # body = ft.Column(
    #     width=360,
    #     controls=[
    #         ft.Text("Create your account", size=28, weight=ft.FontWeight.BOLD),
    #         email,
    #         password,
    #         confirm,
    #         error,
    #         ft.Button("Sign up", on_click=handle_register),
    #         ft.TextButton("I already have an account", on_click=handle_text),
    #     ],
    # )

    return ft.View(
        route="/register",
        controls=[body])