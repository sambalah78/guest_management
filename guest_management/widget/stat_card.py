import reflex as rx

def stat_box(label, val, color):
    return rx.vstack(
        rx.text(label, color="gray", size="2"),
        rx.heading(val.to(str), size="6", color="white"),
        padding="1em", bg="#1A1A1A", border=f"1px solid {color}44", border_radius="8px", width="100%"
    )