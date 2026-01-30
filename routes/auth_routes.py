"""Authentication routes - Login, Logout, Register"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from models import db, User
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Username dan password harus diisi.', 'danger')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Akun Anda tidak aktif. Hubungi administrator.', 'warning')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            
            if not next_page or not next_page.startswith('/'):
                if user.role == 'admin':
                    next_page = url_for('admin.dashboard')
                elif user.role == 'kasir':
                    next_page = url_for('cashier.index')
                else:  # pemilik
                    next_page = url_for('finance.dashboard')
            
            flash(f'Selamat datang, {user.full_name}!', 'success')
            return redirect(next_page)
        
        flash('Username atau password salah.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Logout handler"""
    logout_user()
    flash('Anda telah berhasil logout.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user (only accessible by admin or for first user)"""
    # Check if there are any users in the system
    user_count = User.query.count()
    
    # If users exist and current user is not admin, deny access
    if user_count > 0:
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Hanya admin yang dapat mendaftarkan user baru.', 'danger')
            return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()
        role = request.form.get('role', 'kasir')
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username minimal 3 karakter.')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Username hanya boleh huruf, angka, dan underscore.')
        
        if User.query.filter_by(username=username).first():
            errors.append('Username sudah digunakan.')
        
        if not email or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            errors.append('Email tidak valid.')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email sudah digunakan.')
        
        if not password or len(password) < 6:
            errors.append('Password minimal 6 karakter.')
        
        if password != confirm_password:
            errors.append('Password dan konfirmasi password tidak cocok.')
        
        if not full_name:
            errors.append('Nama lengkap harus diisi.')
        
        if role not in ['admin', 'kasir', 'pemilik']:
            errors.append('Role tidak valid.')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            role=role if user_count > 0 else 'admin'  # First user is always admin
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            flash(f'User {username} berhasil didaftarkan!', 'success')
            
            # If this is the first user, log them in
            if user_count == 0:
                login_user(new_user)
                return redirect(url_for('admin.dashboard'))
            
            return redirect(url_for('admin.users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('auth/register.html')

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """API endpoint to check if user is logged in"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        })
    return jsonify({'authenticated': False}), 401
