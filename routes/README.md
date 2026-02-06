# KASIR Application Routes

This directory contains all the Flask Blueprint route modules for the KASIR application.

## Route Modules

### 1. auth_routes.py
**Authentication Routes**
- `POST /auth/login` - User login with validation
- `GET /auth/logout` - User logout
- `GET/POST /auth/register` - User registration (admin only or first user)
- `GET /auth/check-session` - Check if user is logged in (API)

**Features:**
- Password validation and hashing
- Email and username validation
- Remember me functionality
- Role-based redirect after login
- First user is automatically admin

### 2. admin_routes.py
**Admin Dashboard and User Management**
- `GET /admin/dashboard` - Admin dashboard with statistics
- `GET /admin/users` - List all users (paginated)
- `GET/POST /admin/users/add` - Add new user
- `GET/POST /admin/users/edit/<id>` - Edit user
- `POST /admin/users/delete/<id>` - Deactivate user
- `POST /admin/users/<id>/toggle-status` - Toggle user active status
- `GET /admin/stats/summary` - Dashboard summary statistics (API)

**Access Control:** Admin and Pemilik only

**Features:**
- Transaction and revenue statistics
- User management CRUD operations
- Real-time statistics
- Top products tracking
- Recent transactions view

### 3. cashier_routes.py
**POS Interface and Transaction Processing**
- `GET /cashier/` - Main POS interface
- `GET /cashier/transactions` - View transaction history
- `GET /cashier/transaction/<id>` - View transaction details
- `POST /cashier/process-transaction` - Process new transaction
- `GET /cashier/print-receipt/<id>` - Print receipt
- `POST /cashier/cancel-transaction/<id>` - Cancel transaction
- `GET /cashier/products/search` - Search products (API)

**Access Control:** Kasir, Admin, and Pemilik

**Features:**
- Real-time product search
- Multiple payment methods (cash, QR, online)
- Tax and discount calculation
- Transaction type support (dine-in, takeaway, online)
- Receipt printing
- Transaction history filtering

### 4. finance_routes.py
**Financial Management and Reporting**
- `GET /finance/dashboard` - Finance dashboard
- `GET /finance/records` - List financial records (paginated, filtered)
- `GET/POST /finance/records/add` - Add new financial record
- `GET/POST /finance/records/edit/<id>` - Edit financial record
- `POST /finance/records/delete/<id>` - Delete financial record
- `GET /finance/reports` - Financial reports with charts
- `GET /finance/api/summary` - Financial summary (API)

**Access Control:** Admin and Pemilik only

**Features:**
- Income and expense tracking
- Category-based filtering
- Date range filtering
- Profit/loss calculations
- Monthly and yearly reports
- Revenue vs expense analysis

### 5. order_routes.py
**Online Orders and QR Code Ordering**
- `GET /order/menu` - Public menu page for online ordering
- `POST /order/place-order` - Place new online order
- `GET /order/payment/<order_id>` - Payment page
- `POST /order/payment-callback` - Midtrans payment callback
- `GET /order/status/<order_id>` - Check order status
- `GET /order/manage` - Manage online orders (staff)
- `POST /order/update-status/<id>` - Update order status
- `GET /order/qr-generate` - Generate QR code for table
- `GET /order/api/orders` - Get orders (API)

**Access Control:** Public for menu/ordering, staff for management

**Features:**
- QR code ordering system
- Midtrans payment integration
- Order status tracking
- Table number assignment
- Real-time order management
- Payment gateway integration

### 6. api_routes.py
**RESTful API Endpoints**

**Products:**
- `GET /api/products` - Get all products (with filters)
- `GET /api/products/<id>` - Get single product
- `GET /api/products/categories` - Get all categories

**Transactions:**
- `GET /api/transactions` - Get transactions (filtered, paginated)
- `GET /api/transactions/<id>` - Get single transaction
- `GET /api/transactions/search` - Search transactions

**Statistics:**
- `GET /api/stats/dashboard` - Dashboard statistics
- `GET /api/stats/sales` - Sales statistics for charts
- `GET /api/stats/top-products` - Top selling products

**Users:**
- `GET /api/users` - Get all users (admin only)

**Orders:**
- `GET /api/orders` - Get online orders
- `GET /api/orders/<order_id>` - Get single order

**Finance:**
- `GET /api/finance/summary` - Financial summary

**System:**
- `GET /api/health` - API health check

## Role-Based Access Control

The routes use decorators from `auth.py` for role-based access control:

- `@admin_required` - Admin only
- `@cashier_required` - Kasir, Admin, and Pemilik
- `@owner_required` - Admin and Pemilik only
- `@login_required_with_role('admin', 'pemilik')` - Custom role list

## Common Features

All routes include:
- Proper error handling with try-catch blocks
- Database transaction management (commit/rollback)
- Flash messages for user feedback
- JSON responses for API endpoints
- Pagination for list views
- Search and filter capabilities
- Input validation
- SQLAlchemy ORM usage

## Blueprint Registration

To use these routes in your Flask application, register them in `app.py`:

```python
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.cashier_routes import cashier_bp
from routes.finance_routes import finance_bp
from routes.order_routes import order_bp
from routes.api_routes import api_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(cashier_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(order_bp)
app.register_blueprint(api_bp)
```

## Dependencies

These routes depend on:
- `models.py` - Database models
- `auth.py` - Authentication decorators
- `config.py` - Application configuration
- Flask-Login - User session management
- Flask-SQLAlchemy - Database ORM

## API Response Format

All API endpoints return JSON in this format:

**Success:**
```json
{
  "success": true,
  "data": {...}
}
```

**Error:**
```json
{
  "success": false,
  "message": "Error description"
}
```

## Testing

To test the routes:
1. Ensure database is initialized
2. Create test users with different roles
3. Use Postman or curl for API testing
4. Check browser console for AJAX errors

## Security Notes

- All password handling uses Werkzeug's secure hashing
- CSRF protection should be enabled in production
- SQL injection prevented by SQLAlchemy ORM
- Role-based access control enforced on all protected routes
- Input validation on all forms
- Soft delete for users (deactivation instead of deletion)
