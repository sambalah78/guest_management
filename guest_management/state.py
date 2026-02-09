import reflex as rx
import pandas as pd
import io
import os
import socket


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






    @rx.var
    def get_base_url(self) -> str:
        # Reflex sets specific env vars when deployed
        # If we are on the cloud, use the production URL
        # If we are local, use the computer's IP
        if os.environ.get("REFLEX_CLOUD") or os.environ.get("PRODUCTION"):
            return "https://your-app-name.reflex.run"

            # Fallback to local IP detection logic
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return f"http://{ip}:3000"
        except:
            return "http://localhost:3000"

    def qr_url(self) -> str:
        # This ensures the QR code always points to the /check-in route
        return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={self.get_base_url}/check-in"
        # URL for QR Code (Change this after deployment)
        # deploy_url: str = "https://your-app-name.reflex.run/check-in"

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

    # @rx.var
    # def qr_url(self) -> str:
    #     target = self.deploy_url if self.deploy_url else self.local_ip
    #     return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={target}"

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
        """Matches Name or ID (Case-Insensitive)"""
        n_in = self.search_name.strip().lower()
        i_in = self.search_id.strip().lower()
        if not n_in and not i_in:
            return rx.window_alert("Please enter your Name or ID.")

        found = False
        # Identify columns dynamically
        name_col = next((c for c in self.columns if c.lower() in ["name", "full name", "guest"]), None)
        id_col = next((c for c in self.columns if c.lower() in ["id", "guest id", "code"]), None)

        new_data = []
        for g in self.guest_data:
            db_n = str(g.get(name_col, "")).strip().lower() if name_col else ""
            db_i = str(g.get(id_col, "")).strip().lower() if id_col else ""

            if (n_in and n_in == db_n) or (i_in and i_in == db_i):
                g["Status"] = "Present"
                found = True
            new_data.append(g)

        self.guest_data = new_data
        if found:
            self.search_name = ""
            self.search_id = ""
            return rx.window_alert("Check-in Successful! Welcome.")
        return rx.window_alert("Details not found. Please contact the host.")

    def login(self):
        if self.username == "admin" and self.password == "password":
            return rx.redirect("/dashboard")
        self.error_message = "Invalid Credentials"