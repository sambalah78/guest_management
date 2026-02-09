import reflex as rx
from ..state import State


def checkin() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Empire Check-In", size="7", color="#D4AF37"),
            rx.text("Enter your Name or Guest ID to verify arrival", color="gray", text_align="center"),

            # Input for Name
            rx.input(
                placeholder="Full Name",
                value=State.search_name,
                on_change=State.set_search_name,
                width="100%", size="3"
            ),

            # OR Divider
            rx.hstack(rx.divider(), rx.text("OR", color="gray", size="1"), rx.divider(), width="100%", align="center"),

            # Input for ID
            rx.input(
                placeholder="Guest ID / Code",
                value=State.search_id,
                on_change=State.set_search_id,
                width="100%", size="3"
            ),

            rx.button(
                "Verify & Check-In",
                on_click=State.check_in_guest,
                background="#D4AF37",
                color="black",
                width="100%",
                size="3",
                margin_top="1em"
            ),

            spacing="4",
            padding="2.5em",
            background="#1A1A1A",
            border_radius="20px",
            border="1px solid #D4AF37",
            width="90%",
            max_width="400px",
            align="center",
        ),
        width="100%", height="100vh", background="#111111",
    )