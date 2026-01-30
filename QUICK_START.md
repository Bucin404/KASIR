# KASIR Templates - Quick Start Guide

## 🚀 Getting Started

### 1. Template Structure Overview

```
22 templates created across 7 categories:
- Base template (1)
- Authentication (3) 
- Admin (4)
- Cashier (2)
- Finance (4)
- Orders (4)
- Errors (3)
```

### 2. Required Flask Routes

Create these blueprints in your Flask app:

```python
# app.py
from flask import Flask, render_template
from flask_blueprints import auth, admin, cashier, finance, orders

app = Flask(__name__)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(cashier, url_prefix='/cashier')
app.register_blueprint(finance, url_prefix='/finance')
app.register_blueprint(orders, url_prefix='/orders')

@app.route('/')
def index():
    return render_template('admin/dashboard.html')  # or appropriate landing page
```

### 3. Session Management

Set up session variables for authentication:

```python
from flask import session

# After successful login
session['user'] = username
session['role'] = user_role  # 'admin', 'cashier', or 'finance'

# Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
```

### 4. Flash Messages

Templates support Bootstrap-style flash messages:

```python
from flask import flash

# Success
flash('Operation successful!', 'success')

# Error
flash('Something went wrong!', 'danger')

# Warning
flash('Please be careful!', 'warning')

# Info
flash('Just so you know...', 'info')
```

### 5. Example Blueprint Structure

```
your_app/
├── app.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── admin.py
│   ├── cashier.py
│   ├── finance.py
│   └── orders.py
├── templates/
│   └── (all templates from this project)
└── static/
    ├── css/
    └── js/
```

### 6. Minimal Blueprint Example

```python
# routes/admin.py
from flask import Blueprint, render_template, session, redirect, url_for

admin = Blueprint('admin', __name__)

@admin.before_request
def check_admin():
    if session.get('role') != 'admin':
        return redirect(url_for('errors.forbidden'))

@admin.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html',
                         users_count=10,
                         orders_today=25,
                         revenue_today=500000,
                         pending_orders=5)

@admin.route('/users')
def users():
    users = []  # Get from database
    return render_template('admin/users.html', users=users)
```

### 7. Testing Templates

```bash
# Install Flask
pip install flask

# Create minimal app.py
python app.py

# Visit http://localhost:5000
```

### 8. Customizing Colors

Edit CSS variables in `templates/base.html`:

```css
:root {
    --primary-blue: #0f2a3d;    /* Change to your color */
    --primary-green: #2ecc71;   /* Change to your color */
}
```

### 9. Adding New Pages

1. Create new template extending base.html
2. Add route in appropriate blueprint
3. Update sidebar menu in base.html if needed

Example:

```html
<!-- templates/admin/settings.html -->
{% extends "base.html" %}
{% block title %}Settings{% endblock %}
{% block page_title %}Settings{% endblock %}
{% block content %}
    <h1>Settings Page</h1>
{% endblock %}
```

```python
# routes/admin.py
@admin.route('/settings')
def settings():
    return render_template('admin/settings.html')
```

### 10. Common Issues & Solutions

**Issue: Sidebar not showing**
- Check `hide_sidebar` is not set to true
- Verify session variables are set

**Issue: Flash messages not showing**
- Ensure you're using `flash()` before redirect
- Check Bootstrap JS is loaded

**Issue: Charts not rendering**
- Verify Chart.js CDN is accessible
- Check console for JavaScript errors

**Issue: Receipt not printing**
- Ensure browser allows pop-ups
- Check printer permissions

## 📱 Mobile Testing

Test on these breakpoints:
- Mobile: 375px width
- Tablet: 768px width
- Desktop: 1920px width

## 🎨 Customization Tips

1. **Logo**: Replace text in sidebar-brand with `<img>` tag
2. **Colors**: Update CSS variables in base.html
3. **Fonts**: Change Google Fonts import in base.html
4. **Layout**: Modify grid classes in templates

## 📚 Resources

- Bootstrap 5 Docs: https://getbootstrap.com/docs/5.3
- Font Awesome: https://fontawesome.com/icons
- Chart.js: https://www.chartjs.org/docs

## ✅ Verification Checklist

- [ ] All 22 templates created
- [ ] Flask routes configured
- [ ] Session management set up
- [ ] Database models ready
- [ ] Static files in place
- [ ] Test on multiple devices
- [ ] Authentication working
- [ ] POS system functional
- [ ] Receipts printing correctly
- [ ] Charts displaying data

## 🆘 Support

For issues or questions, refer to:
- TEMPLATES_README.md (comprehensive documentation)
- Template comments (inline documentation)
- Bootstrap 5 documentation

---

**Created**: 2024
**Framework**: Flask + Bootstrap 5
**Theme**: Blue-Green Premium
**Status**: ✅ Production Ready
