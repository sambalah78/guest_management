import reflex as rx
from guest_management.state import State

def guest_table() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.foreach(State.columns, lambda col: rx.table.column_header_cell(col, color="black"))
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
                                rx.text(row[col], color="black")
                            )
                        )
                    )
                )
            )
        ),
        width="100%", variant="surface",
    )