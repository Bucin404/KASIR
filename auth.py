from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user

def login_required_with_role(*roles):
    """
    Decorator untuk require login dan role tertentu
    Usage: @login_required_with_role('admin', 'pemilik')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Silakan login terlebih dahulu.', 'warning')
                return redirect(url_for('auth.login'))
            
            if roles and current_user.role not in roles:
                flash('Anda tidak memiliki akses ke halaman ini.', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator untuk require role admin"""
    return login_required_with_role('admin')(f)

def cashier_required(f):
    """Decorator untuk require role kasir atau lebih tinggi"""
    return login_required_with_role('admin', 'kasir', 'pemilik')(f)

def owner_required(f):
    """Decorator untuk require role pemilik atau admin"""
    return login_required_with_role('admin', 'pemilik')(f)

class Permission:
    """Class untuk mengelola permissions"""
    
    # Role hierarchy: admin > pemilik > kasir
    ROLE_HIERARCHY = {
        'admin': 3,
        'pemilik': 2,
        'kasir': 1
    }
    
    # Permission mapping
    PERMISSIONS = {
        'manage_users': ['admin'],
        'manage_products': ['admin', 'pemilik'],
        'manage_finances': ['admin', 'pemilik'],
        'view_reports': ['admin', 'pemilik'],
        'process_transactions': ['admin', 'kasir', 'pemilik'],
        'view_transactions': ['admin', 'kasir', 'pemilik'],
        'manage_online_orders': ['admin', 'kasir', 'pemilik'],
    }
    
    @staticmethod
    def can(user, permission):
        """Check if user has permission"""
        if not user or not user.is_authenticated:
            return False
        
        allowed_roles = Permission.PERMISSIONS.get(permission, [])
        return user.role in allowed_roles
    
    @staticmethod
    def has_higher_role(user_role, target_role):
        """Check if user role is higher than target role"""
        user_level = Permission.ROLE_HIERARCHY.get(user_role, 0)
        target_level = Permission.ROLE_HIERARCHY.get(target_role, 0)
        return user_level > target_level
