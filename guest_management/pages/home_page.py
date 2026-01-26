import reflex as rx


def feature_card(icon_tag: str, title: str, desc: str):
    return rx.vstack(
        rx.icon(tag=icon_tag, size=30, color="blue"),
        rx.heading(title, size="4"),
        rx.text(desc, color_override="gray", text_align="center"),
        padding="2em",
        border="1px solid #e5e7eb",
        border_radius="15px",
        width="100%",
    )


def home() -> rx.Component:
    return rx.vstack(
        # --- Navigation (Updated to hstack) ---
        rx.hstack(
            rx.heading("Empire Signature", size="7"),
            rx.spacer(),
            rx.hstack(
                rx.link("Features", href="#features"),
                rx.button("Get Started"),
                spacing="4",
                align="center",
            ),
            width="100%",
            padding="1.5em",
            border_bottom="1px solid #f0f0f0",
        ),
        # --- Hero Section ---
        rx.center(
            rx.hstack(
                rx.vstack(
                    rx.heading("Manage Guest faster wiht Us", size="9"),
                    rx.text("No manual seacrhing, its", size="5"),
                    rx.button("Start Now", size="3", variant="soft"),
                    spacing="5",
                    padding_y="10vh",
                    align="center",
                ),
                rx.image(
                    src="empire.jpg",
                    alt="Empire Signature Logo",
                    width=["150px", "200px", "250px", "300px", "350px"],
                ),
                gap="5vw",
                align_item="center",
                # width="80%",
            ),
            width="100%",
        ),
        # --- Features Section ---
        rx.grid(
            feature_card("zap", "Fast", "Get Guest info in milliseconds."),
            feature_card("lock", "Secure", "Guest data is protected with encryption."),
            feature_card("code", "Simple", "Upload and manage guests with ease."),
            columns="3",
            spacing="4",
            width="80%",
            id="features",
        ),
        width="100%",
        align="center",
    )
