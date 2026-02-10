import base64

import reflex as rx

import os

import asyncio
import pandas as pd
import io
import base64
import qrcode
import sqlalchemy  # Ensure this is imported



class Guest(rx.Model, table=True):
    name: str
    guest_id: str
    status: str = "Absent"

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

    async def splash_logic(self):
        # Wait 2 seconds
        await asyncio.sleep(2)
        # Redirect to /home
        return rx.redirect("/home")

    @rx.var
    def get_base_url(self) -> str:
        # Reflex sets specific env vars when deployed
        # If we are on the cloud, use the production URL
        # If we are local, use the computer's IP
        if os.environ.get("REFLEX_CLOUD") or os.environ.get("PRODUCTION"):
            return "https://your-app-name.reflex.run/check-in"

            # Fallback to local IP detection logic
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return f"http://{ip}:3000"
        except:
            return "http://192.168.100.68:3000"

    @rx.var
    def qr_url(self) -> str:
        # This ensures the QR code always points to the /check-in route
        return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={self.get_base_url}/checkin"
        # return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={self.get_base_url}/check-in"
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

    def clear_table(self):
        """Physically wipes the database and resets the UI."""
        with rx.session() as session:
            session.execute(sqlalchemy.delete(Guest))
            session.commit()
        self.guest_data = []
        self.columns = []
        return rx.toast.success("Database and UI cleared.")
    # @rx.var
    # def qr_url(self) -> str:
    #     target = self.deploy_url if self.deploy_url else self.local_ip
    #     return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={target}"

    # --- Actions ---
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            data = await file.read()
            df = pd.read_excel(io.BytesIO(data))

            # Standardize 'Status'
            if "Status" not in df.columns:
                df["Status"] = "Absent"

            df = df.fillna("")
            self.columns = df.columns.tolist()
            self.guest_data = df.to_dict("records")

            # SAVE TO DATABASE for cross-session check-in
            with rx.session() as session:
                for _, row in df.iterrows():
                    session.add(
                        Guest(
                            name=str(row.get("Name", row.get("name", ""))),
                            guest_id=str(row.get("ID", row.get("guest_id", ""))),
                            status="Absent"
                        )
                    )
                session.commit()
        return rx.toast.success("List uploaded and database synced!")

    # In state.py

    def load_guests(self):
        """Pulls the latest data from the database to refresh the dashboard."""
        with rx.session() as session:
            # Query all guests from the DB
            guests = session.exec(Guest.select()).all()

            # Update the UI list
            self.guest_data = [
                {
                    "Name": g.name,
                    "ID": g.guest_id,
                    "Status": g.status,
                    # Add any other columns you need here
                }
                for g in guests
            ]
        return rx.toast.success("Dashboard Updated!")

    def check_in_guest(self):
        n_in = self.search_name.strip()
        i_in = self.search_id.strip()

        with rx.session() as session:
            guest = session.exec(
                Guest.select().where(
                    (Guest.name.ilike(f"%{n_in}%")) |
                    (Guest.guest_id == i_in)
                )
            ).first()

            if guest:
                guest.status = "Present"
                session.add(guest)
                session.commit()

                self.search_name = ""
                self.search_id = ""

                # Feedback for the guest
                yield rx.toast.success(f"Welcome, {guest.name}!", duration=4000)

                # OPTIONAL: Redirect guest to a thank you page
                # yield rx.redirect("/thank-you")
            else:
                yield rx.toast.error("Guest not found.")

    @rx.var
    def qr_code_image(self) -> str:
        """Offline generation of QR code pointing to local IP."""
        # Use your computer's IP (e.g. 192.168.x.x) here for mobile testing
        url = "http://192.168.100.68:3000/checkin"
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"

    def login(self):
        if self.username == "admin" and self.password == "password":
            return rx.redirect("/dashboard")
        self.error_message = "Invalid Credentials"
