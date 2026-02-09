import reflex as rx
import pandas as pd
import io
import asyncio


class State(rx.State):
    """Central State for Empire Signature."""
    # Data
    guest_data: list[dict] = []
    columns: list[str] = []

    # Inputs
    username: str = ""
    password: str = ""
    error_message: str = ""
    search_query: str = ""  # Dashboard search
    search_name: str = ""  # Guest check-in name
    search_id: str = ""  # Guest check-in ID

    # URL for QR Code (Change this after deployment)
    deploy_url: str = "https://your-app-name.reflex.run/check-in"

    # --- Computed Vars (Default to 0) ---
    @rx.var
    def total_count(self) -> int:
        return len(self.guest_data)

    @rx.var
    def present_count(self) -> int:
        return len([g for g in self.guest_data if g.get("Status") == "Present"])

    @rx.var
    def absent_count(self) -> int:
        return len([g for g in self.guest_data if g.get("Status") == "Absent"])

    @rx.var
    def filtered_data(self) -> list[dict]:
        if not self.search_query:
            return self.guest_data
        term = self.search_query.lower()
        return [g for g in self.guest_data if any(term in str(v).lower() for v in g.values())]

    @rx.var
    def qr_url(self) -> str:
        return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={self.deploy_url}"

    # --- Actions ---
    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files: return
        for file in files:
            data = await file.read()
            df = pd.read_excel(io.BytesIO(data))
            if "Status" not in df.columns:
                df["Status"] = "Absent"
            df = df.fillna("")
            self.columns = df.columns.tolist()
            self.guest_data = df.to_dict("records")

    def check_in_guest(self):
        """Robust Name & ID Matching."""
        name_in = self.search_name.strip().lower()
        id_in = self.search_id.strip().lower()

        if not name_in and not id_in:
            return rx.window_alert("Please enter Name or ID.")

        # Detect columns dynamically
        name_col = next((c for c in self.columns if c.lower() in ["name", "full name", "guest"]), None)
        id_col = next((c for c in self.columns if c.lower() in ["id", "guest id", "code"]), None)

        found = False
        new_list = []
        for g in self.guest_data:
            db_name = str(g.get(name_col, "")).strip().lower() if name_col else ""
            db_id = str(g.get(id_col, "")).strip().lower() if id_col else ""

            if (name_in and name_in == db_name) or (id_in and id_in == db_id):
                g["Status"] = "Present"
                found = True
            new_list.append(g)

        self.guest_data = new_list
        if found:
            self.search_name = ""
            self.search_id = ""
            return rx.window_alert("Check-in Successful!")
        return rx.window_alert("Guest not found.")

    def login(self):
        if self.username == "admin" and self.password == "password":
            return rx.redirect("/dashboard")
        self.error_message = "Invalid Credentials"