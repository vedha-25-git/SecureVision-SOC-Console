import sqlite3

conn = sqlite3.connect('alerts.db')

cursor = conn.cursor()

alerts = [
    ("Malware Detected", "Critical", "Open"),
    ("Port Scan", "High", "Investigating"),
    ("Failed Login Attempts", "Medium", "Resolved"),
    ("Suspicious IP", "High", "Open"),
    ("USB Device Connected", "Low", "Resolved")
]

cursor.executemany(
    "INSERT INTO alerts(alert_name,severity,status) VALUES(?,?,?)",
    alerts
)

conn.commit()
conn.close()

print("Alerts Inserted Successfully")