"""
KASIR Modern - Main Application File
Version 2.0.0
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from datetime import datetime
import os

from config import config
from models import db, User, Product, Transaction, TransactionItem, FinancialRecord, OnlineOrder
from utils import PaymentService, QRCodeService, generate_unique_id, format_currency
from auth import Permission

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'

# Initialize services
payment_service = PaymentService()
qr_service = QRCodeService()

# Custom Jinja2 filters
@app.template_filter('format_number')
def format_number_filter(value):
    """Format number with thousand separator"""
    try:
        return f"{int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        return value

@app.template_filter('format_currency')
def format_currency_filter(value):
    """Format as currency"""
    return format_currency(value)

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login"""
    return User.query.get(int(user_id))

# Context processor to inject common variables
@app.context_processor
def inject_globals():
    """Inject global variables to all templates"""
    return {
        'app_name': app.config.get('APP_NAME'),
        'app_version': app.config.get('APP_VERSION'),
        'current_year': datetime.now().year,
        'Permission': Permission
    }

# Import blueprints
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.cashier_routes import cashier_bp
from routes.finance_routes import finance_bp
from routes.order_routes import order_bp
from routes.api_routes import api_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(cashier_bp, url_prefix='/cashier')
app.register_blueprint(finance_bp, url_prefix='/finance')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    """Landing page - redirect based on authentication"""
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'pemilik':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('cashier.index'))
    return redirect(url_for('login_page'))

@app.route('/home')
def login_page():
    """Public landing page with login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('public/login.html')

@app.errorhandler(403)
def forbidden(e):
    """Handle 403 Forbidden error"""
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 Not Found error"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 Internal Server Error"""
    return render_template('errors/500.html'), 500

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create default admin
            admin = User(
                username='admin',
                email='admin@kasir.com',
                full_name='Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create default kasir
            kasir = User(
                username='kasir1',
                email='kasir1@kasir.com',
                full_name='Kasir 1',
                role='kasir'
            )
            kasir.set_password('kasir123')
            db.session.add(kasir)
            
            # Create default pemilik
            pemilik = User(
                username='pemilik',
                email='pemilik@kasir.com',
                full_name='Pemilik Toko',
                role='pemilik'
            )
            pemilik.set_password('pemilik123')
            db.session.add(pemilik)
            
            db.session.commit()
            print("✅ Default users created:")
            print("   - Admin: admin / admin123")
            print("   - Kasir: kasir1 / kasir123")
            print("   - Pemilik: pemilik / pemilik123")
        
        # Migrate products from old FOOD_MENU
        if Product.query.count() == 0:
            from data.sample_products import FOOD_MENU
            for item in FOOD_MENU:
                product = Product(
                    name=item['name'],
                    description=item.get('description', ''),
                    category=item['category'],
                    price=item['price'],
                    image_url=item.get('image', ''),
                    is_popular=item.get('popular', False),
                    is_active=True,
                    stock=100,
                    spicy_level=item.get('spicy_level', 'normal')
                )
                db.session.add(product)
            
            db.session.commit()
            print(f"✅ {len(FOOD_MENU)} products imported")

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Initialize database
    init_database()
    
    # Initialize Midtrans
    payment_service.init_midtrans(
        server_key=app.config.get('MIDTRANS_SERVER_KEY'),
        is_production=app.config.get('MIDTRANS_IS_PRODUCTION')
    )
    
    print(f"""
    ╔══════════════════════════════════════════╗
    ║  🍽️  KASIR MODERN - VERSION 2.0.0       ║
    ╚══════════════════════════════════════════╝
    
    🎯 FITUR LENGKAP:
    ✅ Authentication & Session Management
    ✅ Role-Based Access Control (Admin, Kasir, Pemilik)
    ✅ Admin Management (CRUD)
    ✅ Financial Management
    ✅ Manual & Online Payment
    ✅ QR Code Ordering
    ✅ Midtrans Integration (Sandbox)
    ✅ Transaction History & Reports
    ✅ Modern UI/UX Design
    
    🔐 Default Accounts:
    👨‍💼 Admin: admin / admin123
    💵 Kasir: kasir1 / kasir123
    👔 Pemilik: pemilik / pemilik123
    
    🌐 Server: http://localhost:{app.config.get('PORT', 8000)}
    📝 Debug: {app.config.get('DEBUG', False)}
    """)
    
    # Run server
    port = int(os.environ.get('PORT', 8000))
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=port
    )
