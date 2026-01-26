import reflex as rx
from guest_management.guest_management.pages.home import home


def index() -> rx.Component:
    return home()


app = rx.App()
app.add_page(index)
