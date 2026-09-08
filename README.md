# Geo Attendance 📍

## QR-Based Geo-Tagged Attendance Management System

Geo Attendance is a Python-based attendance management system that combines **QR code scanning with location verification** to provide a secure and efficient way to record attendance.

The system allows an organizer to create an event with a specific location and permitted radius. Participants scan the event QR code, and their current geographical location is checked before attendance is recorded.

## 🚀 Features

- 📱 QR code-based attendance
- 📍 Geo-fencing using latitude and longitude
- 📏 Distance calculation using the Haversine formula
- 🚫 Duplicate attendance prevention
- 📊 Attendance dashboard and statistics
- ⚠️ Boundary/suspicious attendance monitoring
- 📥 CSV attendance report download
- 🗄️ SQLite database
- 🌐 Streamlit web application

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **SQLite**
- **Pandas**
- **Plotly**
- **QRCode**
- **Pillow**
- **Streamlit Geolocation**

## ⚙️ How It Works

1. The organizer creates an event with the event name, date, time, location, and allowed radius.
2. The system generates a unique QR code for the event.
3. The participant scans the QR code.
4. The application obtains the participant's geographical location.
5. The system calculates the distance between the participant and the event location.
6. Attendance is marked only if the participant is within the allowed radius.
7. The system prevents duplicate attendance for the same event.
8. The organizer can view attendance records, statistics, and download reports.

## 📂 Project Structure

```text
geo-attendance/
│
├── app.py
├── database.py
├── qr_utils.py
├── location_utils.py
├── requirements.txt
├── data/
│   └── attendance.db
└── .gitignore
