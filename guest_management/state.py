# import reflex as rx
# import pandas as pd
# import io
# import json
# import sqlalchemy
# from datetime import datetime
# from typing import List
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
# import os
# # ======================
# # DATABASE MODEL
# # ======================
#
# class Guest(rx.Model, table=True):
#     __tablename__ = "guest"
#
#     name: str
#     guest_id: str
#     status: str = "Absent"
#     full_data: str
#
#
#
# # ======================
# # APP STATE (PRODUCTION CLEAN)
# # ======================
#
# class State(rx.State):
#
#     # --------------------
#     # UI STATE
#     # --------------------
#     uploaded_filename: str = ""
#     search_query: str = ""
#     search_name: str = ""
#     search_id: str = ""
#     username: str = ""
#     password: str = ""
#     error_message: str = ""
#     qr_dialog_open: bool = False
#     guest_data: List[dict] = []
#     filtered_data: List[dict] = []
#     columns: List[str] = []
#
#     # qr_url: str = "/checkin"
#
#     def splash_logic(self):
#         return rx.redirect("/home")
#     # --------------------
#     # AUTH
#     # --------------------
#     def set_username(self, value: str):
#         self.username = value
#
#     def set_password(self, value: str):
#         self.password = value
#
#     def login(self):
#         if self.username == "admin" and self.password == "password":
#             return rx.redirect("/dashboard")
#         self.error_message = "Invalid Credentials"
#
#     def set_search_name(self, value: str):
#         self.search_name = value
#
#     def set_search_id(self, value: str):
#         self.search_id = value
#
#     def clear_checkin_fields(self):
#         self.search_name = ""
#         self.search_id = ""
#     # --------------------
#     # FILE NAME DISPLAY
#     # --------------------
#     def set_uploaded_filename(self, files):
#         if files:
#             self.uploaded_filename = files[0].name
#
#     # --------------------
#     # QR DIALOG
#     # --------------------
#     def show_qr_dialog(self):
#         self.qr_dialog_open = True
#
#     def close_qr_dialog(self):
#         self.qr_dialog_open = False
#
#     # --------------------
#     # QR URL
#     # --------------------
#     @rx.var
#     def qr_url(self) -> str:
#         return "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https://guest-management-blue-sun.reflex.run/checkin"
#
#     # --------------------
#     # EXCEL UPLOAD
#     # --------------------
#     async def handle_upload(self, files: List[rx.UploadFile]):
#
#         if not files:
#             return rx.toast.error("No file selected.")
#
#         file = files[0]
#         self.uploaded_filename = file.filename
#
#         file_bytes = await file.read()
#
#         try:
#             df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
#         except:
#             try:
#                 df = pd.read_excel(io.BytesIO(file_bytes), engine="xlrd")
#             except:
#                 df = pd.read_csv(io.BytesIO(file_bytes))
#
#
#         # Add Status column if missing
#         if "Status" not in df.columns:
#             df["Status"] = "Absent"
#
#         self.columns = df.columns.tolist()
#         self.guest_data = df.to_dict("records")
#         self.filtered_data = self.guest_data
#
#         # Save to database
#         with rx.session() as session:
#
#             session.execute(sqlalchemy.delete(Guest))
#
#             for _, row in df.iterrows():
#
#                 row_dict = row.to_dict()
#
#                 # Try auto detect name
#                 name = ""
#                 for col in df.columns:
#                     if col.lower() in ["name", "full name", "guest name"]:
#                         name = str(row[col])
#                         break
#
#                 # Try auto detect id
#                 guest_id = ""
#                 for col in df.columns:
#                     if col.lower() in ["id", "guest id", "guest_id", "code"]:
#                         guest_id = str(row[col])
#                         break
#
#                 guest = Guest(
#                     name=name,
#                     guest_id=guest_id,
#                     status=row_dict.get("Status", "Absent"),
#                     full_data=json.dumps(row_dict)
#                 )
#
#                 session.add(guest)
#
#             session.commit()
#
#         return rx.toast.success(f"Uploaded {len(df)} guests successfully.")
#
#     # --------------------
#     # CLEAR TABLE
#     # --------------------
#     def clear_table(self):
#         with rx.session() as session:
#             session.execute(sqlalchemy.delete(Guest))
#             session.commit()
#
#         self.guest_data = []
#         self.filtered_data = []
#         self.columns = []
#         self.uploaded_filename = ""
#
#         return rx.toast.success("Database cleared.")
#
#     # --------------------
#     # CHECK-IN (ATOMIC SAFE)
#     # --------------------
#     def check_in_guest(self):
#
#         name_input = self.search_name.strip()
#         id_input = self.search_id.strip()
#
#         if not name_input and not id_input:
#             return rx.toast.error("Enter Name or ID.")
#
#         with rx.session() as session:
#
#             query = Guest.select()
#
#             if name_input:
#                 query = query.where(Guest.name.ilike(f"%{name_input}%"))
#
#             if id_input:
#                 query = query.where(Guest.guest_id == id_input)
#
#             guest = session.exec(query).first()
#
#             if not guest:
#                 return rx.toast.error("Guest not found.")
#
#             guest.status = "Present"
#             session.add(guest)
#             session.commit()
#
#             guest_name = guest.name
#
#         self.clear_checkin_fields()
#         self.load_guests()
#
#         return rx.redirect("/success")
#
#     # --------------------
#     # DYNAMIC TABLE DATA
#     # --------------------
#
#     # def guest_data(self) -> List[dict]:
#     #     with rx.session() as session:
#     #         guests = session.exec(select(Guest)).all()
#     #
#     #     rows = []
#     #
#     #     for g in guests:
#     #         row = json.loads(g.full_data)
#     #         row["Status"] = g.status
#     #         rows.append(row)
#     #
#     #     return rows
#
#     def load_guests(self):
#
#         with rx.session() as session:
#             guests = session.exec(Guest.select()).all()
#
#         if not guests:
#             self.guest_data = []
#             self.filtered_data = []
#             self.columns = []
#             return
#
#         updated_data = []
#
#         for g in guests:
#             row = json.loads(g.full_data)
#             row["Status"] = g.status
#             updated_data.append(row)
#
#         self.guest_data = updated_data
#         self.filtered_data = updated_data
#         self.columns = list(updated_data[0].keys())
#
#     # ---------------- SEARCH ----------------
#
#     def set_search_query(self, value: str):
#         self.search_query = value
#
#         if not value:
#             self.filtered_data = self.guest_data
#         else:
#             term = value.lower()
#             self.filtered_data = [
#                 g for g in self.guest_data
#                 if any(term in str(v).lower() for v in g.values())
#             ]
#
#     def columns(self) -> List[str]:
#         if not self.guest_data:
#             return []
#         return list(self.guest_data[0].keys())
#
#
#     # def filtered_data(self) -> List[dict]:
#     #     if not self.search_query:
#     #         return self.guest_data
#     #
#     #     term = self.search_query.lower()
#     #     return [
#     #         row for row in self.guest_data
#     #         if any(term in str(v).lower() for v in row.values())
#     #     ]
#
#     # --------------------
#     # LIVE COUNTS (DB SAFE)
#     # --------------------
#     @rx.var
#     def total_count(self) -> int:
#         return len(self.guest_data)
#
#     @rx.var
#     def present_count(self) -> int:
#         return len([g for g in self.guest_data if g["Status"] == "Present"])
#
#     @rx.var
#     def absent_count(self) -> int:
#         return len([g for g in self.guest_data if g["Status"] == "Absent"])
import reflex as rx
import pandas as pd
import io
import json
import sqlalchemy
from typing import List
import asyncio


# ---------------- DATABASE MODEL ----------------

class Guest(rx.Model, table=True):
    name: str
    guest_id: str
    status: str = "Absent"
    full_data: str = ""


# ---------------- STATE ----------------

class State(rx.State):

    # Base variables
    guest_data: List[dict] = []
    filtered_data: List[dict] = []
    columns: List[str] = []

    uploaded_filename: str = ""
    qr_dialog_open: bool = False

    username: str = ""
    password: str = ""
    error_message: str = ""

    search_query: str = ""
    search_name: str = ""
    search_id: str = ""

    # ---------------- COMPUTED COUNTS ----------------

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
    def qr_url(self) -> str:
        return "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=https://guest-management-blue-sun.reflex.run/checkin"

    # ---------------- SPLASH ----------------

    async def splash_logic(self):
        await asyncio.sleep(2)
        return rx.redirect("/home")

    # ---------------- SETTERS ----------------

    def set_username(self, value: str):
        self.username = value

    def set_password(self, value: str):
        self.password = value

    def set_search_query(self, value: str):
        self.search_query = value

        if not value:
            self.filtered_data = self.guest_data
        else:
            term = value.lower()
            self.filtered_data = [
                g for g in self.guest_data
                if any(term in str(v).lower() for v in g.values())
            ]

    def set_search_name(self, value: str):
        self.search_name = value

    def set_search_id(self, value: str):
        self.search_id = value

    # ---------------- QR ----------------

    def show_qr_dialog(self):
        self.qr_dialog_open = True

    def close_qr_dialog(self):
        self.qr_dialog_open = False

    # ---------------- CLEAR TABLE ----------------

    def clear_table(self):
        with rx.session() as session:
            session.execute(sqlalchemy.delete(Guest))
            session.commit()

        self.guest_data = []
        self.filtered_data = []
        self.columns = []
        self.uploaded_filename = ""

        return rx.toast.success("Database cleared.")

    # ---------------- UPLOAD ----------------

    async def handle_upload(self, files: List[rx.UploadFile]):

        if not files:
            return rx.toast.error("No file selected.")

        file = files[0]
        self.uploaded_filename = file.filename

        content = await file.read()

        try:
            df = pd.read_excel(io.BytesIO(content))
        except:
            df = pd.read_csv(io.BytesIO(content))

        df.columns = df.columns.str.strip()
        df.fillna("", inplace=True)

        if "Status" not in df.columns:
            df["Status"] = "Absent"

        self.columns = df.columns.tolist()
        self.guest_data = df.to_dict("records")
        self.filtered_data = self.guest_data

        with rx.session() as session:

            session.execute(sqlalchemy.delete(Guest))

            for _, row in df.iterrows():
                row_dict = row.to_dict()

                name = ""
                guest_id = ""

                for col in df.columns:
                    if col.lower() in ["name", "full name", "guest name"]:
                        name = str(row[col])
                    if col.lower() in ["id", "guest id", "guest_id", "code"]:
                        guest_id = str(row[col])

                guest = Guest(
                    name=name,
                    guest_id=guest_id,
                    status=row_dict.get("Status", "Absent"),
                    full_data=json.dumps(row_dict)
                )

                session.add(guest)

            session.commit()

        return rx.toast.success(f"Uploaded {len(df)} guests successfully.")

    # ---------------- LOAD ----------------

    def load_guests(self):

        with rx.session() as session:
            guests = session.exec(Guest.select()).all()

        if not guests:
            self.guest_data = []
            self.filtered_data = []
            self.columns = []
            return

        updated = []

        for g in guests:
            row = json.loads(g.full_data)
            row["Status"] = g.status
            updated.append(row)

        self.guest_data = updated
        self.filtered_data = updated
        self.columns = list(updated[0].keys())

    # ---------------- CHECK-IN ----------------

    def clear_checkin_fields(self):
        self.search_name = ""
        self.search_id = ""

    def check_in_guest(self):

        name_input = self.search_name.strip()
        id_input = self.search_id.strip()

        if not name_input and not id_input:
            return rx.toast.error("Enter Name or ID.")

        with rx.session() as session:

            guest = None

            if name_input:
                guest = session.exec(
                    Guest.select().where(Guest.name == name_input)
                ).first()

            if not guest and id_input:
                guest = session.exec(
                    Guest.select().where(Guest.guest_id == id_input)
                ).first()

            if not guest:
                return rx.toast.error("Guest not found.")

            if guest.status == "Present":
                return rx.redirect("/already")

            guest.status = "Present"
            session.add(guest)
            session.commit()

        self.load_guests()
        self.search_name = ""
        self.search_id = ""

        return rx.redirect("/success")

    # ---------------- LOGIN ----------------

    def login(self):
        if self.username == "admin" and self.password == "password":
            return rx.redirect("/dashboard")

        self.error_message = "Invalid Credentials"

    async def success_redirect(self):
        await asyncio.sleep(3)
        return rx.redirect("/")

    def refresh_dashboard(self):
        self.load_guests()

