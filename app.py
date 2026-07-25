from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def dashboard():

    search = request.args.get('search', '')
    severity = request.args.get('severity', '')

    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()

    # Search + Filter
    if severity:
        cursor.execute(
            """
            SELECT * FROM alerts
            WHERE alert_name LIKE ?
            AND severity=?
            """,
            ('%' + search + '%', severity)
        )
    else:
        cursor.execute(
            """
            SELECT * FROM alerts
            WHERE alert_name LIKE ?
            """,
            ('%' + search + '%',)
        )

    alerts = cursor.fetchall()

    # Severity Counters
    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE severity='Critical'"
    )
    critical_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE severity='High'"
    )
    high_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE severity='Medium'"
    )
    medium_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE severity='Low'"
    )
    low_count = cursor.fetchone()[0]

    # Status Counters for Charts
    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE status='Open'"
    )
    open_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE status='Investigating'"
    )
    investigating_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE status='Resolved'"
    )
    resolved_count = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        alerts=alerts,
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        open_count=open_count,
        investigating_count=investigating_count,
        resolved_count=resolved_count
    )


@app.route('/add', methods=['POST'])
def add_alert():

    alert_name = request.form['alert_name']
    severity = request.form['severity']
    status = request.form['status']

    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO alerts(alert_name,severity,status) VALUES(?,?,?)",
        (alert_name, severity, status)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/update_status/<int:id>/<status>')
def update_status(id, status):

    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE alerts SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete_alert(id):

    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM alerts WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)