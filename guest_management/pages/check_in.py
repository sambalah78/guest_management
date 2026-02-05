import reflex as rx
from guest_management import guest_management
def checkin():
    return rx.center(
        rx.card(
            rx.vstack(
                rx.heading("Welcome!"),
                rx.text("Please enter your name to check-in:"),
                rx.input(placeholder="Enter Full Name", value=guest_management.State.search_name, on_change=guest_management.State.set_search_name),
                rx.button("Check-In", on_click=guest_management.State.check_in_guest, width="100%", color_scheme="gold"),
                spacing="4"
            ),
            padding="2em"
        ),
        height="100vh"
    )