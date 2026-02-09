import reflex as rx

def stat_card(label: str, value: int, icon: str, color: str):
    return rx.vstack(
        rx.hstack(
            rx.icon(tag=icon, color=color, size=20),
            rx.text(label, color="gray", size="2"),
            spacing="2",
        ),
        # value comes directly from State.total_count etc.
        rx.heading(value.to(str), size="6", color="white"),
        background="#1A1A1A",
        padding="1.5em",
        border_radius="10px",
        border=f"1px solid {color}44",
        width="100%",
    )