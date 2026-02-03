from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Association table for User-Role many-to-many relationship
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

# Association table for Role-Permission many-to-many relationship  
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Permission {self.name}>'

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    permissions = db.relationship('Permission', secondary=role_permissions, 
                                  backref=db.backref('roles', lazy='dynamic'))
    
    def has_permission(self, permission_name):
        return any(p.name == permission_name for p in self.permissions)
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    roles = db.relationship('Role', secondary=user_roles,
                           backref=db.backref('users', lazy='dynamic'))
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role_name):
        return any(r.name == role_name for r in self.roles)
    
    def has_permission(self, permission_name):
        for role in self.roles:
            if role.has_permission(permission_name):
                return True
        return False
    
    def get_primary_role(self):
        if self.roles:
            # Priority: admin > manager > kasir > customer
            role_priority = {'admin': 0, 'manager': 1, 'kasir': 2, 'customer': 3}
            sorted_roles = sorted(self.roles, key=lambda r: role_priority.get(r.name, 99))
            return sorted_roles[0].name
        return 'customer'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    menu_items = db.relationship('MenuItem', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    is_popular = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    has_spicy_option = db.Column(db.Boolean, default=False)
    has_temperature_option = db.Column(db.Boolean, default=False)  # For drinks (hot/cold)
    stock = db.Column(db.Integer, default=100)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image': self.image,
            'category': self.category.name if self.category else None,
            'category_id': self.category_id,
            'is_popular': self.is_popular,
            'is_available': self.is_available,
            'has_spicy_option': self.has_spicy_option,
            'has_temperature_option': self.has_temperature_option,
            'stock': self.stock
        }
    
    def __repr__(self):
        return f'<MenuItem {self.name}>'

class Table(db.Model):
    __tablename__ = 'tables'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    capacity = db.Column(db.Integer, default=4)
    qr_code = db.Column(db.String(255))
    status = db.Column(db.String(20), default='available')  # available, occupied, reserved
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='table', lazy='dynamic')
    
    def __repr__(self):
        return f'<Table {self.number}>'

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'))
    customer_name = db.Column(db.String(100))
    order_type = db.Column(db.String(20), default='dine_in')  # dine_in, takeaway, online
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, cancelled
    subtotal = db.Column(db.Integer, default=0)
    tax = db.Column(db.Integer, default=0)
    discount = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    payment = db.relationship('Payment', backref='order', uselist=False, cascade='all, delete-orphan')
    
    def calculate_totals(self):
        self.subtotal = sum(item.subtotal for item in self.items)
        self.tax = int(self.subtotal * 0.10)  # 10% tax
        self.total = self.subtotal + self.tax - self.discount
        
    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'table': self.table.number if self.table else None,
            'order_type': self.order_type,
            'status': self.status,
            'subtotal': self.subtotal,
            'tax': self.tax,
            'discount': self.discount,
            'total': self.total,
            'notes': self.notes,
            'items': [item.to_dict() for item in self.items],
            'payment': self.payment.to_dict() if self.payment else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.order_number}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    subtotal = db.Column(db.Integer, nullable=False)
    spice_level = db.Column(db.String(20))  # none, mild, medium, hot, extra_hot
    temperature = db.Column(db.String(20))  # hot, cold, normal
    notes = db.Column(db.Text)
    item_status = db.Column(db.String(20), default='pending')  # pending, cooking, ready, served
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    menu_item = db.relationship('MenuItem')
    
    def to_dict(self):
        return {
            'id': self.id,
            'menu_item_id': self.menu_item_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'subtotal': self.subtotal,
            'spice_level': self.spice_level,
            'temperature': self.temperature,
            'notes': self.notes,
            'item_status': self.item_status
        }
    
    def __repr__(self):
        return f'<OrderItem {self.name} x{self.quantity}>'

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # cash, midtrans, transfer
    amount = db.Column(db.Integer, nullable=False)
    paid_amount = db.Column(db.Integer, default=0)
    change_amount = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, paid, failed, refunded
    midtrans_order_id = db.Column(db.String(100))
    midtrans_transaction_id = db.Column(db.String(100))
    midtrans_status = db.Column(db.String(50))
    snap_token = db.Column(db.String(255))  # Midtrans Snap token
    payment_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'payment_method': self.payment_method,
            'amount': self.amount,
            'paid_amount': self.paid_amount,
            'change_amount': self.change_amount,
            'status': self.status,
            'payment_url': self.payment_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.status}>'

class Income(db.Model):
    __tablename__ = 'incomes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total_orders = db.Column(db.Integer, default=0)
    total_income = db.Column(db.Integer, default=0)
    total_tax = db.Column(db.Integer, default=0)
    total_discount = db.Column(db.Integer, default=0)
    net_income = db.Column(db.Integer, default=0)
    cash_income = db.Column(db.Integer, default=0)
    online_income = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Income {self.date}>'

class Setting(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Setting {self.key}>'

class Cart(db.Model):
    """Shopping cart stored in database - supports multiple items per user/session"""
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=True)  # For guest users
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=True)
    order_type = db.Column(db.String(20), default='dine_in')
    customer_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = db.relationship('CartItem', backref='cart', lazy='dynamic', cascade='all, delete-orphan')
    user = db.relationship('User', backref='carts')
    table = db.relationship('Table')
    
    def get_subtotal(self):
        return sum(item.subtotal for item in self.items)
    
    def get_tax(self):
        return int(self.get_subtotal() * 0.10)
    
    def get_total(self):
        return self.get_subtotal() + self.get_tax()
    
    def get_item_count(self):
        return sum(item.quantity for item in self.items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'table_id': self.table_id,
            'order_type': self.order_type,
            'customer_name': self.customer_name,
            'items': [item.to_dict() for item in self.items],
            'subtotal': self.get_subtotal(),
            'tax': self.get_tax(),
            'total': self.get_total(),
            'item_count': self.get_item_count()
        }
    
    def __repr__(self):
        return f'<Cart {self.id}>'

class CartItem(db.Model):
    """Individual item in a shopping cart"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    subtotal = db.Column(db.Integer, nullable=False)
    spice_level = db.Column(db.String(20))  # none, mild, medium, hot, extra_hot
    temperature = db.Column(db.String(20))  # hot, cold, normal
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    menu_item = db.relationship('MenuItem')
    
    def update_subtotal(self):
        self.subtotal = self.price * self.quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'menu_item_id': self.menu_item_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'subtotal': self.subtotal,
            'spice_level': self.spice_level,
            'temperature': self.temperature,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<CartItem {self.name} x{self.quantity}>'
