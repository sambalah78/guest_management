import reflex as rx
from ..state import State
from guest_management.widget.table import guest_table
from guest_management.widget import stat_card
from guest_management.state import State

GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"

def dashboard() -> rx.Component:
    return rx.vstack(
        # Navbar
        rx.hstack(
            rx.heading("Empire Dashboard", color="#D4AF37", size="6"),
            rx.spacer(),
            rx.button("Log Out", on_click=rx.redirect("/"), variant="outline", color="#D4AF37", border="1px solid #D4AF37"),
            width="100%", padding="1em 2em", background="#1A1A1A", border_bottom="1px solid #D4AF37",
        ),
        # Content
        rx.grid(
            # Left: Controls & Stats
            rx.vstack(
                rx.hstack(
                    stat_card.stat_card("Total Guests", State.total_count, "users", "#D4AF37"),
                    stat_card.stat_card("Present", State.present_count, "check-circle", "#4CAF50"),
                    stat_card.stat_card("Absent", State.absent_count, "user-minus", "#F44336"),
                    width="100%", spacing="4",
                ),
                rx.upload(
                    rx.center(rx.text("Drop Excel here or Click to Upload", color="gray")),
                    id="upload_guest", border="1px dashed #D4AF37", padding="2em", width="100%", border_radius="10px",
                ),
                rx.button("Sync Guest List", on_click=State.handle_upload(rx.upload_files(upload_id="upload_guest")), bg="#D4AF37", color="black", width="100%"),
                spacing="4", width="100%",
            ),
            # Right: QR Code
            rx.vstack(
                rx.heading("Entry QR Code", size="4", color="#D4AF37"),
                rx.image(src=State.qr_code_url, width="180px", border="4px solid white", border_radius="5px"),
                rx.text("Guests scan this to check-in", color="gray", size="2"),
                background="#1A1A1A", padding="2em", border_radius="15px", align="center", border="1px solid #D4AF37",
            ),
            columns="2", spacing="6", width="100%", grid_template_columns="2fr 1fr",
        ),
        # Table Section
        rx.vstack(
            rx.input(placeholder="Search by name, table, or status...", on_change=State.set_search_query, width="100%", bg="#1A1A1A", border="1px solid #333", color="white"),
            rx.cond(State.guest_data, guest_table(), rx.center(rx.text("No guests imported yet.", color="gray"), width="100%", padding="4em")),
            width="100%", spacing="4",
        ),
        width="100%", min_height="100vh", background="#111111", padding="2em", spacing="8",
    )