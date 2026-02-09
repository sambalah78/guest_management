import reflex as rx
import asyncio
import pandas as pd
import io


class State(rx.State):
    """The app state."""
    username: str = ""
    password: str = ""
    error_message: str = ""
    guest_data: list[dict] = []
    columns: list[str] = []
    is_processing: bool = False

    # Missing variables for check_in.py
    search_name: str = ""
    search_query: str = ""
    search_id: str = ""
    deploy_url: str = "https://guest-management-blue-sun.reflex.run/check-in"

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
    def qr_code_url(self) -> str:
        # Generates a QR code pointing to the check-in page
        return f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={self.deploy_url}"

    @rx.var
    def filtered_guest_data(self) -> list[dict]:
        if not self.search_query:
            return self.guest_data
        term = self.search_query.lower()
        return [g for g in self.guest_data if any(term in str(v).lower() for v in g.values())]

    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            rx.window_alert("No file selected.")

        self.is_processing = True
        yield

        for file in files:
            upload_data = await file.read()
            # df = pd.read_excel(io.BytesIO(upload_data))
            #
            # if "Status" not in df.columns:
            #     df["Status"] = "Absent"
            #
            # df = df.fillna("")
            # self.columns = df.columns.tolist()
            # self.guest_data = [
            #     {str(k): str(v) for k, v in record.items()}
            #     for record in df.to_dict("records")
            # ]
            try:
                df = pd.read_excel(io.BytesIO(upload_data))
                if "Status" not in df.columns:
                    df["Status"] = "Absent"
                df = df.fillna("")
                self.columns = df.columns.tolist()
                self.guest_data = df.to_dict("records")
            except Exception as e:
                rx.window_alert(f"Error processing file: {str(e)}")
        self.is_processing = False

    def check_in_guest(self):
        """The most robust version of name/ID matching."""
        # 1. Clean the guest's input
        name_to_find = self.search_name.strip().lower()
        id_to_find = self.search_id.strip().lower()

        if not name_to_find and not id_to_find:
            return rx.window_alert("Please enter a Name or an ID.")

        found = False
        new_data = []

        # 2. DEBUG: This prints to your terminal/console to help you see column names
        print(f"DEBUG: Current Columns are: {self.columns}")

        # 3. Flexible column detection
        # We look for ANY column that sounds like 'Name' or 'ID'
        name_col = next((c for c in self.columns if c.lower() in ["name", "full name", "guest"]), None)
        id_col = next((c for c in self.columns if c.lower() in ["id", "guest id", "code", "no"]), None)

        for guest in self.guest_data:
            # Extract data from the row safely
            db_name = str(guest.get(name_col, "")).strip().lower() if name_col else ""
            db_id = str(guest.get(id_col, "")).strip().lower() if id_col else ""

            # Check for a match
            match_name = (name_to_find != "" and name_to_find == db_name)
            match_id = (id_to_find != "" and id_to_find == db_id)

            if match_name or match_id:
                guest["Status"] = "Present"
                found = True

            new_data.append(guest)

        self.guest_data = new_data

        if found:
            self.search_name = ""
            self.search_id = ""
            return rx.window_alert("Check-in Successful!")
        else:
            # If it fails, we show the guest exactly what the system detected
            return rx.window_alert(
                f"Failed. Found no match for '{name_to_find}' or '{id_to_find}' in columns {self.columns}")

    def login(self):
        if self.username == "admin" and self.password == "password":
            self.error_message = ""
            return rx.redirect("/dashboard")
        else:
            self.error_message = "Invalid username or password."

    async def splash_logic(self):
        await asyncio.sleep(2)
        return rx.redirect("/home")