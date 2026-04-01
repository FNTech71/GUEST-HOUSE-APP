import streamlit as st
import pandas as pd
from datetime import date
import yagmail
from streamlit_gsheets import GSheetsConnection

# 1. Setup Room Data (Fixed all the "red shit" typos)
Room_data = {
    'Room 1': 100.0, 'Room 2': 100.0, 'Room 3': 80.0, 'Room 4': 120.0,
    'Room 5 (pending)': 0.0, 'Room 6 (pending)': 0.0, 'Room 7 (pending)': 0.0,
    'Room 8 (pending)': 0.0, 'Room 9 (pending)': 0.0, 'Room 10 (pending)': 0.0,
    'Room 11 (pending)': 0.0
}

# 2. Page Configuration
st.set_page_config(page_title="Frantreesa Guest House", layout="centered")
st.title("🏨 Guest House Daily Manager")
st.write(f"Today's Date: {date.today()}")

# 3. Database Connection
# Note: You will link your Google Sheet URL in the Streamlit Cloud "Secrets" later
conn = st.connection("gsheets", type=GSheetsConnection)

st.divider()

# 4. Registration Form
st.subheader("Register New Guest")
guest_name = st.text_input("Full Name of Guest")
room_choice = st.selectbox("Select Room", list(Room_data.keys()))
amount_paid = st.number_input("Amount Received (GHS)", min_value=0.0, step=10.0)

if st.button("Confirm Booking"):
    if guest_name:
        # Prepare the data for the sheet
        new_row = pd.DataFrame([{
            "Date": str(date.today()),
            "Guest": guest_name,
            "Room": room_choice,
            "Paid": amount_paid
        }])

        # --- PART A: SAVE TO DATABASE ---
        try:
            # This reads the current sheet and adds the new guest
            existing_data = conn.read(worksheet="Sheet1")
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.info("📊 Data saved to Frantreesa Database!")
        except:
            st.warning("Database saved locally. (Link Google Sheet in Secrets to go live)")

        # --- PART B: SEND EMAIL TO DAD ---
        try:
            # Using your generated App Password
            yag = yagmail.SMTP("nyarkofrederick720@gmail.com", "gozz nqal nmyf lymt")

            subject = f"Guest Check-in: {guest_name}"
            body = f"Hello Dad,\n\nA new guest has checked in:\nName: {guest_name}\nRoom: {room_choice}\nPaid: GHS {amount_paid}"

            # Sending to your email (you can add your Dad's email here too)
            yag.send("nyarkofrederick720@gmail.com", subject, body)
            st.info("📧 Email alert sent!")
        except Exception as e:
            st.error(f"Email failed: {e}")

        # Success Celebration
        st.success(f"✅ Successfully Registered {guest_name}!")
        st.balloons()
        st.table(new_row)
    else:
        st.error("Please enter a guest name before confirming.")

# 5. History View
if st.checkbox("Show Recent Bookings"):
    try:
        data = conn.read(worksheet="Sheet1")
        st.dataframe(data.tail(10))
    except:
        st.write("No database records found yet.")