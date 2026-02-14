import reflex as rx
from ..state import State
from ..components import stat_card

GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"


def dashboard():
    return rx.vstack(

        # ================= HEADER =================
        rx.hstack(
            rx.heading("Empire Event Dashboard", size="6", color=GOLD),
            rx.grid(
                stat_card.stat_card("Total Guests", State.total_count, "users", GOLD),
                stat_card.stat_card("Present", State.present_count, "user-plus", "#4CAF50"),
                stat_card.stat_card("Absent", State.absent_count, "user-minus", "#F44336"),
                columns="3",
                # spacing="3",
                width="100%",
                padding="0.5em 0",
            ),

            rx.button(
                "📱 QR Code",
                on_click=State.show_qr_dialog,
                variant="outline",
                border=f"1px solid {GOLD}",
                color=GOLD,
            ),
            rx.button(
                "Log Out",
                on_click=rx.redirect("/"),
                variant="outline",
                border=f"1px solid {GOLD}",
                color=GOLD,
            ),
            width="100%",
            align="center",
            padding="0.5em",
            bg=DARK_GRAY,
            border_bottom=f"1px solid {GOLD}",
        ),

        # ================= STATS =================

        # ================= FILE UPLOAD =================
        rx.card(
            rx.vstack(
                rx.heading("Upload Guest List"

                           , size="4", color=GOLD),

                rx.hstack(
                    rx.upload(
                        rx.button("Select Excel File", border="1px dashed #D4AF37", bg="#D4AF37"),
                        id="u_guest",
                        multiple=False,
                        accept={
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
                            "application/vnd.ms-excel": [".xls"],
                        },
                    ),
                    rx.button(
                        "Upload",
                        on_click=lambda: State.handle_upload(
                            rx.upload_files(upload_id="u_guest")
                        ),
                        bg="#D4AF37"
                    ),

                    rx.button(
                        "Clear",
                        on_click=State.clear_table,
                        variant="outline",
                        color_scheme="red", bg="#D4AF37"
                    ),
                    spacing="4",
                ),

                rx.cond(
                    State.uploaded_filename != "",
                    rx.text(
                        f"Selected: {State.uploaded_filename}",
                        size="2",
                        color=GOLD,
                    ),
                ),

                spacing="4",
            ),
            bg=DARK_GRAY,
            padding="2em",
            width="100%",
        ),

        # ================= SEARCH =================
        rx.input(
            placeholder="Search guest...",
            on_change=State.set_search_query,
            size="3",
            width="100%",
        ),

        # ================= TABLE =================
        rx.box(
            rx.cond(
                State.guest_data.length() > 0,

                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.foreach(
                                State.columns,
                                lambda col: rx.table.column_header_cell(col)
                            )
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            State.filtered_data,
                            lambda row: rx.table.row(
                                rx.foreach(
                                    State.columns,
                                    lambda col: rx.table.cell(
                                        rx.cond(
                                            col == "Status",
                                            rx.badge(
                                                row[col],
                                                color_scheme=rx.cond(
                                                    row[col] == "Present",
                                                    "green",
                                                    "red"
                                                ),
                                                radius="full",
                                                variant="soft",
                                            ),
                                            row[col],
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    variant="surface",
                    size="2",
                ),

                rx.center(
                    rx.text(
                        "No guest data available. Upload an Excel file.",
                        color="gray",
                    ),
                    padding="2em",
                ),
            ),
            max_height="500px",
            overflow_y="auto",
            width="100%",
            border=f"1px solid {GOLD}",
            border_radius="10px",
        ),

        # ================= QR DIALOG =================
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.alert_dialog.title("Guest Check-In QR Code", color=GOLD),
                rx.vstack(
                    rx.image(
                        src=State.qr_url,
                        width="280px",
                        height="280px",
                        border=f"6px solid {GOLD}",
                        border_radius="12px",
                    ),
                    rx.text(
                        "Scan to check in",
                        color="gray",
                    ),
                    rx.button(
                        "Close",
                        on_click=State.close_qr_dialog,
                        variant="soft",
                    ),
                    spacing="4",
                    align="center",
                ),
                bg=DARK_GRAY,
                border=f"2px solid {GOLD}",
                padding="2em",
            ),
            open=State.qr_dialog_open,
        ),

        padding="2em",
        bg=BLACK,
        min_height="100vh",
        spacing="6",
    )
