import base64
import reflex as rx
import os
import asyncio
import pandas as pd
import io
import qrcode
import sqlalchemy
import json
from datetime import datetime
from typing import List, Optional


class Guest(rx.Model, table=True):
    name: str
    guest_id: str
    status: str = "Absent"
    # Add a field to store all data as JSON
    full_data: str = ""  # Will store JSON string of all columns


class State(rx.State):
    """Central State for Empire Signature."""
    # Data
    guest_data: List[dict] = []
    columns: List[str] = []  # Will be dynamically set from Excel

    # File upload
    uploaded_filename: str = ""

    # Dialog control
    qr_dialog_open: bool = False

    # Inputs
    username: str = ""
    password: str = ""
    error_message: str = ""
    search_query: str = ""
    search_name: str = ""
    search_id: str = ""

    @rx.event(background=True)
    async def auto_refresh(self):
        """Background auto refresh for dashboard."""
        while True:
            await asyncio.sleep(3)

            with rx.session() as session:
                guests = session.exec(Guest.select()).all()

            # 🔥 MUST use async with self before modifying state
            async with self:
                if guests:
                    first_guest = json.loads(guests[0].full_data)
                    self.columns = list(first_guest.keys())

                    updated_data = []
                    for g in guests:
                        guest_dict = json.loads(g.full_data)
                        guest_dict["Status"] = g.status
                        updated_data.append(guest_dict)

                    self.guest_data = updated_data
                else:
                    self.columns = []
                    self.guest_data = []

    async def splash_logic(self):
        await asyncio.sleep(2)
        return rx.redirect("/home")

    # --- Explicit Setters (to fix deprecation warnings) ---
    def set_username(self, value: str):
        self.username = value

    def set_password(self, value: str):
        self.password = value

    def set_search_query(self, value: str):
        self.search_query = value

    def set_search_name(self, value: str):
        self.search_name = value

    def set_search_id(self, value: str):
        self.search_id = value

    def set_uploaded_filename(self, files: List[rx.UploadFile]):
        """Set the filename when a file is selected."""
        if files and len(files) > 0:
            self.uploaded_filename = files[0].name
        return rx.toast.info(f"Selected: {self.uploaded_filename}")

    def show_qr_dialog(self):
        """Open the QR code dialog."""
        self.qr_dialog_open = True

    def close_qr_dialog(self):
        """Close the QR code dialog."""
        self.qr_dialog_open = False

    def download_qr(self):
        """Download the QR code as PNG."""
        # Generate QR code with timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"empire_qr_{timestamp}.png"

        # Get the QR code image data
        img_data = self.qr_code_image.replace("data:image/png;base64,", "")

        return rx.download(
            data=f"data:image/png;base64,{img_data}",
            filename=filename
        )

    def clear_checkin_fields(self):
        """Clear the check-in input fields."""
        self.search_name = ""
        self.search_id = ""
        return rx.toast.info("Fields cleared")

    @rx.var
    def get_base_url(self) -> str:
        if os.environ.get("REFLEX_CLOUD") or os.environ.get("PRODUCTION"):
            return "https://your-app-name.reflex.run/check-in"
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
        return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={self.get_base_url}/checkin"

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
    def filtered_data(self) -> List[dict]:
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
        self.uploaded_filename = ""
        return rx.toast.success("Database and UI cleared.")

    async def handle_upload(self, files: List[rx.UploadFile]):
        for file in files:
            self.uploaded_filename = file.filename
            upload_data = await file.read()

            # Try different Excel engines
            try:
                df = pd.read_excel(io.BytesIO(upload_data), engine='openpyxl')
            except:
                try:
                    df = pd.read_excel(io.BytesIO(upload_data), engine='xlrd')
                except:
                    try:
                        df = pd.read_csv(io.BytesIO(upload_data))
                    except:
                        df = pd.read_excel(io.BytesIO(upload_data))

            # Clean column names - strip whitespace
            df.columns = df.columns.str.strip()

            # Store all original columns
            self.columns = df.columns.tolist()

            # Ensure Status column exists
            if "Status" not in df.columns:
                df["Status"] = "Absent"
                if "Status" not in self.columns:
                    self.columns.append("Status")

            # Fill NaN values
            df = df.fillna("")

            # Convert to records
            self.guest_data = df.to_dict("records")

            # SAVE TO DATABASE - Store all columns as JSON
            with rx.session() as session:
                # Clear existing data
                session.execute(sqlalchemy.delete(Guest))

                for _, row in df.iterrows():
                    # Get name and ID from appropriate columns (case insensitive)
                    name = ""
                    guest_id = ""

                    # Try to find name column
                    for col in df.columns:
                        if col.lower() in ['name', 'full name', 'guest name', 'names', 'fullname']:
                            name = str(row[col])
                            break

                    # Try to find ID column
                    for col in df.columns:
                        if col.lower() in ['id', 'guest id', 'guest_id', 'code', 'identification', 'guestid']:
                            guest_id = str(row[col])
                            break

                    # Store all data as JSON
                    full_data = json.dumps(row.to_dict())

                    guest = Guest(
                        name=name,
                        guest_id=guest_id,
                        status=str(row.get("Status", "Absent")),
                        full_data=full_data
                    )
                    session.add(guest)
                session.commit()

        return rx.toast.success(f"Uploaded {len(df)} guests with {len(self.columns)} columns!")

    def load_guests(self):
        """Pull latest guests from database."""
        with rx.session() as session:
            guests = session.exec(Guest.select()).all()

            if guests:
                first_guest = json.loads(guests[0].full_data)
                self.columns = list(first_guest.keys())

                updated_data = []
                for g in guests:
                    guest_dict = json.loads(g.full_data)
                    guest_dict["Status"] = g.status
                    updated_data.append(guest_dict)

                self.guest_data = updated_data
            else:
                self.guest_data = []
                self.columns = []

    def check_in_guest(self):
        n_in = self.search_name.strip()
        i_in = self.search_id.strip()

        if not n_in and not i_in:
            return rx.toast.error("Please enter a name or ID.")

        with rx.session() as session:
            query = Guest.select()

            if n_in:
                query = query.where(Guest.name.ilike(f"%{n_in}%"))

            if i_in:
                query = query.where(Guest.guest_id == i_in)

            guest = session.exec(query).first()

            if not guest:
                return rx.toast.error("Guest not found.")

            guest.status = "Present"
            session.add(guest)
            session.commit()

            guest_name = guest.name

        # Clear inputs
        self.search_name = ""
        self.search_id = ""

        # Reload data for THIS session
        self.load_guests()

        return rx.toast.success(
            f"✅ Welcome, {guest_name}!",
            duration=4000
        )

    def login(self):
        if self.username == "admin" and self.password == "password":
            return rx.redirect("/dashboard")
        self.error_message = "Invalid Credentials"