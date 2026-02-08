import reflex as rx

from guest_management import guest_management
from guest_management.widget import table

GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"
TEXT_WHITE = "#FFFFFF"


def dashboard() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Dashboard", size="6", color=GOLD),

            rx.spacer(),
            rx.button(
                "Log Out",
                on_click=rx.redirect("/"),
                variant="outline",
                border=f"1px solid {GOLD}",
                color=GOLD
            ),
            width="100%",
            padding="1em 2em",
            background=DARK_GRAY,
            border_bottom=f"1px solid {GOLD}",
        ),

        rx.vstack(

            rx.divider(border_color=GOLD),
            rx.card(
                rx.hstack(
                    rx.heading("Guest Overview", size="4", color=GOLD),
                    rx.text("Status: All systems operational", color="white"),
                ),
                background=DARK_GRAY,
                border=f"1px solid {GOLD}",
                width="100%",
            ),
             rx.upload(
                rx.vstack(
                    rx.button("Select Excel File", color="#D4AF37", bg="#1A1A1A", border="1px solid #D4AF37"),
                    rx.text("Drag and drop or click to upload guest list", color="gray"),
                ),
                id="upload_guest",
                border=f"1px dashed #D4AF37",
                padding="2em",
                border_radius="10px",
                width="100%",
            ),
            rx.button(
                "Process & Display List",
                on_click=guest_management.State.handle_upload(rx.upload_files(upload_id="upload_guest")),
                background="#D4AF37",
                color="black",
                # margin_top="1em",
            ),

            # --- The Data Table ---
            rx.cond(
                guest_management.State.guest_data,
                table.guest_table(),
                rx.center(
                    rx.text("No guests loaded. Upload an Excel file to begin.", color="gray", margin_top="2em"),
                    width="100%"
                )
            ),
            align="start",
            spacing="4",
            width="100%"
        ),

        width="100%",
        min_height="100vh",
        background=BLACK,
        padding="2em"
    )
