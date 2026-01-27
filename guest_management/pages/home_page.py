import reflex as rx

GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"
TEXT_WHITE = "#FFFFFF"


def feature_card(icon_tag: str, title: str, desc: str):
    return rx.vstack(
        rx.icon(tag=icon_tag, size=30, color=GOLD),
        rx.heading(title, size="4", color=GOLD),
        rx.text(desc, color="gray", text_align="center"),
        padding="2em",
        background=DARK_GRAY,
        border=f"1px solid {GOLD}",
        border_radius="15px",
        width="100%",
        _hover={"transform": "translateY(-5px)", "transition": "0.3s"},
    )


def home() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.heading("Empire Signature", size="7", color=GOLD),
            rx.spacer(),
            # rx.button(
            #     "Admin Sign In",
            #     on_click=rx.redirect("/login"),
            #     variant="ghost",
            #     color=GOLD,
            #     color_scheme="gold",
            #     _hover={"background": "transparent", "opacity": "0.8"}
            # ),
            width="100%",
            padding="1.5em",
            border_bottom=f"1px solid {GOLD}",
        ),
        rx.center(
            rx.hstack(
                rx.vstack(
                    rx.heading("Manage Guests with Elegance", size="9", color=TEXT_WHITE),
                    rx.text("Automated solutions for the elite.", size="5", color="gray"),
                    rx.button(
                        "Get Started",
                        size="3",
                        background=GOLD,
                        color=BLACK,
                        on_click=rx.redirect("/login"),
                        _hover={"opacity": "0.9"}
                    ),
                    spacing="5",
                    padding_y="10vh",
                    align="center",
                ),
                rx.image(src="empire.jpg", width="300px", border=f"1px solid {GOLD}",
                         border_radius="15px", ),
                gap="5vw",
                align="center",
            ),
        ),
        rx.grid(
            feature_card("zap", "Fast", "Real-time processing."),
            feature_card("lock", "Secure", "Encrypted data vaults."),
            feature_card("code", "Simple", "Refined user interface."),
            columns="3",
            spacing="4",
            width="80%",
            padding_bottom="5em",
        ),
        width="100%",
        background=BLACK,
        min_height="100vh",
        align="center"
    )
