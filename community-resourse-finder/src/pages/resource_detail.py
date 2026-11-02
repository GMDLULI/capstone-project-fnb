import flet as ft

import api

from pages.home import category_pill, info_row, normalize_url


def resource_detail_screen(page: ft.Page, state: dict, resource_id: int) -> ft.View:
    async def go_back(e):
        await page.push_route("/home")

    back_button = ft.TextButton(
        "Back to resources",
        icon=ft.Icons.ARROW_BACK_ROUNDED,
        on_click=go_back,
        style=ft.ButtonStyle(text_style=ft.TextStyle(color="#EBE2CC", weight=ft.FontWeight.BOLD)),
    )

    content = ft.Column(spacing=20)
    content.controls.append(back_button)

    try:
        r = api.get_resource(resource_id)
    except api.ApiError as exc:
        content.controls.append(ft.Text(str(exc), color="#EBE2CC", size=18))
    else:
        details: list[ft.Control] = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(r["name"], size=32, weight=ft.FontWeight.BOLD, color="#728E6D", expand=True),
                    category_pill(r["category"]),
                ],
            ),
            info_row(ft.Icons.LOCATION_ON_ROUNDED, r["area"]),
            ft.Divider(color="#728E6D"),
            ft.Text("About", size=18, weight=ft.FontWeight.BOLD, color="#728E6D"),
            ft.Text(r["description"], color="#728E6D", size=16, selectable=True),
        ]
        if r.get("phone"):
            details.append(info_row(ft.Icons.PHONE_ROUNDED, r["phone"])) # pyright: ignore[reportArgumentType]
        website = normalize_url(r.get("website"))
        if website:
            details.append(info_row(ft.Icons.LANGUAGE_ROUNDED, website)) # pyright: ignore[reportArgumentType]

        content.controls.append(
            ft.Card(
                bgcolor="#EBE2CC",
                elevation=4,
                content=ft.Container(
                    padding=ft.Padding.all(30),
                    border_radius=ft.BorderRadius.all(20),
                    content=ft.Column(details, spacing=12),
                ),
            )
        )

    content.width = min(800, (page.width or 800) * 0.9)

    return ft.View(
        route=f"/resource/{resource_id}",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#728E6D",
                alignment=ft.Alignment.TOP_CENTER,
                padding=ft.Padding.all(30),
                content=content,
            )
        ],
    )