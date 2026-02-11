import reflex as rx
from ..state import State
from ..widget import stat_card

GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"
TEXT_WHITE = "#FFFFFF"

def dashboard():
    return rx.vstack(


        rx.hstack(
            rx.heading("Empire Dashboard", color="#D4AF37"),
            rx.grid(rx.hstack(
                stat_card.stat_card("Total Guests", State.total_count, "users", "#D4AF37"),
                stat_card.stat_card("Present", State.present_count, "user-plus", "#4CAF50"),
                stat_card.stat_card("Absent", State.absent_count, "user-minus", "#F44336"),

            ), width="60%", spacing="4"),

            rx.button("Log Out", on_click=rx.redirect("/"), variant="outline", color="#D4AF37"),
            width="100%", padding="1em", bg="#1A1A1A",justify="between",
        ),

        rx.hstack(
            rx.upload(
                    rx.button("Select Excel File", border="1px dashed #D4AF37"),
                    id="u_guest",
                    multiple=False,
                    accept={"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
                           "application/vnd.ms-excel": [".xls"]},border="none",padding="0,5em",
                ),
            rx.cond(
                State.uploaded_filename != "",
                rx.text(
                    f"Selected: {State.uploaded_filename}",
                    size="1",
                    color=GOLD,
                    font_style="italic"
                )
            ),


                    rx.button("Upload",
                             on_click=lambda: State.handle_upload(rx.upload_files(upload_id="u_guest")),
                             bg="#D4AF37"),
                    rx.button("Clear Table",
                             on_click=State.clear_table,
                             variant="outline",
                             color_scheme="red",
                             border="1px solid #F44336"),



            rx.button(
                "↻ Refresh Data",
                on_click=State.load_guests,
                variant="soft",
                color_scheme="blue",
                size="2"
            ),
            rx.button(
                "📱 Show QR",
                on_click=State.show_qr_dialog,
                bg="transparent",
                border=f"1px solid {GOLD}",
                color=GOLD,
                _hover={"bg": "rgba(212, 175, 55, 0.1)"}
            ),

            # rx.vstack(
            #     rx.heading("Entry QR Code", size="4", color="#D4AF37"),
            #     # rx.image(src=State.qr_url, width="180px", border="5px solid white"),
            #     rx.text("Scan to Check-In", color="gray", size="2"),
            #     bg="#1A1A1A", padding="2em", border_radius="15px", border="1px solid #D4AF37", align="center"
            # ),
            width="100%", spacing="4", align="center",
        ),
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.alert_dialog.title(
                    "Guest Check-In QR Code",
                    color=GOLD,
                    size="6",

                ),
                rx.alert_dialog.description(
                    rx.vstack(

                        rx.image(
                            src=State.qr_url,
                            width="300px",
                            height="300px",
                            border=f"8px solid {GOLD}",
                            border_radius="15px",
                            box_shadow="0 0 20px rgba(212, 175, 55, 0.3)"
                        ),
                        rx.text(
                            "Scan this QR code with your phone camera to check in",
                            color="gray",
                            size="2",
                            text_align="center"
                        ),
                        rx.hstack(

                            rx.button(
                                "Close",
                                on_click=State.close_qr_dialog,
                                variant="soft",
                                color_scheme="gray",
                                color="white"
                            ),
                            spacing="3",
                            justify="center",
                            width="100%",
                            padding_top="1em"
                        ),
                        spacing="4",
                        align="center",
                        width="100%"
                    )
                ),
                bg=DARK_GRAY,
                border=f"2px solid {GOLD}",
                max_width="500px",
                padding="2em",

            ),
            open=State.qr_dialog_open,

        ),
        rx.input(
            placeholder="Search Table...",
            on_change=State.set_search_query,
            width="100%",
            size="3"
        ),
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
                                            color_scheme=rx.cond(row[col] == "Present", "green", "red"),
                                            radius="full",
                                            variant="soft"
                                        ),
                                        row[col]
                                    )
                                )
                            )
                        )
                    )
                ),
                width="100%", variant="surface"
            ),
            rx.text("No guest data available. Please upload an Excel file.",
                   color="gray", padding="2em")
        ),
        padding="2em", bg=BLACK, min_height="100vh", spacing="4",
    )