import reflex as rx

from guest_management import state
from guest_management.widget import table
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
            stat_card.stat_card("Total Guests", state.State.total_count, "users", "#D4AF37"),
            stat_card.stat_card("Present", state.State.present_count, "check-circle", "#4CAF50"),
            stat_card.stat_card("Absent", state.State.absent_count, "user-minus", "#F44336"),

        ),width="100%", spacing="4"),
        rx.hstack(
            rx.upload(rx.button("Select Excel"), id="u_guest", border="1px dashed #D4AF37", padding="1em"),
            rx.button("Sync", on_click=state.State.handle_upload(rx.upload_files(upload_id="u_guest")), bg="#D4AF37"),
            rx.vstack(
                rx.heading("Entry QR Code", size="4", color="#D4AF37"),
                rx.image(src=state.State.qr_url, width="180px", border="5px solid white"),
                rx.text("Scan to Check-In", color="gray", size="2"),
                bg="#1A1A1A", padding="2em", border_radius="15px", border="1px solid #D4AF37", align="center"
            ),
            width="100%", align="center"
        ),
        rx.input(placeholder="Search Table...", on_change=state.State.set_search_query, width="100%"),
        rx.table.root(
            rx.table.header(rx.table.row(rx.foreach(state.State.columns, rx.table.column_header_cell))),
            rx.table.body(
                rx.foreach(state.State.filtered_data, lambda row: rx.table.row(
                    rx.foreach(state.State.columns, lambda col: rx.table.cell(
                        rx.cond(col == "Status", rx.badge(row[col], color_scheme="green"), row[col])
                    ))
                ))
            ),
            width="100%"
        ),
        padding="2em", bg="gray", min_height="100vh"
    )