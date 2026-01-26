import reflex as rx
import asyncio
from guest_management.pages.home_page import home as home_page


# --- STATE LOGIC ---
class State(rx.State):
    """The app state."""

    async def splash_logic(self):
        # Wait 2 seconds
        await asyncio.sleep(2)
        # Redirect to /home
        return rx.redirect("/home")


# --- COMPONENT: FEATURE CARD ---
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


# --- PAGE: SPLASH SCREEN ---
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.image(src="empire.jpg", width="100px", height="auto"),
            rx.heading("Empire Signature", size="8", weight="bold"),
            rx.text("Loading Guest Manager...", color_scheme="gray"),
            rx.spinner(size="3"),
            spacing="4",
            align="center",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle, #ffffff 0%, #f0f0f0 100%)",
    )


# --- PAGE: HOME ---
# def home_page() -> rx.Component:
#     return rx.vstack(
#         rx.hstack(
#             rx.heading("Empire Signature", size="7"),
#             rx.spacer(),
#             rx.hstack(
#                 rx.link("Features", href="#features"),
#                 rx.button("Get Started"),
#                 spacing="4",
#                 align="center",
#             ),
#             width="100%",
#             padding="1.5em",
#             border_bottom="1px solid #f0f0f0",
#         ),
#         rx.center(
#             rx.hstack(
#                 rx.vstack(
#                     rx.heading("Manage Guest faster with Us", size="9"),
#                     rx.text("No manual searching, it's instant.", size="5"),
#                     rx.button("Start Now", size="3", variant="soft"),
#                     spacing="5",
#                     padding_y="10vh",
#                     align="start",
#                 ),
#                 rx.image(
#                     src="/empire.jpg",
#                     width=["150px", "300px"],
#                 ),
#                 gap="5vw",
#                 align="center",
#             ),
#             width="100%",
#         ),
#         rx.grid(
#             feature_card("zap", "Fast", "Get Guest info in milliseconds."),
#             feature_card("lock", "Secure", "Data is protected."),
#             feature_card("code", "Simple", "Manage with ease."),
#             columns="3",
#             spacing="4",
#             width="80%",
#             id="features",
#         ),
#         width="100%",
#         align="center",
#     )


# --- APP SETUP ---
app = rx.App()
# Add pages and link the splash logic to the index 'on_load'
app.add_page(index, route="/", on_load=State.splash_logic)
app.add_page(home_page, route="/home")
