import reflex as rx
from ..state import State

def checkin_page():
    return rx.center(
        rx.vstack(
            rx.image(src="/empire.jpg", width="80px"),
            rx.heading("Guest Check-In", size="7", color="#D4AF37"),
            rx.text("Verify your attendance below", color="gray"),
            rx.input(
                placeholder="Name",
                value=State.search_name,
                on_change=State.set_search_name,
                width="100%",
                size="3",
                bg="#2A2A2A",
                color="white",
                border_color="#D4AF37"
            ),
            rx.text("— OR —", color="gray", size="1"),
            rx.input(
                placeholder="Guest ID / Code",
                value=State.search_id,
                on_change=State.set_search_id,
                width="100%",
                size="3",
                bg="#2A2A2A",
                color="white",
                border_color="#D4AF37"
            ),
            rx.vstack(
                rx.button(
                    "✅ Confirm Arrival",
                    on_click=State.check_in_guest,
                    bg="#D4AF37",
                    color="black",
                    width="100%",
                    size="3",
                    _hover={"bg": "#C4A030"}
                ),
                rx.button(
                    "↻ Reset",
                    on_click=State.clear_checkin_fields,
                    variant="outline",
                    border_color="#D4AF37",
                    color="#D4AF37",
                    size="3"
                ),
                width="100%",
                spacing="2"
            ),
            rx.divider(border_color="#D4AF37"),
            rx.text(
                "Scan the QR code at the entrance to check in",
                color="gray",
                size="1",
                text_align="center"
            ),
            spacing="4",
            padding="2.5em",
            bg="#1A1A1A",
            border_radius="20px",
            border="1px solid #D4AF37",
            width="90%",
            max_width="400px",
            align="center"
        ),
        height="100vh",
        bg="#111111"
    )