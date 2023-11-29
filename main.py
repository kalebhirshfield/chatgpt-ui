import flet as ft
from flet import RoundedRectangleBorder
from openai import OpenAI
from os import getenv
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=getenv("OPENAI_API_KEY"))


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
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": question}],
                model="gpt-3.5-turbo",
            )
            lvAnswer.controls.append(
                ft.Text(
                    f"ChatGPT: {completion.choices[0].message.content}",
                    color=ft.colors.TERTIARY,
                )
            )

            page.update()
        except:
            page.banner.open = True
            page.update()

    page.window_width = 600
    page.window_height = 400
    page.window_resizable = False
    page.window_full_screen = False
    page.scroll = ft.ScrollMode(value="auto")
    page.window_maximizable = False
    page.theme = ft.Theme(use_material3=True, color_scheme_seed="cyan")

    page.banner = ft.Banner(
        bgcolor=ft.colors.ERROR_CONTAINER,
        leading=ft.Icon(
            ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.ON_ERROR_CONTAINER, size=40
        ),
        content=ft.Text(
            color=ft.colors.ON_ERROR_CONTAINER,
            value="ChatGPT was unable to respond to that message. Please try again.",
        ),
        actions=[
            ft.TextButton(
                "Retry",
                on_click=btnClick,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: ft.colors.ON_ERROR_CONTAINER,
                    },
                    shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
                ),
            ),
            ft.TextButton(
                "Cancel",
                on_click=closeBanner,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: ft.colors.ON_ERROR_CONTAINER,
                    },
                    bgcolor={
                        ft.MaterialState.HOVERED: ft.colors.ERROR_CONTAINER,
                    },
                    shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
                ),
            ),
        ],
    )

    lvAnswer = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True,
        height=page.window_height - 150,
    )

    tbQuestion = ft.TextField(
        label="Talk to ChatGPT",
        suffix_icon="send",
        multiline=True,
        shift_enter=True,
        border_radius=10,
        border_color=ft.colors.BACKGROUND,
        text_style=ft.TextStyle(color=ft.colors.ON_SURFACE_VARIANT),
        label_style=ft.TextStyle(color=ft.colors.ON_SURFACE_VARIANT),
        border_width=2,
        focused_border_width=4,
        expand=True,
        on_submit=btnClick,
        autofocus=True,
        focused_border_color=ft.colors.ON_SURFACE_VARIANT,
        capitalization=ft.TextCapitalization.SENTENCES,
        focused_bgcolor=ft.colors.BACKGROUND,
        bgcolor=ft.colors.SURFACE_VARIANT,
        cursor_color=ft.colors.ON_SURFACE_VARIANT,
        cursor_width=2,
    )

    page.add(
        ft.Row(controls=[lvAnswer]),
        ft.Row(controls=[tbQuestion], alignment="bottom"),
    )


if __name__ == "__main__":
    ft.app(target=main)
