#  Campus Event Registration System

A real-time web application for managing college event registrations. It features a student-facing registration form and an automated Admin Dashboard with live data visualization.

---

## Tech Stack
* **Backend:** Python (Flask, Flask-SocketIO)
* **Frontend:** HTML5, CSS3, JavaScript (Chart.js)
* **Database:** MySQL

---
## Project Structure

```text
project/
│
├─ app.py
├─ database.sql
├─ requirements.txt
└─ templates/
   ├─ index.html        
   └─ admin.html       
```

## Setup & Installation

### 1. Database Configuration
1.  Open **MySQL Workbench**.
2.  Run the `database.sql` script to create the `college_event` database and `registrations` table.
3.  Ensure your password in `app.py` matches your MySQL root password (e.g., `vihaan@2507`).

### 2. Environment Setup
Install the required Python libraries using the terminal:

```bash
py -m pip install flask flask-socketio mysql-connector-python flask-cors
```

```bash
pip install -r requirements.txt
```

### 3. Running the Application
Start the server from your project directory:
py app.py

### 4. Project Access
Once the server is running, use these links in your browser:

Registration Form: http://127.0.0.1:5000/

Admin Dashboard: http://127.0.0.1:5000/admin

 