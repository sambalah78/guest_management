import reflex as rx
from ..state import State


def checkin_page():
    return rx.center(
        rx.cond(
            State.checkin_success,

            rx.vstack(
                rx.heading("✅ Check-In Successful!", size="7"),
                rx.button(
                    "Next Guest",
                    on_click=State.reset_checkin,
                    width="100%"
                ),
                spacing="4",
                align="center"
            ),

            rx.vstack(
                rx.heading("Guest Check-In", size="7"),

                rx.input(
                    placeholder="Scan QR Code",
                    value=State.search_id,
                    on_change=State.set_search_id,
                    auto_focus=True,
                    width="100%"
                ),

                rx.button(
                    "Confirm",
                    on_click=State.check_in_guest,
                    width="100%"
                ),

                spacing="4",
                width="90%",
                max_width="400px"
            )
        ),
        height="100vh"
    )
