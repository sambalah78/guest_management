import reflex as rx
from ..state import State

def checkin_page():
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading("Guest Check-In", size="6", color="#D4AF37"),

                rx.input(
                    placeholder="Enter Name",
                    value=State.search_name,
                    on_change=State.set_search_name,
                    width="100%",
                    size="3",
                ),

                rx.text("— OR —", size="1", color="gray"),

                rx.input(
                    placeholder="Enter Guest ID",
                    value=State.search_id,
                    on_change=State.set_search_id,
                    width="100%",
                    size="3",
                ),

                rx.button(
                    "Confirm Arrival",
                    on_click=State.check_in_guest,
                    width="100%",
                    size="3",
                    bg="#D4AF37",
                    color="black",
                ),

                spacing="4",
                width="100%",
                max_width="400px",
                padding="2em",
                border_radius="20px",
                bg="#1A1A1A",
                border="1px solid #D4AF37",
            ),
            height="100vh",
        ),
        bg="#111111",
        width="100%",
    )
