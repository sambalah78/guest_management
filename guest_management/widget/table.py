import reflex as rx
from guest_management.state import State
GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"
TEXT_WHITE = "#FFFFFF"
def guest_table() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.foreach(State.columns, lambda col: rx.table.column_header_cell(col))
            )
        ),
        rx.table.body(
            rx.foreach(
                State.filtered_guest_data,
                lambda row: rx.table.row(
                    rx.foreach(
                        State.columns,
                        lambda col: rx.table.cell(
                            rx.cond(
                                col == "Status",
                                rx.badge(
                                    row[col],
                                    variant="solid",
                                    color_scheme=rx.cond(row[col] == "Present", "green", "gold")
                                ),
                                rx.text(row[col], color="white")
                            )
                        )
                    )
                )
            )
        ),
        width="100%", variant="surface",
    )