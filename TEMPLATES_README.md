# KASIR Templates Documentation

## Overview
Complete set of HTML templates for the KASIR Point of Sale system with modern, responsive design using Bootstrap 5.

## Design Features
- **Theme**: Blue-green gradient premium theme
- **Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Poppins & Inter from Google Fonts
- **Mobile**: Fully responsive design
- **Interactive**: AJAX calls, animations, modal dialogs

## Directory Structure

```
templates/
├── base.html                      # Base template with sidebar & navbar
├── public/
│   └── login.html                # Public login page
├── auth/
│   ├── login.html                # Auth login page
│   └── register.html             # Registration page
├── admin/
│   ├── dashboard.html            # Admin dashboard with stats & charts
│   ├── users.html                # User management list
│   ├── user_form.html            # Add/Edit user form
│   └── user_detail.html          # User detail view
├── cashier/
│   ├── index.html                # Full POS interface
│   └── receipt.html              # Printable receipt
├── finance/
│   ├── dashboard.html            # Finance dashboard
│   ├── records.html              # Financial records list
│   ├── record_form.html          # Add/Edit financial record
│   └── reports.html              # Financial reports
├── orders/
│   ├── online.html               # Online orders list
│   ├── qr_generate.html          # QR code generator
│   ├── order_detail.html         # Order details
│   └── customer_order.html       # Public ordering page
└── errors/
    ├── 403.html                  # Access denied
    ├── 404.html                  # Not found
    └── 500.html                  # Server error
```

## Key Features by Template

### base.html
- Responsive sidebar navigation
- Top navbar with user info
- Role-based menu visibility
- Mobile-friendly toggle
- Flash message support
- Auto-dismiss alerts

### cashier/index.html (POS)
- Product grid with categories
- Real-time cart management
- Quantity controls
- Tax calculation (10%)
- Payment modal with multiple methods
- Receipt generation
- Print support

### admin/dashboard.html
- Statistics cards with animations
- Interactive charts (Chart.js)
- Recent activity feed
- Quick action buttons
- Responsive grid layout

### finance/dashboard.html
- Income/Expense/Profit cards
- Line chart for trends
- Doughnut chart for categories
- Period filters

### orders/customer_order.html
- Public ordering interface
- Interactive product selection
- Table number input
- Order notes
- Responsive design

## Color Scheme

```css
Primary Blue:   #0f2a3d
Primary Teal:   #1a4d6e
Primary Green:  #2ecc71
Accent Blue:    #3498db
Success:        #27ae60
Warning:        #f39c12
Danger:         #e74c3c
```

## Usage Examples

### Extending base.html
```jinja
{% extends "base.html" %}

{% block title %}Page Title{% endblock %}
{% block page_title %}Page Heading{% endblock %}

{% block extra_css %}
<style>
    /* Custom CSS */
</style>
{% endblock %}

{% block content %}
    <!-- Your content here -->
{% endblock %}

{% block extra_js %}
<script>
    // Custom JavaScript
</script>
{% endblock %}
```

### Hide sidebar/navbar (for login pages)
```jinja
{% extends "base.html" %}
{% set hide_sidebar = true %}
{% set hide_navbar = true %}
```

### Flash messages (automatic)
```python
from flask import flash
flash('Success message', 'success')
flash('Error message', 'danger')
```

## Routes Required

The templates expect these Flask routes to exist:

### Auth
- `auth.login` (GET, POST)
- `auth.register` (GET, POST)
- `auth.logout` (POST)

### Admin
- `admin.dashboard` (GET)
- `admin.users` (GET)
- `admin.user_form` (GET, POST)
- `admin.user_detail` (GET)

### Cashier
- `cashier.index` (GET)
- `cashier.receipt` (GET)

### Finance
- `finance.dashboard` (GET)
- `finance.records` (GET)
- `finance.record_form` (GET, POST)
- `finance.reports` (GET)

### Orders
- `orders.online` (GET)
- `orders.qr_generate` (GET)
- `orders.order_detail` (GET)
- `orders.customer_order` (GET, POST)

## Session Variables

Templates expect these session variables:
- `session.user` - Username
- `session.role` - User role (admin, cashier, finance)

## Dependencies

### CDN Resources
- Bootstrap 5.3.0
- Font Awesome 6.4.0
- jQuery 3.7.0
- Chart.js 4.4.0
- Google Fonts (Poppins, Inter)

### Static Files
- `/static/css/style.css` (referenced but optional)
- `/static/js/script.js` (referenced but optional)

## Browser Support
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Responsive Breakpoints
- Desktop: > 992px (full sidebar)
- Tablet: 768px - 992px (collapsible sidebar)
- Mobile: < 768px (hamburger menu)

## Accessibility
- Semantic HTML5 elements
- ARIA labels where needed
- Keyboard navigation support
- Screen reader friendly

## Performance
- Lazy-loaded images
- Minified CSS/JS (via CDN)
- Optimized animations
- Mobile-first approach

## Customization

### Change Theme Colors
Edit CSS variables in `base.html`:
```css
:root {
    --primary-gradient: linear-gradient(135deg, #0f2a3d 0%, #1a4d6e 50%, #2ecc71 100%);
    --primary-blue: #0f2a3d;
    --primary-green: #2ecc71;
}
```

### Add New Menu Items
In `base.html` sidebar-menu section:
```html
<a href="{{ url_for('route_name') }}" class="menu-item">
    <i class="fas fa-icon"></i>
    <span>Menu Label</span>
</a>
```

## Testing Checklist
- [ ] All pages render without errors
- [ ] Mobile responsiveness works
- [ ] Sidebar toggle functions
- [ ] Forms submit correctly
- [ ] Flash messages display
- [ ] Charts render (where applicable)
- [ ] Print receipt works
- [ ] QR code generates
- [ ] Error pages display

## Notes
- All monetary values use Indonesian Rupiah (Rp) format
- Date/time uses Indonesian locale (id-ID)
- Forms use POST method with CSRF protection expected
- AJAX calls expect JSON responses
- Receipt auto-prints on load

## Future Enhancements
- Dark mode support
- Multiple language support (i18n)
- PWA capabilities
- Offline mode
- Real-time notifications
- Export to PDF/Excel
