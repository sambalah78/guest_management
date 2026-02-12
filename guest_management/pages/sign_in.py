import reflex as rx
from ..state import State
GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"
TEXT_WHITE = "#FFFFFF"
def login_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Empire Login", size="7", color=GOLD),
            rx.input(
                placeholder="Username", 
                on_change=State.set_username,
                width="100%",
                background=BLACK,
                border=f"1px solid {GOLD}",
                color=TEXT_WHITE,
            ),
            rx.input(
                placeholder="Password", 
                type="password", 
                on_change=State.set_password,
                width="100%",
                background=BLACK,
                border=f"1px solid {GOLD}",
                color=TEXT_WHITE,
            ),
            rx.cond(
                State.error_message != "",
                rx.text(State.error_message, color="red", size="2"),
            ),
            rx.button(
                "Sign In", 
                width="100%", 
                on_click=State.login,
                background=GOLD, 
                color=BLACK
            ),
            rx.link("Back to Home", href="/", size="2", color="gray"),
            spacing="4",
            padding="3em",
            background=DARK_GRAY,
            border=f"1px solid {GOLD}",
            border_radius="10px",
            box_shadow=f"0 0 20px {GOLD}33", # Subtle gold glow
            width="380px",
        ),
        height="100vh",
        background=BLACK,
    )