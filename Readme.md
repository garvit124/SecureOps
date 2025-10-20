# 🔐 Security Management System

A comprehensive web-based security management system built with Flask, featuring visitor management, suspect tracking, alert systems, and role-based access control.

## 📋 Features

### Core Functionality

- **User Authentication** - Secure login with password hashing
- **Role-Based Access Control** - Admin and User roles with different permissions
- **Visitor Management** - Register, track, and check-in/out visitors
- **Suspect Database** - Track suspects with threat levels (Admin only)
- **Alert System** - Create and manage security alerts
- **User Management** - Add and manage system users (Admin only)
- **Real-time Statistics** - Dashboard with live statistics
- **Search & Filter** - Easy data filtering across all tables

### Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Protected routes with decorators
- SQL injection prevention with parameterized queries

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or Download the Project**

```bash
cd security_system
```

2. **Create a Virtual Environment (Recommended)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the Application**

```bash
python app.py
```

5. **Access the Application**
   Open your browser and navigate to:

```
http://127.0.0.1:5000
```

## 🔑 Default Login Credentials

### Admin Account

- **Username:** `admin`
- **Password:** `admin123`

> ⚠️ **Important:** Change the default admin password after first login in a production environment!

## 👥 User Roles & Permissions

### Admin Role

Full system access including:

- ✅ Dashboard with all statistics
- ✅ User management (add/delete users)
- ✅ Visitor registration and management
- ✅ Suspect database management
- ✅ Alert creation and management
- ✅ All logs and records

### User Role

Limited access including:

- ✅ Dashboard with basic statistics
- ✅ Visitor registration and management
- ✅ Alert creation and management
- ✅ Visitor logs
- ❌ No access to suspect database
- ❌ No user management access

## 📁 Project Structure

```
security_system/
├── app.py                      # Main Flask application
├── database.db                 # SQLite database (auto-generated)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── static/
│   ├── css/
│   │   └── style.css          # Complete styling
│   └── js/
│       └── script.js          # JavaScript functionality
└── templates/
    ├── login.html             # Login page
    ├── admin_dashboard.html   # Admin dashboard
    ├── user_dashboard.html    # User dashboard
    ├── manage_users.html      # User management (Admin)
    ├── add_user.html          # Add new user (Admin)
    ├── register_visitor.html  # Visitor registration
    ├── visitor_logs.html      # Visitor logs
    ├── add_suspect.html       # Add suspect (Admin)
    ├── suspect_records.html   # Suspect database (Admin)
    └── view_alerts.html       # Security alerts
```

## 📖 Usage Guide

### Creating a New User

1. Login as **admin**
2. Navigate to **Manage Users**
3. Click **Add New User**
4. Fill in the form:
   - Username (alphanumeric and underscores only)
   - Password (minimum 6 characters)
   - Role (User or Admin)
5. Click **Create User**

### Registering a Visitor

1. Navigate to **Register Visitor**
2. Fill in visitor details:
   - Full Name
   - Contact Number
   - Purpose of Visit
   - ID Type (Aadhar, PAN, Passport, etc.)
   - ID Number
3. Click **Register Visitor**
4. Visitor is automatically checked in

### Checking Out a Visitor

1. Go to **Visitor Logs**
2. Find the visitor in the table
3. Click **Check Out** button
4. Status changes to "Checked Out"

### Adding a Suspect (Admin Only)

1. Navigate to **Add Suspect**
2. Fill in suspect information:
   - Name
   - Description/Identifying Features
   - Last Seen Location
   - Threat Level (Low/Medium/High/Critical)
3. Click **Add to Suspect Database**

### Creating an Alert

1. Go to **Alerts**
2. Fill in the alert form:
   - Alert Type (Unauthorized Access, Suspicious Activity, etc.)
   - Severity (Low/Medium/High)
   - Description
   - Location
3. Click **Create Alert**

### Resolving an Alert

1. Navigate to **Alerts**
2. Find the pending alert
3. Click **Resolve** button
4. Alert status changes to "Resolved"

## 🗄️ Database Schema

### Users Table

- `id` - Primary key
- `username` - Unique username
- `password` - Hashed password
- `role` - User role (admin/user)
- `created_at` - Account creation timestamp

### Visitors Table

- `id` - Primary key
- `name` - Visitor name
- `contact` - Contact number
- `purpose` - Purpose of visit
- `id_type` - Type of ID document
- `id_number` - ID number
- `check_in` - Check-in timestamp
- `check_out` - Check-out timestamp
- `registered_by` - Username who registered
- `status` - Current status (checked_in/checked_out)

### Suspects Table

- `id` - Primary key
- `name` - Suspect name
- `description` - Physical description
- `last_seen` - Last seen location
- `threat_level` - Threat level (low/medium/high/critical)
- `added_by` - Username who added
- `added_at` - Addition timestamp
- `status` - Status (active/inactive)

### Alerts Table

- `id` - Primary key
- `alert_type` - Type of alert
- `description` - Alert description
- `severity` - Severity level (low/medium/high)
- `location` - Location of incident
- `created_by` - Username who created
- `created_at` - Creation timestamp
- `resolved` - Resolution status (0/1)

## 🎨 UI Features

- **Modern Gradient Design** - Professional blue gradient theme
- **Responsive Layout** - Works on desktop, tablet, and mobile
- **Auto-dismissing Alerts** - Flash messages auto-hide after 5 seconds
- **Search Functionality** - Real-time table search
- **Confirmation Dialogs** - Confirm before critical actions
- **Status Badges** - Color-coded status indicators
- **Interactive Tables** - Hover effects and smooth transitions

## 🔧 Configuration

### Secret Key

Change the secret key in `app.py` for production:

```python
app.secret_key = 'your-secret-key-change-this-in-production'
```

### Database Location

The SQLite database is created automatically in the project root. To change location:

```python
conn = sqlite3.connect('path/to/your/database.db')
```

## 🔒 Security Best Practices

1. **Change Default Credentials** - Update admin password immediately
2. **Use Strong Passwords** - Enforce minimum password requirements
3. **Regular Backups** - Backup database.db regularly
4. **HTTPS in Production** - Use SSL/TLS certificates
5. **Update Dependencies** - Keep Flask and dependencies updated
6. **Environment Variables** - Store secret key in environment variables
7. **Disable Debug Mode** - Set `debug=False` in production

## 📝 Future Enhancements

Potential features for future development:

- Email notifications for alerts
- Photo upload for visitors
- Biometric integration
- Report generation (PDF/Excel)
- SMS alerts for high-priority incidents
- CCTV camera integration
- Mobile app companion
- Advanced analytics dashboard
- Audit logs and activity tracking
- Multi-language support

## 📄 License

This project is open-source and available for educational and commercial use.

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Built with:** Flask, SQLite, JavaScript, HTML5, CSS3

---

⭐ **Star this project if you find it useful!**
