import reflex as rx

from guest_management.pages.home_page import home


def index() -> rx.Component:
    return rx.box(rx.redirect("/home"))


app = rx.App()
app.add_page(index)
app.add_page(home, route="/home")
