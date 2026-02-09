import reflex as rx
from ..state import State

import reflex as rx
from ..state import State

def checkin_page():
    return rx.center(
        rx.vstack(
            rx.heading("Guest Check-In", color="#D4AF37"),
            rx.input(placeholder="Full Name", value=State.search_name, on_change=State.set_search_name, width="100%"),
            rx.text("— OR —", color="gray"),
            rx.input(placeholder="Guest ID", value=State.search_id, on_change=State.set_search_id, width="100%"),
            rx.button("Check In", on_click=State.check_in_guest, bg="#D4AF37", width="100%"),
            spacing="4", padding="2em", bg="#1A1A1A", border_radius="15px", border="1px solid #D4AF37"
        ),
        height="100vh", bg="#111111"
    )