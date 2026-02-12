import reflex as rx
GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"
TEXT_WHITE = "#FFFFFF"
def success_page():
    return rx.center(
        rx.vstack(
            rx.image(src="empire.jpg", width=["150px","200px","300px","350px"], border=f"1px solid {GOLD}",
                         border_radius="15px",padding="1" ),
            rx.heading("Check-In Successful!", size="7"),
            rx.text("Welcome to Empire Signature Event",color=GOLD),

            spacing="4",
            align="center"
        ),
        height="100vh",
        bg="#111111",


    )
