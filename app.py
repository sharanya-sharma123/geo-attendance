import streamlit as st
import pandas as pd
import plotly.express as px

from database import initialize_database, get_connection
from qr_utils import generate_qr
from streamlit_geolocation import streamlit_geolocation
from location_utils import calculate_distance

from datetime import date, time
import uuid


# =========================================================
# DATABASE
# =========================================================

initialize_database()


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Geo Attendance System",
    page_icon="📍",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .main {
        padding-top: 1.5rem;
    }

    body {
        font-family: "Segoe UI", sans-serif;
    }

    /* ---------- HERO ---------- */

.hero {
    padding: 38px 45px;
    border-radius: 14px;
    margin: 10px auto 38px auto;

    background: #132A43;

    border: 1px solid #294968;

    text-align: center;

    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.18);
}

.hero-title {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 48px;
    font-weight: 700;
    letter-spacing: -0.8px;
    color: #F8FAFC;

    margin-bottom: 12px;
}

.hero-subtitle {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 20px;
    font-weight: 400;
    color: #C7D4E2;

    letter-spacing: 0.1px;
}

    /* ---------- SECTION HEADINGS ---------- */

    .section-title {
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 30px;
    font-weight: 700;

    color: #F1F5F9;

    margin-top: 30px;
    margin-bottom: 20px;
}

    /* ---------- INFORMATION CARDS ---------- */

    .info-card {
        padding: 20px 22px;
        border-radius: 14px;

        border: 1px solid rgba(148,163,184,0.18);

        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.75),
                rgba(15,23,42,0.75)
            );

        margin-bottom: 15px;

        box-shadow:
            0 4px 18px rgba(0,0,0,0.12);
    }

    .info-label {
        font-size: 12px;
        font-weight: 650;
        letter-spacing: 1px;
        opacity: 0.55;
    }

    .info-value {
        font-size: 19px;
        font-weight: 650;
        margin-top: 6px;
    }

    /* ---------- DASHBOARD CARDS ---------- */

    .dashboard-card {
        padding: 24px;

        border-radius: 16px;

        border: 1px solid rgba(148,163,184,0.18);

        background:
            linear-gradient(
                145deg,
                rgba(30,41,59,0.8),
                rgba(15,23,42,0.8)
            );

        min-height: 130px;

        box-shadow:
            0 5px 20px rgba(0,0,0,0.15);
    }

    .card-icon {
        font-size: 25px;
    }

    .card-title {
        font-size: 12px;
        font-weight: 650;
        letter-spacing: 1px;
        opacity: 0.55;
        margin-top: 10px;
    }

    .card-value {
        font-size: 35px;
        font-weight: 750;
        margin-top: 4px;
    }

    /* ---------- SUCCESS CARD ---------- */

    .success-card {
        padding: 24px;

        border-radius: 16px;

        border: 1px solid rgba(34,197,94,0.25);

        background: rgba(34,197,94,0.07);

        text-align: center;

        margin-top: 18px;

        box-shadow:
            0 5px 20px rgba(0,0,0,0.10);
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 650;

        min-height: 45px;

        border: 1px solid rgba(59,130,246,0.35);

        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 6px 18px rgba(37,99,235,0.22);
    }

    /* ---------- INPUT BOXES ---------- */

    input,
    textarea,
    [data-baseweb="select"] > div {
        border-radius: 9px !important;
    }

    /* ---------- DIVIDERS ---------- */

    hr {
        border-color: rgba(148,163,184,0.15);
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;

        opacity: 0.45;

        margin-top: 50px;

        padding: 22px;

        font-size: 12px;

        letter-spacing: 0.3px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Geo Attendance</div>
<div class="hero-subtitle">
    QR-Based Geo-Tagged Attendance Management System
</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# GET EVENT FROM QR
# =========================================================

event_token = st.query_params.get("event")

event = None

if event_token:

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM events WHERE qr_token = ?",
        (event_token,)
    )

    event = cursor.fetchone()

    connection.close()

    if not event:
        st.error("❌ Invalid or expired event QR code.")
        st.stop()


# =========================================================
# STUDENT ATTENDANCE PAGE
# =========================================================

if event_token and event:

    st.markdown(
        '<div class="section-title">👨‍🎓 Mark Attendance</div>',
        unsafe_allow_html=True
    )

    # Event information
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">EVENT</div>
                <div class="info-value">{event[1]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">DATE</div>
                <div class="info-value">📅 {event[2]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">GEO-FENCE</div>
                <div class="info-value">📍 {event[6]} meters</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Student Information")

    col1, col2 = st.columns(2)

    with col1:
        student_id = st.text_input(
            "Student ID",
            placeholder="Example: DS001"
        )

    with col2:
        student_name = st.text_input(
            "Student Name",
            placeholder="Example: Ananya Sharma"
        )

    st.markdown("### Location Verification")

    location = streamlit_geolocation()

    if location and location.get("latitude") is not None and location.get("longitude") is not None:

        student_lat = location["latitude"]
        student_lon = location["longitude"]

        st.success("📍 Your location has been detected.")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Latitude",
                f"{student_lat:.6f}"
            )

        with col2:
            st.metric(
                "Longitude",
                f"{student_lon:.6f}"
            )

        if st.button(
            "✅ Verify & Mark Attendance",
            use_container_width=True
        ):

            if not student_id or not student_name:

                st.warning(
                    "⚠️ Please enter both Student ID and Student Name."
                )

            else:

                distance = calculate_distance(
                    student_lat,
                    student_lon,
                    event[4],
                    event[5]
                )

                st.metric(
                    "📏 Distance From Event",
                    f"{distance:.2f} m"
                )

                if distance <= event[6]:

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        SELECT attendance_id
                        FROM attendance
                        WHERE event_id = ? AND user_id = ?
                        """,
                        (event[0], student_id)
                    )

                    existing_attendance = cursor.fetchone()

                    if existing_attendance:

                        connection.close()

                        st.warning(
                            "⚠️ Attendance has already been marked for this event."
                        )

                    else:

                        cursor.execute(
                            """
                            INSERT OR IGNORE INTO users (user_id, name)
                            VALUES (?, ?)
                            """,
                            (student_id, student_name)
                        )

                        cursor.execute(
                            """
                            INSERT INTO attendance
                            (
                                event_id,
                                user_id,
                                timestamp,
                                latitude,
                                longitude,
                                distance,
                                status
                            )
                            VALUES (?, ?, datetime('now'), ?, ?, ?, ?)
                            """,
                            (
                                event[0],
                                student_id,
                                student_lat,
                                student_lon,
                                distance,
                                "Present"
                            )
                        )

                        connection.commit()
                        connection.close()

                        if distance >= event[6] * 0.8:

                            st.warning(
                                "⚠️ Attendance marked near the geo-fence boundary."
                            )

                        st.markdown(
                            """
                            <div class="success-card">
                                <h2>🎉 Attendance Marked Successfully!</h2>
                                <p>Your attendance has been recorded.</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                else:

                    st.error(
                        "❌ You are outside the allowed attendance area."
                    )

    else:

        st.info(
            "📍 Please allow location access to continue."
        )


# =========================================================
# ADMIN PAGE
# =========================================================

if not event_token:

    # -----------------------------------------------------
    # CREATE EVENT
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">➕ Create New Event</div>',
        unsafe_allow_html=True
    )

    with st.form("event_form"):

        col1, col2 = st.columns(2)

        with col1:

            event_name = st.text_input(
                "Event Name",
                placeholder="Example: Python Workshop"
            )

        with col2:

            event_date = st.date_input(
                "Event Date",
                value=date.today()
            )

        col1, col2 = st.columns(2)

        with col1:

            start_time = st.time_input(
                "Start Time",
                value=time(10, 0)
            )

        with col2:

            allowed_radius = st.number_input(
                "Allowed Radius (meters)",
                min_value=10.0,
                max_value=1000.0,
                value=100.0,
                step=10.0
            )

        st.markdown("### 📍 Event Location")

        col1, col2 = st.columns(2)

        with col1:

            latitude = st.number_input(
                "Event Latitude",
                format="%.6f",
                help="Enter the latitude of the event location."
            )

        with col2:

            longitude = st.number_input(
                "Event Longitude",
                format="%.6f",
                help="Enter the longitude of the event location."
            )

        submit = st.form_submit_button(
            "🚀 Create Event",
            use_container_width=True
        )


    # -----------------------------------------------------
    # SAVE EVENT
    # -----------------------------------------------------

    if submit:

        if not event_name:

            st.error("❌ Please enter an event name.")

        else:

            qr_token = str(uuid.uuid4())

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO events
                (
                    event_name,
                    event_date,
                    start_time,
                    latitude,
                    longitude,
                    allowed_radius,
                    qr_token
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_name,
                    str(event_date),
                    str(start_time),
                    latitude,
                    longitude,
                    allowed_radius,
                    qr_token
                )
            )

            connection.commit()
            connection.close()

            st.success(
                "🎉 Event created successfully!"
            )

            st.markdown("### 📱 Event QR Code")

            qr_data = f"https://sharanya-sharma123-geo-attendance-app-klqlxy.streamlit.app/?event={qr_token}"

            qr_image = generate_qr(qr_data)

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:

                st.image(
                    qr_image,
                    width=300
                )

            st.info(
                "📱 Attendees can scan this QR code to mark their attendance."
            )

    # -----------------------------------------------------
# EXISTING EVENT QR CODES
# -----------------------------------------------------

st.markdown(
    '<div class="section-title">📱 Event QR Codes</div>',
    unsafe_allow_html=True
)

connection = get_connection()

events_df = pd.read_sql_query(
    """
    SELECT
        event_id,
        event_name,
        event_date,
        start_time,
        allowed_radius,
        qr_token
    FROM events
    ORDER BY event_id DESC
    """,
    connection
)

connection.close()

if events_df.empty:

    st.info("📭 No events created yet.")

else:

    for _, event_row in events_df.iterrows():

        with st.container(border=True):

            col1, col2 = st.columns([2, 1])

            with col1:

                st.markdown(f"### 🎟️ {event_row['event_name']}")

                st.write(
                    f"📅 **Date:** {event_row['event_date']}"
                )

                st.write(
                    f"🕐 **Start Time:** {event_row['start_time']}"
                )

                st.write(
                    f"📍 **Allowed Radius:** "
                    f"{event_row['allowed_radius']} meters"
                )

                qr_data = (
                    f"http://localhost:8501/?event={event_row['qr_token']}"
                )

                st.caption(
                    "📱 Scan this QR code to mark attendance."
                )

            with col2:

                qr_image = generate_qr(qr_data)

                st.image(
                    qr_image,
                    width=220
                )
    # -----------------------------------------------------
    # ADMIN DASHBOARD
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-title">📊 Admin Dashboard</div>',
        unsafe_allow_html=True
    )

    connection = get_connection()

    total_events = connection.execute(
        "SELECT COUNT(*) FROM events"
    ).fetchone()[0]

    total_students = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    total_attendance = connection.execute(
        "SELECT COUNT(*) FROM attendance"
    ).fetchone()[0]

    connection.close()


    # -----------------------------------------------------
    # DASHBOARD CARDS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">📅</div>
                <div class="card-title">TOTAL EVENTS</div>
                <div class="card-value">{total_events}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">👨‍🎓</div>
                <div class="card-title">TOTAL STUDENTS</div>
                <div class="card-value">{total_students}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-icon">✅</div>
                <div class="card-title">TOTAL ATTENDANCE</div>
                <div class="card-value">{total_attendance}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # ATTENDANCE RECORDS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Attendance Records</div>',
        unsafe_allow_html=True
    )

    connection = get_connection()

    attendance_df = pd.read_sql_query(
        """
        SELECT
            attendance.attendance_id,
            events.event_name,
            users.user_id,
            users.name,
            attendance.timestamp,
            attendance.latitude,
            attendance.longitude,
            attendance.distance,
            events.allowed_radius,
            attendance.status
        FROM attendance
        JOIN events
            ON attendance.event_id = events.event_id
        JOIN users
            ON attendance.user_id = users.user_id
        ORDER BY attendance.attendance_id DESC
        """,
        connection
    )

    connection.close()


    if attendance_df.empty:

        st.info(
            "📭 No attendance records yet."
        )

    else:

        display_df = attendance_df.rename(
            columns={
                "attendance_id": "ID",
                "event_name": "Event",
                "user_id": "Student ID",
                "name": "Student Name",
                "timestamp": "Timestamp",
                "latitude": "Latitude",
                "longitude": "Longitude",
                "distance": "Distance (m)",
                "allowed_radius": "Allowed Radius (m)",
                "status": "Status"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        st.download_button(
            label="📥 Download Attendance Report",
            data=attendance_df.to_csv(index=False),
            file_name="attendance_report.csv",
            mime="text/csv",
            use_container_width=True
        )


        # -------------------------------------------------
        # ATTENDANCE CHART
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">📈 Attendance Analytics</div>',
            unsafe_allow_html=True
        )

        event_counts = (
            attendance_df
            .groupby("event_name")
            .size()
            .reset_index(name="attendance")
        )

        fig = px.bar(
            event_counts,
            x="event_name",
            y="attendance",
            text="attendance",
            title="Attendance by Event"
        )

        fig.update_layout(
            xaxis_title="Event",
            yaxis_title="Students Present",
            showlegend=False,
            height=420
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # -------------------------------------------------
        # SUSPICIOUS ATTENDANCE
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">⚠️ Geo-Fence Monitoring</div>',
            unsafe_allow_html=True
        )

        suspicious_count = (
            attendance_df["distance"]
            >= attendance_df["allowed_radius"] * 0.8
        ).sum()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "⚠️ Boundary Attendance",
                suspicious_count
            )

        with col2:

            if suspicious_count == 0:

                st.success(
                    "✅ No boundary attendance detected."
                )

            else:

                st.warning(
                    "⚠️ Attendance near the geo-fence boundary detected."
                )


    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="footer">
            QR-Based Geo-Tagged Attendance Management System
            <br>
            Smart • Secure • Location-Aware
        </div>
        """,
        unsafe_allow_html=True
    )