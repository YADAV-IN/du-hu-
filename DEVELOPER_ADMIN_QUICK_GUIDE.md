# Developer/Admin System - Quick Reference Guide

## 🚀 Quick Start

### 1. Initial Setup (Via Django Shell)

```bash
# Open Django shell
python manage.py shell

# Create Developer Admin
from django.contrib.auth.models import User
from hello_world.core.models import DeveloperAdmin
from django.contrib.auth.hashers import make_password

# Create user for developer
dev_user = User.objects.create_user(
    username='developer_admin',
    email='dev@example.com',
    password='temp_password'
)

# Create DeveloperAdmin with master key
dev_admin = DeveloperAdmin.objects.create(
    user=dev_user,
    developer_id='DEV_001',
    master_key=make_password('your_master_key_here'),
    organization_name='Your Organization'
)

print(f"Developer created: {dev_admin.developer_id}")
print(f"Master Key: your_master_key_here (save this safely)")
```

### 2. Access Developer Dashboard

```
URL: http://localhost:8000/developer-login/
Developer ID: DEV_001
Master Key: your_master_key_here
```

---

## 📋 Admin Roles Overview

| Role | Societies | Events | Chat | Reports | Admins | Delete |
|------|-----------|--------|------|---------|--------|--------|
| **Super Admin** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Societies Admin** | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Events Admin** | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Chat Admin** | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Reports Admin** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Limited Admin** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |

---

## 🎯 Common Tasks

### Creating a New Admin User

```
1. Go to Dashboard → "Create New Admin" button
2. Enter username (e.g., "admin_john")
3. Enter email (e.g., "john@example.com")
4. Select role from dropdown
5. Optionally assign to society
6. Click "Create Admin"
7. IMPORTANT: Copy and save temporary password
8. Share password securely with admin
```

### Changing Admin Role

```
1. Go to Dashboard → Find admin in list
2. Click "Edit" button on admin card
3. Change role from dropdown
4. Click "Save Role Changes"
5. Permissions update automatically
```

### Assigning Societies

```
1. Click "Edit" on admin card
2. Scroll to "Assign Societies" section
3. Hold Ctrl/Cmd and select multiple societies
4. Click "Save Societies"
5. Admin can now manage these societies only
```

### Deactivating Admin

```
1. Click "Edit" on admin card
2. Scroll to "Danger Zone" section
3. Click "Deactivate Admin"
4. Confirm the action
5. Admin loses all system access
```

### Viewing Activity Logs

```
1. Scroll to "Recent Activity Logs" on dashboard
2. See all admin and developer actions
3. Details include: Action, Resource, Timestamp, IP
4. Logs are automatically recorded for all changes
```

---

## 🔐 Security Best Practices

### Password Management

```
✓ DO:
  - Use strong, unique developer master key
  - Share temporary passwords through secure channel
  - Require password change on first admin login
  - Regularly review access logs
  - Deactivate unused admin accounts

✗ DON'T:
  - Share master key with admins
  - Use simple passwords
  - Leave temporary passwords visible
  - Ignore access logs
  - Leave deactivated accounts active
```

### Access Control

```
Always follow principle of least privilege:
- Assign lowest necessary role
- Limit societies per admin
- Remove permissions not needed
- Review admin list regularly
- Check audit logs for suspicious activity
```

---

## 📊 Dashboard Statistics

The dashboard shows real-time statistics:

- **Total Admins** - Count of all admin users
- **Active Admins** - Count of enabled admins only
- **Total Societies** - Count of all societies
- **Total Events** - Count of all events
- **Admins by Role** - Breakdown by role type

---

## 🛠️ Troubleshooting

### Admin Can't Log In

```
Check:
1. Is admin account active? (Check manage_admin page)
2. Did admin change temporary password?
3. Is admin's user account enabled?
4. Check IP restrictions (if any)
5. Review AdminLoginRecord table
```

### Can't Create Admin

```
Check:
1. Is developer account active?
2. Is developer logged in?
3. Are permissions intact? (can_create_admins=True)
4. Check Django error logs
5. Verify database migrations applied
```

### Permission Not Working

```
Solution:
1. Go to manage_admin for the user
2. Check current role
3. Click "Save Role Changes" to refresh permissions
4. Verify permission checkboxes in "Current Permissions" section
5. Check AdminUser record in database
```

### Forgot Master Key

```
Recovery (Django shell):
from django.contrib.auth.hashers import make_password
from hello_world.core.models import DeveloperAdmin

dev = DeveloperAdmin.objects.get(developer_id='DEV_001')
dev.master_key = make_password('new_master_key')
dev.save()

# Now login with new key
```

---

## 📁 Database Queries

### View All Admins Created by Developer

```python
from hello_world.core.models import AdminUser, DeveloperAdmin

dev = DeveloperAdmin.objects.get(developer_id='DEV_001')
admins = AdminUser.objects.filter(created_by=dev)

for admin in admins:
    print(f"{admin.user.username} - {admin.get_role_display()} - Active: {admin.is_active}")
```

### View All Actions by Specific Admin

```python
from hello_world.core.models import AdminAccessLog, AdminUser

admin = AdminUser.objects.get(user__username='admin_john')
logs = AdminAccessLog.objects.filter(admin_user=admin)

for log in logs:
    print(f"{log.timestamp}: {log.action} - {log.ip_address}")
```

### Check Admin Permissions

```python
admin = AdminUser.objects.get(user__username='admin_john')
print(f"Manage Societies: {admin.can_manage_societies}")
print(f"Manage Events: {admin.can_manage_events}")
print(f"Moderate Chat: {admin.can_moderate_chat}")
```

### Get Activity Summary

```python
from hello_world.core.models import AdminAccessLog
from datetime import datetime, timedelta

today = datetime.now().date()
logs_today = AdminAccessLog.objects.filter(timestamp__date=today)

print(f"Total actions today: {logs_today.count()}")
for log in logs_today:
    print(f"  {log.timestamp.strftime('%H:%M')} - {log.action}")
```

---

## 🔗 Important URLs

```
/developer-login/           → Developer login page
/developer-dashboard/       → Developer main dashboard
/create-admin/              → Create new admin form
/manage-admin/1/            → Manage admin with ID 1
/developer-logout/          → Logout and end session
/admin-login/               → Regular admin login page
/admin-dashboard/           → Admin dashboard (if exists)
```

---

## 📞 Support

### Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Developer login fails | Verify developer_id and master_key in database |
| Admin not showing on dashboard | Check AdminUser.is_active = True |
| Can't edit admin permissions | Verify DeveloperAdmin.can_modify_permissions = True |
| Temporary password not showing | Check AdminCredentials model for the admin |
| Audit logs empty | Check AdminAccessLog table - ensure dev has can_view_all_logs=True |

---

## 📚 Model Reference

### DeveloperAdmin
```python
user → Django User (OneToOne)
developer_id → String (unique)
master_key → Hashed password
organization_name → String
is_active → Boolean
can_create_admins → Boolean
can_delete_admins → Boolean
can_modify_permissions → Boolean
can_view_all_logs → Boolean
can_manage_all_societies → Boolean
```

### AdminUser
```python
user → Django User (OneToOne)
role → String (6 choices)
created_by → DeveloperAdmin (ForeignKey)
is_active → Boolean
societies → Society list (ManyToMany)
can_manage_societies → Boolean
can_manage_events → Boolean
can_manage_admins → Boolean
can_view_reports → Boolean
can_moderate_chat → Boolean
can_delete_content → Boolean
```

### AdminAccessLog
```python
admin_user → AdminUser (ForeignKey, nullable)
developer → DeveloperAdmin (ForeignKey, nullable)
action → String (description)
resource_type → String
resource_id → Integer
ip_address → IP address
timestamp → DateTime
changes_made → JSON field
```

### AdminCredentials
```python
admin_user → AdminUser (OneToOne)
temporary_password → String
password_changed → Boolean
password_changed_at → DateTime
api_token → String (unique)
token_created_at → DateTime
last_accessed → DateTime
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Developer can log in to dashboard
- [ ] Can view statistics and admin list
- [ ] Can create a new admin user
- [ ] Temporary password displayed after creation
- [ ] Can edit admin role
- [ ] Can assign societies
- [ ] Can deactivate admin
- [ ] Activity logs show actions
- [ ] Admin can log in with temporary password
- [ ] Admin can change password on first login

---

## 🎓 Tips & Tricks

### Quick Admin Creation Script

```python
# Create multiple admins at once
from django.contrib.auth.models import User
from hello_world.core.models import AdminUser, AdminCredentials, DeveloperAdmin
import secrets

dev = DeveloperAdmin.objects.get(developer_id='DEV_001')

admins = [
    {'username': 'admin_events', 'email': 'events@org.com', 'role': 'events_admin'},
    {'username': 'admin_chat', 'email': 'chat@org.com', 'role': 'chat_admin'},
    {'username': 'admin_reports', 'email': 'reports@org.com', 'role': 'reports_admin'},
]

for admin_data in admins:
    temp_pwd = secrets.token_urlsafe(12)
    user = User.objects.create_user(
        username=admin_data['username'],
        email=admin_data['email'],
        password=temp_pwd
    )
    admin = AdminUser.objects.create(
        user=user,
        role=admin_data['role'],
        created_by=dev
    )
    AdminCredentials.objects.create(
        admin_user=admin,
        temporary_password=temp_pwd
    )
    print(f"{admin_data['username']}: {temp_pwd}")
```

### Export Admin Report

```python
from hello_world.core.models import AdminUser, DeveloperAdmin

dev = DeveloperAdmin.objects.get(developer_id='DEV_001')
admins = AdminUser.objects.filter(created_by=dev)

print("Username | Email | Role | Active | Societies")
for admin in admins:
    societies = ", ".join([s.name for s in admin.societies.all()])
    print(f"{admin.user.username} | {admin.user.email} | {admin.get_role_display()} | {admin.is_active} | {societies}")
```

---

**Last Updated**: Today
**System Version**: 1.0
**Status**: ✅ Production Ready
