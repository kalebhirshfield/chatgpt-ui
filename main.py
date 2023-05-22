import flet as ft
from flet import RoundedRectangleBorder
import openai as ai
from os import getenv
from dotenv import load_dotenv

load_dotenv()
ai.api_key = getenv("OPENAI_API_KEY")


def main(page: ft.Page):
    def closeBanner(_):
        page.banner.open = False
        page.update()

    def btnClick(_):
        try:
            question = tbQuestion.value
            tbQuestion.value = ""
            lvAnswer.controls.append(ft.Text(f"You: {question}"))
            page.update()
            completion = ai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}],
            )
            lvAnswer.controls.append(
                ft.Text(
                    f"ChatGPT: {completion.choices[0].message.content}",
                    color=ft.colors.BLUE_ACCENT,
                )
            )

            page.update()
        except:
            page.banner.open = True
            page.update()

    page.title = "ChatGPT"
    page.window_width = 645
    page.window_height = 455
    page.window_resizable = False
    page.window_full_screen = False
    page.scroll = ft.ScrollMode(value="auto")
    page.theme_mode = "dark"
    page.window_maximizable = False
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    windowDragArea = ft.WindowDragArea(
        ft.Container(
            ft.Text("ChatGPT", size=20), bgcolor=ft.colors.BACKGROUND, padding=10
        ),
        expand=True,
        maximizable=False,
    )

    btnClose = ft.IconButton(
        ft.icons.CLOSE,
        style=ft.ButtonStyle(
            color={
                ft.MaterialState.DEFAULT: ft.colors.WHITE60,
                ft.MaterialState.HOVERED: ft.colors.RED_ACCENT_200,
            },
            shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
        ),
        on_click=lambda e: page.window_close(),
    )

    page.banner = ft.Banner(
        bgcolor=ft.colors.AMBER_ACCENT_700,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.BLACK, size=40),
        content=ft.Text(
            color=ft.colors.BLACK,
            value="ChatGPT was unable to respond to that message. Please try again.",
        ),
        actions=[
            ft.TextButton(
                "Retry",
                on_click=btnClick,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: ft.colors.BLACK,
                    },
                    bgcolor={
                        ft.MaterialState.HOVERED: ft.colors.AMBER_ACCENT_400,
                    },
                    shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
                ),
            ),
            ft.TextButton(
                "Cancel",
                on_click=closeBanner,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: ft.colors.BLACK,
                    },
                    bgcolor={
                        ft.MaterialState.HOVERED: ft.colors.AMBER_ACCENT_400,
                    },
                    shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
                ),
            ),
        ],
    )

    lvAnswer = ft.ListView(
        expand=1,
        spacing=10,
        padding=20,
        auto_scroll=True,
        height=290,
    )

    tbQuestion = ft.TextField(
        label="Talk to ChatGPT",
        suffix_icon="send",
        multiline=True,
        shift_enter=True,
        border_radius=10,
        border_color=ft.colors.BACKGROUND,
        text_style=ft.TextStyle(color=ft.colors.WHITE70),
        label_style=ft.TextStyle(color=ft.colors.WHITE70),
        border_width=2,
        focused_border_width=4,
        expand=True,
        on_submit=btnClick,
        autofocus=True,
        focused_border_color=ft.colors.BLUE_ACCENT,
        capitalization=ft.TextCapitalization.SENTENCES,
        focused_bgcolor=ft.colors.BACKGROUND,
        bgcolor=ft.colors.BLACK26,
        cursor_color=ft.colors.BLUE_ACCENT,
        cursor_width=3,
    )

    page.add(
        ft.Row(controls=[windowDragArea, btnClose]),
        ft.Row(controls=[lvAnswer]),
        ft.Row(controls=[tbQuestion], alignment="bottom"),
    ),

    pass


ft.app(target=main)
