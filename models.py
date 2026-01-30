from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Model untuk pengguna sistem"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='kasir')  # admin, kasir, pemilik
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='cashier', lazy='dynamic')
    
    def set_password(self, password):
        """Hash dan simpan password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        """Check if user has specific role"""
        return self.role == role
    
    def can_access(self, required_roles):
        """Check if user has permission to access"""
        return self.role in required_roles
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Transaction(db.Model):
    """Model untuk transaksi"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    cashier_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer_name = db.Column(db.String(150))
    customer_phone = db.Column(db.String(20))
    payment_method = db.Column(db.String(20), default='cash')  # cash, qr, online
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled
    subtotal = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    total = db.Column(db.Float, nullable=False)
    payment_amount = db.Column(db.Float)
    change_amount = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    transaction_type = db.Column(db.String(20), default='dine-in')  # dine-in, takeaway, online
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('TransactionItem', backref='transaction', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'cashier': self.cashier.full_name if self.cashier else 'N/A',
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'subtotal': self.subtotal,
            'tax': self.tax,
            'discount': self.discount,
            'total': self.total,
            'payment_amount': self.payment_amount,
            'change_amount': self.change_amount,
            'notes': self.notes,
            'transaction_type': self.transaction_type,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'date_iso': self.created_at.strftime('%Y-%m-%d')
        }

class TransactionItem(db.Model):
    """Model untuk item transaksi"""
    __tablename__ = 'transaction_items'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product_name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.subtotal,
            'notes': self.notes
        }

class Product(db.Model):
    """Model untuk produk"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    is_popular = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transaction_items = db.relationship('TransactionItem', backref='product', lazy='dynamic')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'image': self.image_url,
            'popular': self.is_popular,
            'is_active': self.is_active,
            'stock': self.stock
        }

class FinancialRecord(db.Model):
    """Model untuk catatan keuangan"""
    __tablename__ = 'financial_records'
    
    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(20), nullable=False)  # income, expense
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    reference_id = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_date = db.Column(db.Date, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='financial_records')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'record_type': self.record_type,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'reference_id': self.reference_id,
            'created_by': self.user.full_name if self.user else 'N/A',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'transaction_date': self.transaction_date.strftime('%Y-%m-%d')
        }

class OnlineOrder(db.Model):
    """Model untuk pesanan online via QR"""
    __tablename__ = 'online_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'))
    customer_name = db.Column(db.String(150))
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(120))
    table_number = db.Column(db.String(10))
    qr_code_url = db.Column(db.String(255))
    payment_gateway_id = db.Column(db.String(100))
    payment_url = db.Column(db.String(255))
    order_status = db.Column(db.String(20), default='pending')  # pending, confirmed, preparing, ready, completed, cancelled
    payment_status = db.Column(db.String(20), default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transaction_ref = db.relationship('Transaction', backref='online_order', uselist=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_email': self.customer_email,
            'table_number': self.table_number,
            'qr_code_url': self.qr_code_url,
            'payment_url': self.payment_url,
            'order_status': self.order_status,
            'payment_status': self.payment_status,
            'total_amount': self.total_amount,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
