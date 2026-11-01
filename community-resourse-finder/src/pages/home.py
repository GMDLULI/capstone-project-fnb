import asyncio

import flet as ft

import api

def resource_card(r: dict) -> ft.Card:
    lines: list[ft.Control] = [
        ft.Text(r["name"], size=18, weight=ft.FontWeight.BOLD),
        ft.Text(f"{r['category'].title()} · {r['area']}", color=ft.Colors.BLUE),
        ft.Text(r["description"]),
    ]
    if r.get("phone"):
        lines.append(ft.Text(f"Phone: {r['phone']}", selectable=True))
    if r.get("website"):
        lines.append(ft.Text(f"Website: {r['website']}", selectable=True))

    return ft.Card(content=ft.Container(padding=15, content=ft.Column(lines, spacing=4)))


def home_screen(page: ft.Page, state: dict) -> ft.View:
    results = ft.ListView(expand=True, spacing=8)
    message = ft.Text()
    search = ft.TextField(label="Search by name, area or description", expand=True)

    def load(e=None):
        message.value = ""
        try:
            data = api.get_resources(q=search.value or "")
        except api.ApiError as exc:
            results.controls = []
            message.value = str(exc)
            page.update()
            return
        results.controls = [resource_card(r) for r in data]
        if not data:
            message.value = "No resources found."
        page.update()

    async def logout(e):
        state["user"] = None
        await page.push_route("/login")

    search.on_submit = load

    # Build the screen first, then fetch the data once it's on the page.
    column = ft.Column(
        width=700,
        expand=True,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Resources", size=28, weight=ft.FontWeight.BOLD),
                    ft.Row([ft.Text(state["user"] or ""), ft.TextButton("Log out", on_click=logout)]),
                ],
            ),
            ft.Row([search, ft.Button("Search", on_click=load)]),
            message,
            results,
        ],
    )
    return ft.View(route="/home", controls=[column])