import reflex as rx
import pandas as pd
import io
import sqlalchemy
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field
import asyncio


# ======================
# DATABASE MODEL
# ======================

class Guest(rx.Model, table=True):
    name: str
    email: Optional[str] = None
    guest_id: str = Field(index=True, unique=True)

    status: str = "Absent"
    checkin_time: Optional[str] = None
    entry_count: int = 0

    username: str = ""
    password: str = ""
    error_message: str = ""

    def set_username(self, value: str):
        self.username = value

    def set_password(self, value: str):
        self.password = value

    @rx.event
    def login(self):
        if self.username == "admin" and self.password == "password":
            return rx.redirect("/dashboard")
        self.error_message = "Invalid Credentials"
# ======================
# APP STATE
# ======================

class State(rx.State):

    # UI state
    search_id: str = ""
    checkin_success: bool = False
    search_query: str = ""
    uploaded_filename: str = ""

    # --------------------
    # EXPLICIT SETTERS
    # --------------------


    def set_search_id(self, value: str):
        self.search_id = value

    def set_search_query(self, value: str):
        self.search_query = value

    def set_uploaded_filename(self, files: List[rx.UploadFile]):
        if files:
            self.uploaded_filename = files[0].name

    # --------------------
    # CHECK-IN (ATOMIC SAFE)
    # --------------------

    @rx.event
    def check_in_guest(self):
        gid = self.search_id.strip()

        if not gid:
            return rx.toast.error("Invalid QR")

        with rx.session() as session:
            result = session.exec(
                sqlalchemy.update(Guest)
                .where(Guest.guest_id == gid)
                .where(Guest.status == "Absent")
                .values(
                    status="Present",
                    checkin_time=datetime.now().strftime("%H:%M:%S")
                )
            )

            session.commit()

            if result.rowcount == 0:
                return rx.toast.warning("Already checked in")

        self.search_id = ""
        self.checkin_success = True

    @rx.event
    def reset_checkin(self):
        self.checkin_success = False

    # --------------------
    # DASHBOARD DATA
    # --------------------

    @rx.var
    def total_count(self) -> int:
        with rx.session() as session:
            return session.exec(Guest.select()).count()

    @rx.var
    def present_count(self) -> int:
        with rx.session() as session:
            return session.exec(
                Guest.select().where(Guest.status == "Present")
            ).count()

    @rx.var
    def absent_count(self) -> int:
        return self.total_count - self.present_count

    @rx.var
    def guests(self) -> List[Guest]:
        with rx.session() as session:
            return session.exec(Guest.select()).all()

    # --------------------
    # UPLOAD EXCEL
    # --------------------

    async def handle_upload(self, files: List[rx.UploadFile]):
        for file in files:
            self.uploaded_filename = file.filename
            upload_data = await file.read()

            df = pd.read_excel(io.BytesIO(upload_data))
            df.columns = df.columns.str.strip()
            df = df.fillna("")

            with rx.session() as session:
                session.execute(sqlalchemy.delete(Guest))

                for _, row in df.iterrows():
                    guest = Guest(
                        name=str(row.get("Name", "")),
                        email=str(row.get("Email", "")),
                        guest_id=str(row.get("Guest ID", "")),
                        status="Absent"
                    )
                    session.add(guest)

                session.commit()

        return rx.toast.success(f"Uploaded {len(df)} guests")
