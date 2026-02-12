import reflex as rx
from ..state import State


def dashboard():
    return rx.vstack(

        rx.hstack(
            rx.heading("Empire Dashboard"),
            rx.spacer(),
            rx.text(f"Total: {State.total_count}"),
            rx.text(f"Present: {State.present_count}"),
            rx.text(f"Absent: {State.absent_count}"),
            width="100%"
        ),

        rx.upload(
            rx.button("Upload Excel"),
            id="u1",
            multiple=False
        ),

        rx.button(
            "Confirm Upload",
            on_click=lambda: State.handle_upload(
                rx.upload_files(upload_id="u1")
            )
        ),

        rx.input(
            placeholder="Search...",
            on_change=State.set_search_query,
            width="100%"
        ),

        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Guest ID"),
                    rx.table.column_header_cell("Status"),
                )
            ),
            rx.table.body(
                rx.foreach(
                    State.guests,
                    lambda guest: rx.table.row(
                        rx.table.cell(guest.name),
                        rx.table.cell(guest.email),
                        rx.table.cell(guest.guest_id),
                        rx.table.cell(
                            rx.badge(
                                guest.status,
                                color_scheme=rx.cond(
                                    guest.status == "Present",
                                    "green",
                                    "red"
                                )
                            )
                        )
                    )
                )
            ),
            width="100%"
        ),

        spacing="4",
        padding="2em",
        width="100%"
    )
