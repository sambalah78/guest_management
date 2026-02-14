import reflex as rx

from .pages import home_page,dashboard,sign_in,success,check_in
from .state import State
# --- STATE LOGIC ---

# --- PAGE: SPLASH SCREEN ---
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.image(src="empire.jpg", width="100px", height="auto"),
            rx.heading("Empire Signature", size="8", weight="bold"),

            rx.spinner(size="3"),
            spacing="4",
            align="center",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle, #ffffff 0%, #f0f0f0 100%)", on_mount=rx.redirect("/home"),
    )

app = rx.App()
# Add pages and link the splash logic to the index 'on_load'
app.add_page(index, route="/",)
app.add_page(home_page.home, route="/home",on_load=State.splash_logic)
app.add_page(sign_in.login_page, route="/login")
app.add_page(dashboard.dashboard, route="/dashboard", on_load=State.refresh_dashboard )
app.add_page(check_in.checkin_page, route="/checkin")
app.add_page(success.success_page, route="/success",on_load=State.success_redirect)

