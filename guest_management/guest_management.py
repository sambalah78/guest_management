import reflex as rx
import asyncio
import pandas as pd
import io
from guest_management.pages.home_page import home as home_page
from guest_management.pages.sign_in import login_page
from guest_management.pages import dashboard
from guest_management.pages import check_in
# --- STATE LOGIC ---
class State(rx.State):
    """The app state."""

    username: str = ""
    password: str = ""
    error_message: str = ""
    guest_data: list[dict] = []
    columns: list[str] = []
    selected_filename: str = ""  # The error is likely here
    is_processing: bool = False

    def handle_file_select(self, files: list[rx.UploadFile]):
        if files:
            # Reflex automatically creates 'set_selected_filename'
            # only if 'selected_filename' is defined above.
            self.selected_filename = files[0].filename

    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            rx.window_alert("No file selected.")

        self.is_processing = True
        yield

        for file in files:
            upload_data = await file.read()
            df = pd.read_excel(io.BytesIO(upload_data))

            # --- Add Status Column ---
            # We add 'Status' at the beginning (index 0) or end.
            # This ensures every guest starts as 'Absent'.
            if "Status" not in df.columns:
                df["Status"] = "Absent"

            df = df.fillna("")

            self.columns = df.columns.tolist()
            # Convert to list of dicts for the table
            self.guest_data = [
                {str(k): str(v) for k, v in record.items()}
                for record in df.to_dict("records")
            ]

        self.is_processing = False
        self.selected_filename = ""

    def login(self):
        """Simple authentication check."""
        # Replace 'admin' and 'password123' with your desired credentials
        if self.username == "admin" and self.password == "password":
            self.error_message = ""
            return rx.redirect("/dashboard")
        else:
            self.error_message = "Invalid username or password."
            return None

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

app = rx.App()
# Add pages and link the splash logic to the index 'on_load'
app.add_page(index, route="/", on_load=State.splash_logic)
app.add_page(home_page, route="/home")
app.add_page(login_page, route="/login")
app.add_page(dashboard.dashboard, route="/dashboard")
app.add_page(check_in.checkin_page, route="/check-in")
