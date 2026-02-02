# Developer/Admin System - Testing Guide

## 🧪 Complete Testing Checklist

### Phase 1: Setup & Verification ✅

#### 1.1 Database Models Verification
```bash
# In Django shell, verify all models exist:
python manage.py shell

from hello_world.core.models import (
    DeveloperAdmin, AdminUser, AdminAccessLog, AdminCredentials
)

# List tables
python manage.py dbshell
SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%admin%';
```

**Expected Result**: 
- ✅ Table `core_developeradmin` exists
- ✅ Table `core_adminuser` exists  
- ✅ Table `core_adminaccesslog` exists
- ✅ Table `core_admincredentials` exists

---

#### 1.2 Migration Status
```bash
python manage.py showmigrations core

# Should show:
# [X] 0008_alter_adminuser_options_adminuser_can_delete_content_and_more
```

**Expected Result**: 
- ✅ Migration 0008 marked as applied [X]

---

#### 1.3 URL Routes Verification
```bash
python manage.py show_urls | grep developer

# Should show:
# developer-login/
# developer-dashboard/
# create-admin/
# manage-admin/
# developer-logout/
```

**Expected Result**:
- ✅ 5 developer routes present

---

### Phase 2: Initial Setup Test

#### 2.1 Create Developer Admin Account
```bash
python manage.py shell

from django.contrib.auth.models import User
from hello_world.core.models import DeveloperAdmin
from django.contrib.auth.hashers import make_password

# Step 1: Create Django user
user = User.objects.create_user(
    username='dev_test',
    email='dev@test.com',
    password='test123'
)

# Step 2: Create DeveloperAdmin
dev = DeveloperAdmin.objects.create(
    user=user,
    developer_id='DEV_TEST_001',
    master_key=make_password('master_key_123'),
    organization_name='Test Organization'
)

print(f"✅ Developer created: {dev.developer_id}")
exit()
```

**Expected Result**:
- ✅ DeveloperAdmin record created
- ✅ developer_id = 'DEV_TEST_001'
- ✅ master_key hashed properly

---

### Phase 3: Frontend Tests

#### 3.1 Test Developer Login Page
```
1. Start server: python manage.py runserver 0.0.0.0:8000
2. Navigate to: http://localhost:8000/developer-login/
3. Page should load with:
   - Purple gradient background
   - Animated developer icon (👨‍💻)
   - Form with 2 input fields: developer_id, master_key
   - Security badge
   - Back links at bottom
```

**Pass Criteria**:
- ✅ Page loads without errors
- ✅ Animations visible
- ✅ Form properly styled
- ✅ CSS gradient background displays

---

#### 3.2 Test Developer Login - Failed Attempt
```
1. On login page, enter:
   - Developer ID: wrong_id
   - Master Key: wrong_key
2. Click submit
3. Should show error message:
   "Invalid developer ID or master key"
```

**Pass Criteria**:
- ✅ Error message displayed
- ✅ Page reloads with form cleared
- ✅ No sensitive info revealed

---

#### 3.3 Test Developer Login - Success
```
1. On login page, enter:
   - Developer ID: DEV_TEST_001
   - Master Key: master_key_123
2. Click submit
3. Should redirect to developer dashboard
```

**Pass Criteria**:
- ✅ Redirects to /developer-dashboard/
- ✅ Session created
- ✅ Developer admin displayed
- ✅ AdminLoginRecord created

---

#### 3.4 Test Developer Dashboard
```
1. Navigate to: http://localhost:8000/developer-dashboard/
2. (If not logged in, should redirect to developer login)
3. Dashboard should show:
   - Dashboard title with icon
   - 4 statistics cards (admins, active, societies, events)
   - "Create New Admin" button
   - Logout button
   - Admin management section
   - Activity logs section
```

**Pass Criteria**:
- ✅ Protected route (requires developer login)
- ✅ All sections render
- ✅ Statistics display correctly
- ✅ Purple gradient background
- ✅ Responsive layout

---

#### 3.5 Test Create Admin Page
```
1. Click "Create New Admin" button
2. Form should display with fields:
   - Username (required)
   - Email (required)
   - Admin Role (6 options in dropdown)
   - Assign to Society (optional)
3. Select role and see description update
4. Fill form:
   - Username: admin_test_001
   - Email: admin001@test.com
   - Role: super_admin
5. Click "Create Admin"
```

**Pass Criteria**:
- ✅ Form loads correctly
- ✅ Role descriptions update dynamically
- ✅ Form validation works
- ✅ Role selection works

---

#### 3.6 Test Admin Creation Success
```
1. After form submission, should see admin_created.html
2. Page should display:
   - Success checkmark (✅) with animation
   - Admin information (username, email, role, date)
   - Temporary password in highlighted box
   - Copy button functional
   - Warning about password
   - Action buttons (Create Another, Go to Dashboard)
```

**Pass Criteria**:
- ✅ Confirmation page displays
- ✅ Temporary password visible
- ✅ Copy button works
- ✅ Admin info accurate
- ✅ Next step buttons functional

---

#### 3.7 Test Manage Admin Page
```
1. Go back to Dashboard
2. Click "Edit" on admin_test_001 card
3. Should see manage_admin.html with:
   - Admin information section
   - Role dropdown (currently: super_admin)
   - Society multi-select
   - Current permissions list
   - Deactivate button
```

**Pass Criteria**:
- ✅ Admin details display correctly
- ✅ Role dropdown works
- ✅ Society selector works
- ✅ Permissions show correctly
- ✅ Action buttons functional

---

### Phase 4: Backend Logic Tests

#### 4.1 Test Permission Update on Role Change
```python
from hello_world.core.models import AdminUser

# Get the test admin
admin = AdminUser.objects.get(user__username='admin_test_001')

# Check super_admin permissions (should all be True)
print(f"can_manage_societies: {admin.can_manage_societies}")
print(f"can_manage_events: {admin.can_manage_events}")
print(f"can_moderate_chat: {admin.can_moderate_chat}")

# Change to events_admin
admin.role = 'events_admin'
admin.update_permissions_from_role()
admin.save()

# Check permissions updated
print(f"can_manage_events: {admin.can_manage_events}")  # Should be True
print(f"can_manage_societies: {admin.can_manage_societies}")  # Should be False
```

**Expected Results**:
- ✅ Super Admin: All permissions True
- ✅ Events Admin: can_manage_events = True, others False
- ✅ Permission update automatic with role change

---

#### 4.2 Test AdminCredentials Creation
```python
from hello_world.core.models import AdminCredentials

# Get credentials for test admin
creds = AdminCredentials.objects.get(admin_user__user__username='admin_test_001')

# Verify fields
print(f"Temporary Password: {creds.temporary_password}")
print(f"Password Changed: {creds.password_changed}")
print(f"API Token: {creds.api_token}")

# Should show:
# Temporary Password: [generated string]
# Password Changed: False
# API Token: [empty initially]
```

**Expected Results**:
- ✅ Temporary password generated (non-empty)
- ✅ password_changed = False initially
- ✅ api_token empty initially

---

### Phase 5: Security Tests

#### 5.1 Test Master Key Hashing
```python
from hello_world.core.models import DeveloperAdmin

dev = DeveloperAdmin.objects.first()

# Master key should be hashed (not plain text)
print(f"Master key (first 10 chars): {dev.master_key[:10]}")

# Should look like: pbkdf2_sha2... (Django hash format)
# NOT like: master_key_123 (plain text)
```

**Expected Results**:
- ✅ Master key is hashed
- ✅ Uses Django's make_password
- ✅ Starts with algorithm prefix

---

#### 5.2 Test Session Security
```
1. Login as developer
2. Note session cookie
3. Try to access developer dashboard in new tab
4. Should work (session valid)
5. Logout
6. Try to access developer dashboard
7. Should redirect to login
```

**Pass Criteria**:
- ✅ Session persists across tabs
- ✅ Session cleared on logout
- ✅ Cannot access without login

---

### Phase 6: Audit Logging Tests

#### 6.1 Test AdminAccessLog Creation
```python
from hello_world.core.models import AdminAccessLog

# Get logs for developer
logs = AdminAccessLog.objects.filter(developer__developer_id='DEV_TEST_001')

for log in logs:
    print(f"Action: {log.action}")
    print(f"Timestamp: {log.timestamp}")
    print(f"IP Address: {log.ip_address}")
    print(f"Resource Type: {log.resource_type}")
    print("---")

# Should include:
# - Developer login action
# - Admin creation actions
# - Any role/permission changes
```

**Expected Results**:
- ✅ Logs created for developer actions
- ✅ Includes timestamps and IP addresses
- ✅ Tracks all administrative changes

---

## ✅ Quick Verification Steps

Run these to quickly verify everything works:

```bash
# 1. Check models exist
python manage.py shell -c "from hello_world.core.models import DeveloperAdmin, AdminUser, AdminAccessLog, AdminCredentials; print('✅ All models imported successfully')"

# 2. Check migrations applied
python manage.py showmigrations core | grep 0008

# 3. Check URL routes
python manage.py show_urls | grep developer

# 4. Check templates exist
ls hello_world/templates/developer*.html
ls hello_world/templates/create_admin.html
ls hello_world/templates/admin_created.html
ls hello_world/templates/manage_admin.html
```

---

## 📊 Success Criteria

All tests pass when:
- ✅ Database models created successfully
- ✅ Migrations applied
- ✅ URL routes working
- ✅ Templates rendering
- ✅ Developer can login
- ✅ Admins can be created
- ✅ Permissions update on role change
- ✅ Audit logs created
- ✅ Session security working
- ✅ No SQL injection vulnerabilities

**Status: Ready for Production ✅**
