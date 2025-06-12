# streamlit_app.py
import streamlit as st
import json
import os
import hashlib
from datetime import datetime



# File paths
TICKETS_FILE = "tickets.json"
COUNTER_FILE =  "counters.json"
RECYCLE_BIN_FILE = "deleted_tickets.json"

# Global state
if "tickets" not in st.session_state:
    st.session_state.tickets = []
if "ticket_counter" not in st.session_state:
    st.session_state.ticket_counter = 1

# Load data

def load_data():
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'r') as f:
            st.session_state.tickets = json.load(f)
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            st.session_state.ticket_counter = int(f.read())

def load_deleted_tickets():
    if os.path.exists(RECYCLE_BIN_FILE):
        with open(RECYCLE_BIN_FILE, "r") as f:
            return json.load(f)
    return []

def save_deleted_ticket(ticket):
    deleted = load_deleted_tickets()
    deleted.append(ticket)
    with open(RECYCLE_BIN_FILE, "w") as f:
        json.dump(deleted, f, indent=2)

def save_data():
    with open(TICKETS_FILE, 'w') as f:
        json.dump(st.session_state.tickets, f, indent=2)
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(st.session_state.ticket_counter))

def load_admins_hash():
    return dict(st.secrets["admins"])

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_ticket():
    ticket_id = f"TICKET-{st.session_state.ticket_counter:03d}"
    user = st.text_input("Enter your name")
    issue = st.text_area("Describe your issue")
    if st.button("Submit Ticket"):
        if user and issue:
            ticket = {
                "id": ticket_id,
                "user": user,
                "issue": issue,
                "status": "Open",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "notes": []
            }
            st.session_state.tickets.append(ticket)
            st.session_state.ticket_counter += 1
            save_data()
            st.success(f"Hi {user}, we have received your support request and will respond shortly. Your Ticket ID is {ticket_id}")

def view_tickets():
    if not st.session_state.tickets:
        st.info("No tickets found.")
        return
    for ticket in st.session_state.tickets:
        with st.expander(f"{ticket['id']} | {ticket['status']} | {ticket['user']}"):
            st.text(f"Issue       : {ticket['issue']}")
            st.text(f"Created At  : {ticket.get('created_at', 'N/A')}")
            if ticket.get("notes"):
                for i, note in enumerate(ticket["notes"], 1):
                    st.text(f"Note {i}: [{note['timestamp']}] {note['text']}")
            else:
                st.text("Notes       : None")

def update_ticket():
    view_tickets()

    if "selected_ticket_id" not in st.session_state:
        st.session_state.selected_ticket_id = None

    with st.form("update_ticket_form"):
        ticket_id = st.text_input("Enter Ticket ID to update").strip().upper()
        submitted = st.form_submit_button("Find Ticket")
        if submitted:
            st.session_state.selected_ticket_id = ticket_id

    # Only run if we have a selected ticket to update
    if st.session_state.selected_ticket_id:
        # Find the ticket object
        ticket = next((t for t in st.session_state.tickets if t["id"] == st.session_state.selected_ticket_id), None)
        if ticket:
            st.markdown(f"### Ticket: {ticket['id']}")
            new_status = st.selectbox("Select new status", ["Open", "In Progress", "Closed"], index=["Open", "In Progress", "Closed"].index(ticket["status"]))
            note_text = st.text_area("Add a note describing the update")

            if st.button("Update Ticket Status"):
                ticket["status"] = new_status
                ticket["notes"].append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text": note_text
                })
                save_data()
                st.success("Ticket updated successfully.")
                st.session_state.selected_ticket_id = None  # Clear after update
        else:
            st.error("Ticket not found.")
            st.session_state.selected_ticket_id = None  # Clear invalid ID


def delete_ticket(admin_username):
    view_tickets()
    ticket_id = st.text_input("Enter Ticket ID to delete").strip().upper()
    for ticket in st.session_state.tickets:
        if ticket["id"] == ticket_id:
            if st.button("Confirm Delete"):
                deleted_entry = ticket.copy()
                deleted_entry['deleted_by'] = admin_username
                deleted_entry['deleted_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_deleted_ticket(deleted_entry)
                st.session_state.tickets.remove(ticket)
                save_data()
                st.success("Ticket deleted and moved to recycle bin.")
                return
    if ticket_id:
        st.error("Invalid Ticket ID.")

def restore_deleted_ticket():
    deleted = load_deleted_tickets()
    if not deleted:
        st.info("Recycle bin is empty.")
        return
    for i, ticket in enumerate(deleted):
        with st.expander(f"{ticket['id']} | Deleted by: {ticket.get('deleted_by', 'Unknown')}"):
            st.write(f"User: {ticket['user']} | Status: {ticket['status']} | Deleted at: {ticket['deleted_at']}")
            if st.button(f"Restore {ticket['id']}"):
                ticket.pop('deleted_by', None)
                ticket.pop('deleted_at', None)
                st.session_state.tickets.append(ticket)
                save_data()
                deleted.pop(i)
                with open(RECYCLE_BIN_FILE, "w") as f:
                    json.dump(deleted, f, indent=2)
                st.success("Ticket restored successfully.")
                st.experimental_rerun()

def search_by_user():
    name = st.text_input("Enter name to search for tickets")
    if name:
        found = False
        for ticket in st.session_state.tickets:
            if ticket["user"].lower() == name.lower():
                st.text(f"ID: {ticket['id']}, Issue: {ticket['issue']}, Status: {ticket['status']}")
                found = True
        if not found:
            st.info("No tickets found for that user.")

def filter_tickets():
    status = st.selectbox("Filter tickets by status", ["Open", "In Progress", "Closed"])
    for ticket in st.session_state.tickets:
        if ticket["status"] == status:
            st.text(f"ID: {ticket['id']}, User: {ticket['user']}, Issue: {ticket['issue']}, Status: {ticket['status']}")

def admin_menu(username):
    st.subheader(f"Welcome, {username}")
    admin_options = [
        "View All Tickets", "Update Ticket", "Filter by Status", "Search by User",
        "Delete a Ticket", "Restore Deleted Ticket"
    ]
    action = st.selectbox("Choose an admin action", admin_options)
    if action == "View All Tickets":
        view_tickets()
    elif action == "Update Ticket":
        update_ticket()
    elif action == "Filter by Status":
        filter_tickets()
    elif action == "Search by User":
        search_by_user()
    elif action == "Delete a Ticket":
        delete_ticket(username)
    elif action == "Restore Deleted Ticket":
        restore_deleted_ticket()


# UI
load_data()

# Top layout: App title (left) and admin login/logout (right)
col1, col2 = st.columns([6, 1])

with col1:
    st.title("🎫 Helpdesk Ticket System")

with col2:
    if "admin" in st.session_state:
        st.success(f"{st.session_state['admin']} logged in")
        if st.button("Logout"):
            del st.session_state["admin"]
            st.success("Logged out successfully.")
    else:
        if st.button("Admin Login"):
            st.session_state["show_login"] = True


if "admin" not in st.session_state:
    user_view()


# Admin login form logic
if st.session_state.get("show_login") and "admin" not in st.session_state:
    st.subheader("🔐 Admin Login")
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0

    if st.session_state.login_attempts >= 3:
        st.warning("Too many failed attempts. Please refresh the page to try again.")
    else:
        username = st.text_input("Admin Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            admins = load_admins_hash()
            hashed = hash_password(password)
            if username in admins and admins[username] == hashed:
                st.session_state["admin"] = username
                st.session_state.login_attempts = 0
                st.session_state.show_login = False
                st.success(f"Welcome, {username}!")
            else:
                st.session_state.login_attempts += 1
                attempts_left = 3 - st.session_state.login_attempts
                st.error(f"Invalid username or password. {attempts_left} attempts left.")


if "admin" in st.session_state:
    admin_menu(st.session_state["admin"])
