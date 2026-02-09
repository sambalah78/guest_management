import reflex as rx
import asyncio
import pandas as pd
import io
from guest_management.pages.home_page import home as home_page
from guest_management.pages.sign_in import login_page
from guest_management.pages.dashboard import dashboard
from guest_management.state import State
from guest_management.pages import check_in
# --- STATE LOGIC ---




# --- PAGE: SPLASH SCREEN ---
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.image(src="empire.jpg", width="100px", height="auto"),
            rx.heading("Empire Signature", size="8", weight="bold"),
            rx.text("Loading Guest Manager...", color_scheme="gray"),
            rx.spinner(size="3"),
            spacing="4",
            align="center",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle, #ffffff 0%, #f0f0f0 100%)",
    )

app = rx.App()
# Add pages and link the splash logic to the index 'on_load'
app.add_page(index, route="/", on_load=State.splash_logic)
app.add_page(home_page, route="/home")
app.add_page(login_page, route="/login")
app.add_page(dashboard, route="/dashboard")
app.add_page(check_in.checkin, route="/check-in")
