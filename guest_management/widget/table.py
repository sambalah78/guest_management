import reflex as rx
from guest_management import guest_management


def guest_table() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.foreach(
                    guest_management.State.columns,
                    lambda col: rx.table.column_header_cell(col, color="#D4AF37")
                )
            )
        ),
        rx.table.body(
            rx.foreach(
                guest_management.State.guest_data,
                lambda row: rx.table.row(
                    rx.foreach(
                        guest_management.State.columns,
                        lambda col: rx.table.cell(
                            # Conditional styling: If the column is 'Status',
                            # give it a border/badge look.
                            rx.cond(
                                col == "Status",
                                rx.badge(
                                    row[col],
                                    variant="outline",
                                    color_scheme="gold", # Custom feel
                                    border=f"1px solid #D4AF37"
                                ),
                                rx.text(row[col], color="white")
                            )
                        )
                    )
                )
            )
        ),
        width="100%",
        variant="surface",
        margin_top="2em",
    )