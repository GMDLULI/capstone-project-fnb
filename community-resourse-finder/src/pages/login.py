import flet as ft

import api
import components.reset_password as reset_password_dialog


def login_screen(page: ft.Page, state: dict) -> ft.View:
    email = ft.TextField(
        label="Email",  
        autofocus=True,
        bgcolor="#EBE2CC",
        color="#728E6D",
        border_color="#EBE2CC",
        text_style=ft.TextStyle(color="#EBE2CC"),
        width=page.width * 0.5, # pyright: ignore[reportOptionalOperand]
        helper_style=ft.TextStyle(color=ft.Colors.RED),
        border_radius=ft.BorderRadius.all(20),

        )
    password = ft.TextField(
        label="Password",
        password=True, 
        bgcolor="#EBE2CC",
        color="#728E6D",
        border_color="#EBE2CC",
        can_reveal_password=True,
        text_style=ft.TextStyle(color="#EBE2CC"),
        width=page.width * 0.5, # pyright: ignore[reportOptionalOperand]
        helper_style=ft.TextStyle(color=ft.Colors.RED),
        border_radius=ft.BorderRadius.all(20),
        )
    
    error = ft.Text(size=25,
                    visible=False,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED)

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

    def on_forgot_password(e):
        page.show_dialog(reset_password_dialog.reset_password_dialog(page, email_prefill=email.value or ""))


    body = ft.Container(
        expand=True,
        bgcolor="#728E6D",
        alignment=ft.Alignment.CENTER,
        height=page.height,
        width=page.width,
        content=ft.Container(
            height=page.height * 0.85, # pyright: ignore[reportOptionalOperand]
            width=page.width * 0.5,  # pyright: ignore[reportOptionalOperand]
            bgcolor="#728E6D",
            border_radius=ft.BorderRadius.all(20),
            padding=ft.Padding.all(40),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                
                controls= [
                    #login text
                   ft.Container(
                        padding = ft.Padding(0,20,0,40),
                        content=ft.Text(
                            "Welcome Back",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color="#EBE2CC"
                        )
                   ),
                   # User Icon and text field
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
                    # Error Message
                    error,

                    #login Button
                    ft.Container(
                        padding=ft.Padding(0,20,0,0),
                        content = ft.Button(
                                content='Login',
                                bgcolor="#EBE2CC",
                                color="#728E6D",
                                width = page.width * 0.3, # type: ignore
                                height = 50,
                                on_click = handle_login
                            )
                    ),

                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.TextButton(
                                "Create an account",
                                on_click=handle_text,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        color="#EBE2CC",
                                        weight=ft.FontWeight.BOLD
                                    )
                                )
                            ),
                            ft.TextButton(
                                "Forgot Password?",
                                on_click=on_forgot_password,
                                style=ft.ButtonStyle(
                                    text_style=ft.TextStyle(
                                        color="#EBE2CC",
                                        weight=ft.FontWeight.BOLD
                                    )
                                )
                            ),
                        ]
                    )
                      
                ]
               
            )
        )
    )

    return ft.View(
        route="/login",
        controls=[body]
    )