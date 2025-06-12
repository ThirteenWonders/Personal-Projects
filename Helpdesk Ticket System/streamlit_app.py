# streamlit_app.py
import streamlit as st
import json
import os
import hashlib
from datetime import datetime

# File paths
TICKETS_FILE = "tickets.json"
COUNTER_FILE = "counters.json"
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
    user = st.text_input("Enter your name", key="create_user")
    issue = st.text_area("Describe your issue", key="create_issue")
    if st.button("Submit Ticket", key="submit_ticket"):
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
            st.success(f"Hi {user}, we have received your support request and will respond shortly.")
            st.success(f"Your Ticket ID is {ticket_id}")

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
        ticket_id = st.text_input("Enter Ticket ID to update", key="update_ticket_id").strip().upper()
        submitted = st.form_submit_button("Find Ticket")
        if submitted:
            st.session_state.selected_ticket_id = ticket_id

    if st.session_state.selected_ticket_id:
        ticket = next((t for t in st.session_state.tickets if t["id"] == st.session_state.selected_ticket_id), None)
        if ticket:
            st.markdown(f"### Ticket: {ticket['id']}")
            new_status = st.selectbox("Select new status", ["Open", "In Progress", "Closed"], index=["Open", "In Progress", "Closed"].index(ticket["status"]), key="update_status")
            note_text = st.text_area("Add a note describing the update", key="update_note")

            if st.button("Update Ticket Status", key="submit_update_ticket"):
                ticket["status"] = new_status
                ticket["notes"].append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text": note_text
                })
                save_data()
                st.success("Ticket updated successfully.")
                st.session_state.selected_ticket_id = None
        else:
            st.error("Ticket not found.")
            st.session_state.selected_ticket_id = None

def search_by_user():
    name = st.text_input("Enter name to search for tickets", key="search_user")
    if name:
        found = False
        for ticket in st.session_state.tickets:
            if ticket["user"].lower() == name.lower():
                st.text(f"ID: {ticket['id']}, Issue: {ticket['issue']}, Status: {ticket['status']}")
                found = True
        if not found:
            st.info("No tickets found for that user.")

def filter_tickets():
    status = st.selectbox("Filter tickets by status", ["Open", "In Progress", "Closed"], key="filter_status")
    for ticket in st.session_state.tickets:
        if ticket["status"] == status:
            st.text(f"ID: {ticket['id']}, User: {ticket['user']}, Issue: {ticket['issue']}, Status: {ticket['status']}")


def delete_ticket(admin_username):
    view_tickets()
    ticket_id = st.text_input("Enter Ticket ID to delete", key="delete_ticket_id").strip().upper()
    for ticket in st.session_state.tickets:
        if ticket["id"] == ticket_id:
            if st.button("Confirm Delete", key="confirm_delete"):
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
            if st.button(f"Restore {ticket['id']}", key=f"restore_{ticket['id']}"):
                ticket.pop('deleted_by', None)
                ticket.pop('deleted_at', None)
                st.session_state.tickets.append(ticket)
                save_data()
                deleted.pop(i)
                with open(RECYCLE_BIN_FILE, "w") as f:
                    json.dump(deleted, f, indent=2)
                st.success("Ticket restored successfully.")
                st.experimental_rerun()

def show_instructions():
    st.title("📘 Instructions:")

    st.markdown("""
    ### 👤 For Users (Non-Admin)

    1. **Submit a Ticket**
       - Fill in the required information (name, issue category, description).
       - Click **Submit Ticket** to generate a unique Ticket ID.
       - Your ticket will be reviewed and updated by an administrator.

    ---

    ### 🔐 For Admins

    1. **Login**
       - Click the **Admin Login** button at the top right.
       - Enter your **admin username and password**.
       - Username: **admin1**
       - Password: **admin123**
       - Upon success, you’ll see additional admin options.

    2. **Admin Features**
       - **View Tickets**: See all submitted tickets with status and timestamps.
       - **Update Ticket**: Change the status of a ticket and add notes.
       - **Delete Ticket**: Move a ticket to the recycle bin with audit logging.
       - **Restore Ticket**: Recover deleted tickets from the recycle bin.
       - **Change Admin Password**: Update your own login credentials securely.

    ---

    ### 💡 Notes

    - All data is saved to `.json` files and will persist between sessions.
    - Passwords are stored securely using SHA-256 hashing.
    - Admin logins are tracked to ensure accountability for deletions.

    If you encounter any issues, please contact the system administrator @ nicholasang1@outlook.com.
        """)

def admin_menu(username):
    st.subheader(f"Welcome, {username}")
    option = st.selectbox(
        "Admin Actions",
        ["View All Tickets", "Update Ticket", "Delete a Ticket", "Restore Deleted Ticket"],
        key="admin_menu_select"
    )

    if option == "View All Tickets":
        view_tickets()

        # Add a divider and subheading
        st.markdown("---")
        st.subheader("🔍 Search & Filter")

        # Integrate search and filter
        search_by_user()
        filter_tickets()

    elif option == "Update Ticket":
        update_ticket()
    elif option == "Delete a Ticket":
        delete_ticket(username)
    elif option == "Restore Deleted Ticket":
        restore_deleted_ticket()

# App UI starts here
load_data()

col1, col2 = st.columns([6, 1])
with col1:
    st.title("\U0001F3AB Helpdesk Ticket System")
with col2:
    if "admin" in st.session_state:
        st.success(f"{st.session_state['admin']} logged in")
        if st.button("Logout", key="logout_button"):
            del st.session_state["admin"]
            st.success("Logged out successfully.")
    else:
        if st.button("Admin Login", key="login_button"):
            st.session_state["show_login"] = True

# Admin login form
if "admin" not in st.session_state:
    if st.session_state.get("show_login"):
        st.subheader("\U0001F512 Admin Login")
        if "login_attempts" not in st.session_state:
            st.session_state.login_attempts = 0
        if st.session_state.login_attempts >= 3:
            st.warning("Too many failed attempts. Please refresh the page.")
        else:
            username = st.text_input("Admin Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", key="login_submit"):
                admins = load_admins_hash()
                hashed = hash_password(password)
                if username in admins and admins[username] == hashed:
                    st.session_state["admin"] = username
                    st.session_state.login_attempts = 0
                    st.session_state.show_login = False
                    st.success(f"Welcome, {username}!")
                    st.experimental_rerun()
                else:
                    st.session_state.login_attempts += 1
                    st.error("Invalid username or password")


# Sidebar navigation
nav = st.sidebar.radio("Navigation", ["Home", "Instructions"], key="nav_select")

if nav == "Instructions":
    show_instructions()
elif nav == "Home":
    if "admin" in st.session_state:
        admin_menu(st.session_state["admin"])
    else:
        create_ticket()
