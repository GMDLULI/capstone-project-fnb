import flet as ft

import api

GREEN = "#728E6D"
CREAM = "#EBE2CC"


def _field(label: str, **kwargs) -> ft.TextField:
    return ft.TextField(
        label=label,
        label_style=ft.TextStyle(color=GREEN),
        color=GREEN,
        border_color=GREEN,
        border_radius=ft.BorderRadius.all(20),
        **kwargs,
    )


def reset_password_dialog(page: ft.Page, email_prefill: str = ""):
    email = _field("Email", autofocus=True, value=email_prefill)
    password = _field("New password (min 6 characters)", password=True, can_reveal_password=True)
    confirm = _field("Confirm new password", password=True, can_reveal_password=True)
    message = ft.Text(visible=False, weight=ft.FontWeight.BOLD)

    def show_message(text: str, color: str = ft.Colors.RED):
        message.value = text
        message.color = color
        message.visible = True
        page.update()

    def close(e):
        page.pop_dialog()

    def save(e):
        # Client-side checks first, so we don't call the API for obvious mistakes
        if not email.value:
            show_message("Email cannot be empty.")
            return
        if not password.value:
            show_message("Password cannot be empty.")
            return
        if password.value != confirm.value:  # compare .value, not the controls
            show_message("Passwords do not match.")
            return

        try:
            api.reset_password(email.value, password.value)
        except api.ApiError as exc:
            show_message(str(exc))
            return

        # Success: swap the form for a confirmation message
        dialog.title = ft.Text("Password updated", color=GREEN, weight=ft.FontWeight.BOLD)
        dialog.content = ft.Text("You can now log in with your new password.", color=GREEN)
        dialog.actions = [ft.Button(content="Back to login", bgcolor=GREEN, color=CREAM, on_click=close)]
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        bgcolor=CREAM,
        title=ft.Text("Reset password", color=GREEN, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            tight=True,
            width=360,
            controls=[email, password, confirm, message],
        ),
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=close,
                style=ft.ButtonStyle(text_style=ft.TextStyle(color=GREEN, weight=ft.FontWeight.BOLD)),
            ),
            ft.Button(content="Save", bgcolor=GREEN, color=CREAM, on_click=save),
        ],
    )
    return dialog