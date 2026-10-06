python
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="Hospital Queue Management System",
    page_icon="🏥",
    layout="wide"
)

# ---------------- DATABASE ----------------

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    token = Column(Integer)
    name = Column(String)
    phone = Column(String)
    doctor = Column(String)


engine = create_engine("sqlite:///hospital.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
db = Session()

# ---------------- SESSION DATA ----------------

if "patients" not in st.session_state:
    st.session_state.patients = []

# ---------------- SIDEBAR ----------------

st.sidebar.title("🏥 Hospital Menu")

menu = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Home",
        "👤 Patient Registration",
        "🩺 Doctor Dashboard",
        "📊 Admin Dashboard"
    ]
)

# ---------------- HOME ----------------

if menu == "🏠 Home":

    st.title("🏥 Hospital Queue Management System")

    st.subheader("Welcome to Our Hospital")

    st.write(
        "This system helps manage patients, doctors, "
        "tokens and waiting queues efficiently."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "👤 Patient Registration\n\n"
            "Register patients and generate tokens."
        )

    with col2:
        st.success(
            "🩺 Doctor Dashboard\n\n"
            "Manage the current patient queue."
        )

    with col3:
        st.warning(
            "📊 Admin Dashboard\n\n"
            "Monitor waiting patients."
        )

    st.divider()

    st.info("👈 Select an option from the menu.")

# ---------------- PATIENT REGISTRATION ----------------

elif menu == "👤 Patient Registration":

    st.title("👤 Patient Registration")

    st.subheader("Register Patient and Get Token 🎫")

    patient_name = st.text_input(
        "Patient Name"
    )

    phone = st.text_input(
        "Phone Number"
    )

    doctor = st.selectbox(
        "Select Doctor",
        [
            "Dr. Priya - General Physician",
            "Dr. Ravi - Cardiologist",
            "Dr. Anitha - Pediatrician"
        ]
    )

    if st.button("🎫 Get Token"):

        if patient_name.strip() and phone.strip():

            token = len(st.session_state.patients) + 1

            new_patient = Patient(
                token=token,
                name=patient_name,
                phone=phone,
                doctor=doctor
            )

            db.add(new_patient)
            db.commit()

            st.session_state.patients.append(
                {
                    "Token": token,
                    "Patient Name": patient_name,
                    "Phone": phone,
                    "Doctor": doctor
                }
            )

            st.success(
                "✅ Patient Registered Successfully!"
            )

            st.success(
                f"🎫 Your Token Number is: {token}"
            )

        else:

            st.warning(
                "⚠️ Please enter Patient Name and Phone Number"
            )

# ---------------- DOCTOR DASHBOARD ----------------

elif menu == "🩺 Doctor Dashboard":

    st.title("🩺 Doctor Dashboard")

    if st.session_state.patients:

        current_patient = st.session_state.patients[0]

        st.subheader("🔔 Current Patient")

        st.write(
            f"🎫 Token Number: {current_patient['Token']}"
        )

        st.write(
            f"👤 Patient Name: {current_patient['Patient Name']}"
        )

        st.write(
            f"📱 Phone Number: {current_patient['Phone']}"
        )

        st.write(
            f"🩺 Doctor: {current_patient['Doctor']}"
        )

        if st.button("➡️ Call Next Patient"):

            st.session_state.patients.pop(0)

            st.success(
                "✅ Patient completed."
            )

            st.rerun()

    else:

        st.info(
            "No patients waiting."
        )

# ---------------- ADMIN DASHBOARD ----------------

elif menu == "📊 Admin Dashboard":

    st.title("📊 Admin Dashboard")

    total_patients = len(
        st.session_state.patients
    )

    st.metric(
        "👥 Waiting Patients",
        total_patients
    )

    if total_patients > 0:

        st.subheader("📋 Patient Details")

        for patient in st.session_state.patients:

            st.write(
                f"🎫 Token: {patient['Token']} | "
                f"👤 {patient['Patient Name']} | "
                f"📱 {patient['Phone']} | "
                f"🩺 {patient['Doctor']}"
            )

    else:

        st.info(
            "No patients registered."
        )

