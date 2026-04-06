from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'college_event_key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


def get_db_connection():
    """Create and return a new DB connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vihaan@2507",  # change if needed
        database="college_event"
    )


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/api/registrations', methods=['POST'])
def register():
    data = request.json or {}

    required_fields = ['full_name', 'student_id', 'email']
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({
            "status": "error",
            "message": "Missing required fields",
            "missing": missing
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO registrations 
    (full_name, student_id, email, phone, department, year, event_type, event_name, category, team_size, notes) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data.get('full_name'),
        data.get('student_id'),
        data.get('email'),
        data.get('phone'),
        data.get('department'),
        data.get('year'),
        data.get('event_type'),
        data.get('event_name'),
        data.get('category'),
        data.get('team_size', 1),
        data.get('notes')
    )

    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    socketio.emit('registration:new', {
        "id": new_id,
        "full_name": data.get('full_name')
    })

    return jsonify({
        "status": "success",
        "id": new_id,
        "full_name": data.get('full_name')
    }), 201


@app.route('/api/registrations', methods=['GET'])
def get_all():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM registrations ORDER BY created_at DESC")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM registrations")
    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({"total": total})


# IMPORTANT: route now includes <int:id>
@app.route('/api/registrations/<int:id>', methods=['DELETE'])
def delete_registration(id):
    """Delete a registration by id and emit a socket event."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM registrations WHERE id = %s", (id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return jsonify({"message": "Registration not found"}), 404

    cursor.execute("DELETE FROM registrations WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    socketio.emit('registration:deleted', {"id": id})

    return jsonify({"message": "Deleted", "id": id}), 200


if __name__ == '__main__':
    print("\n" + "=" * 30)
    print("ONLINE LINKS:")
    print("REGISTRATION: http://127.0.0.1:5000/")
    print("ADMIN PANEL: http://127.0.0.1:5000/admin")
    print("=" * 30 + "\n")
    socketio.run(app, debug=True)
