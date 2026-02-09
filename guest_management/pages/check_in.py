import reflex as rx
from ..state import State

import reflex as rx
from ..state import State


def checkin_page():
    return rx.center(
        rx.vstack(
            rx.image(src="/empire.jpg", width="80px"),
            rx.heading("Guest Check-In", size="7", color="#D4AF37"),
            rx.text("Verify your attendance below", color="gray"),
            rx.input(placeholder="Full Name", value=State.search_name, on_change=State.set_search_name, width="100%", size="3"),
            rx.text("— OR —", color="gray", size="1"),
            rx.input(placeholder="Guest ID / Code", value=State.search_id, on_change=State.set_search_id, width="100%", size="3"),
            rx.button("Confirm Arrival", on_click=State.check_in_guest, bg="#D4AF37", color="black", width="100%", size="3"),
            spacing="4", padding="2.5em", bg="#1A1A1A", border_radius="20px", border="1px solid #D4AF37", width="90%", max_width="400px", align="center"
        ),
        height="100vh", bg="#111111"
    )