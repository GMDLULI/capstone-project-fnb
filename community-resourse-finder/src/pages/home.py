import asyncio

import flet as ft

import api


GREEN = "#728E6D",
CREAM = "#EBE2CC",
DARK_GREEN = "#4F6B4A"

def info_row(icon:str, text:str) -> ft.Row:
    return ft.Row(
        controls=[
            ft.Icon(icon=icon, size=20, color="#4F6B4A"), # pyright: ignore[reportArgumentType]
            ft.Text(text, size=16, color="#4F6B4A", selectable=True, expand=True),
        ],
        spacing=8,
    )


def resource_card(r: dict) -> ft.Card:

    category_pill = ft.Container(
        bgcolor="#728E6D",
        border_radius=ft.BorderRadius.all(12),
        padding=ft.Padding(10, 4, 10, 4),
        content=ft.Text(r["category"].title(), size=12, color="#EBE2CC", weight=ft.FontWeight.BOLD),
    )
     
    lines: list[ft.Control] = [

        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(r["name"], size=18, weight=ft.FontWeight.BOLD, color="#4F6B4A"),
                category_pill,

            ]
        ),
        ft.Row(
        controls=[
            ft.Icon(icon=ft.Icons.LOCATION_ON_ROUNDED, size=20, color="#4F6B4A"),
            ft.Text(r["area"], size=16, color="#4F6B4A", selectable=True, expand=True),
            ],
            spacing=8,
        ),
        ft.Text(r["description"], size=16, color="#4F6B4A", selectable=True, expand=True),
    ]
    if r.get("phone"):
        lines.append(info_row(ft.Icons.PHONE_ROUNDED, r["phone"])) # pyright: ignore[reportArgumentType]
    if r.get("website"):
        lines.append(info_row(ft.Icons.WEB, r["website"])) # pyright: ignore[reportArgumentType]

    return ft.Card(
        bgcolor="#EBE2CC",
        elevation=4,
        content=ft.Container(
            padding=ft.Padding.all(20), 
            border_radius=ft.BorderRadius.all(20),
            content=ft.Column(lines, spacing=8)))


def home_screen(page: ft.Page, state: dict) -> ft.View:
    results = ft.ListView(expand=True, spacing=8)
    message = ft.Text(color="#EBE2CC", size=16)
    search = ft.TextField(
        label="Search by name, area or description", 
        label_style=ft.TextStyle(color="#728E6D"),
        bgcolor="#EBE2CC",
        color="#728E6D",
        border_color="#EBE2CC",
        border_radius=ft.BorderRadius.all(20),
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        expand=True,
        )


    def fetch():
        """Fill the list. No page.update() here: the view isn't on the page yet on first build."""
        message.value = ""
        try:
            data = api.get_resources(q=search.value or "")
        except api.ApiError as exc:
            results.controls = []
            message.value = str(exc)
            return
        results.controls = [resource_card(r) for r in data]
        if not data:
            message.value = "No resources found."

    def load(e=None):
        fetch()
        page.update()

    async def logout(e):
        state["user"] = None
        await page.push_route("/login")

    search.on_submit = load

    content_width = min(800, (page.width or 800) * 0.9)

    # Build the screen first, then fetch the data once it's on the page.
    column = ft.Column(
        width=content_width,
        expand=True,
        spacing=20,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Resources", size=28, weight=ft.FontWeight.BOLD, color="#EBE2CC"),
                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.Icon(icon=ft.Icons.PERSON_ROUNDED, size=22, color='#EBE2CC'),
                            ft.Text(state["user"], size=16, color="#EBE2CC"),
                            ft.TextButton(
                                "Logout",
                                on_click=logout,
                                style=ft.ButtonStyle(
                                    color= "#EBE2CC",
                                    bgcolor= "#728E6D",
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.Padding(10, 5, 10, 5),
                                    text_style=ft.TextStyle(color="#EBE2CC", weight=ft.FontWeight.BOLD)
                                
                                 
                                ),
                            )
                           
                        ],
                        
                    )
                ],
            ),
            ft.Row(
                controls=[
                    search, 
                    ft.Button(
                        "Search", 
                        on_click=load,
                        color="#728E6D",
                        bgcolor="#EBE2CC",
                        height=40,
                        )
                    ],
                ),
            message,
            results,
        ],
    )

    fetch()  # initial fetch, before the view is on the page
    return ft.View(
        route="/home",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#728E6D",
                alignment=ft.Alignment.TOP_CENTER,
                padding=ft.Padding.all(30),
                content=column
            )
        ]
    )