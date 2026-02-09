import reflex as rx

def stat_card(label, val, icon, color):
    return rx.vstack(
        rx.hstack(rx.icon(tag=icon, color=color, size=18), rx.text(label, size="2", color="gray")),
        rx.heading(val.to(str), size="6", color="white"),
        padding="1.5em", bg="#1A1A1A", border=f"1px solid {color}33", border_radius="12px", width="100%"
    )