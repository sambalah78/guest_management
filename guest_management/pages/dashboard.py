import reflex as rx

from ..state import State

from guest_management.widget import stat_card

GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"
TEXT_WHITE = "#FFFFFF"


def dashboard():
    return rx.vstack(
        rx.hstack(
            rx.heading("Empire Dashboard", color="#D4AF37"),
            rx.spacer(),
            rx.button("Log Out", on_click=rx.redirect("/"), variant="outline", color="#D4AF37"),
            width="100%", padding="1em", bg="#1A1A1A"
        ),
        rx.grid(rx.hstack(
            stat_card.stat_card("Total Guests", State.total_count, "users", "#D4AF37"),
            stat_card.stat_card("Present", State.present_count, "check-circle", "#4CAF50"),
            stat_card.stat_card("Absent", State.absent_count, "user-minus", "#F44336"),

        ), width="100%", spacing="4"),
        rx.hstack(
            rx.upload(rx.button("Select Excel"), id="u_guest", border="1px dashed #D4AF37", padding="1em"),
            rx.button("Upload", on_click=State.handle_upload(rx.upload_files(upload_id="u_guest")), bg="#D4AF37"),
            rx.button(
                "Clear Table",
                on_click=State.clear_table,
                variant="outline",
                color_scheme="red",
                border="1px solid #F44336"
            ),
            rx.button(
                rx.icon(tag="refresh-cw", mr="2"),
                "Refresh Data",
                on_click=State.load_guests,
                variant="soft",
                color_scheme="blue"
            ),
            rx.vstack(
                rx.heading("Entry QR Code", size="4", color="#D4AF37"),
                rx.image(src=State.qr_url, width="180px", border="5px solid white"),
                rx.text("Scan to Check-In", color="gray", size="2"),
                bg="#1A1A1A", padding="2em", border_radius="15px", border="1px solid #D4AF37", align="center"
            ),
            width="100%", align="center"
        ),
        rx.input(placeholder="Search Table...", on_change=State.set_search_query, width="100%"),
        rx.table.root(
            rx.table.header(rx.table.row(rx.foreach(State.columns, rx.table.column_header_cell))),
            rx.table.body(
                rx.foreach(State.filtered_data, lambda row: rx.table.row(
                    rx.foreach(State.columns, lambda col: rx.table.cell(
                        rx.cond(col == "Status",  # In your table logic (dashboard.py or table.py)
                                rx.badge(
                                    row[col],
                                    # This must match "Present" exactly
                                    color_scheme=rx.cond(row[col] == "Present", "green", "red")
                                ), row[col])
                    ))
                ))
            ),
            width="100%"
        ),
        padding="2em", bg="gray", min_height="100vh"
    )
