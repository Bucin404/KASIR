"""Admin routes - Dashboard and User Management"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from auth import admin_required, login_required_with_role
from models import db, User, Transaction, Product, FinancialRecord, OnlineOrder
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required_with_role('admin', 'pemilik')
def dashboard():
    """Admin dashboard with statistics"""
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Transaction statistics
    total_transactions = Transaction.query.count()
    today_transactions = Transaction.query.filter(
        func.date(Transaction.created_at) == today
    ).count()
    
    # Revenue statistics
    total_revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid'
    ).scalar() or 0
    
    today_revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) == today
    ).scalar() or 0
    
    week_revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) >= week_ago
    ).scalar() or 0
    
    month_revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) >= month_ago
    ).scalar() or 0
    
    # Product statistics
    total_products = Product.query.filter_by(is_active=True).count()
    low_stock_products = Product.query.filter(Product.stock < 10, Product.is_active == True).count()
    
    # User statistics
    total_users = User.query.filter_by(is_active=True).count()
    
    # Online orders
    pending_orders = OnlineOrder.query.filter_by(order_status='pending').count()
    
    # Recent transactions
    recent_transactions = Transaction.query.order_by(desc(Transaction.created_at)).limit(10).all()
    
    # Top products - import TransactionItem for proper join
    from models import TransactionItem
    
    top_products = db.session.query(
        Product.name,
        func.sum(TransactionItem.subtotal).label('total_sales')
    ).join(TransactionItem, Product.id == TransactionItem.product_id
    ).join(Transaction, TransactionItem.transaction_id == Transaction.id
    ).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) >= month_ago
    ).group_by(Product.name).order_by(desc('total_sales')).limit(5).all()
    
    return render_template('admin/dashboard.html',
        total_transactions=total_transactions,
        today_transactions=today_transactions,
        total_revenue=total_revenue,
        today_revenue=today_revenue,
        week_revenue=week_revenue,
        month_revenue=month_revenue,
        total_products=total_products,
        low_stock_products=low_stock_products,
        total_users=total_users,
        pending_orders=pending_orders,
        recent_transactions=recent_transactions,
        top_products=top_products
    )

@admin_bp.route('/users')
@admin_required
def users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users_query = User.query.order_by(desc(User.created_at))
    pagination = users_query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users.html', 
        users=pagination.items,
        pagination=pagination
    )

@admin_bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    
    # Get user statistics
    if user.role == 'kasir':
        transaction_count = Transaction.query.filter_by(cashier_id=user_id).count()
        total_sales = db.session.query(func.sum(Transaction.total)).filter(
            Transaction.cashier_id == user_id,
            Transaction.payment_status == 'paid'
        ).scalar() or 0
    else:
        transaction_count = 0
        total_sales = 0
    
    return render_template('admin/user_detail.html',
        user=user,
        transaction_count=transaction_count,
        total_sales=total_sales
    )

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    """Add new user"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            full_name = request.form.get('full_name', '').strip()
            role = request.form.get('role', 'kasir')
            
            # Validation
            if not username or not email or not password or not full_name:
                flash('Semua field harus diisi.', 'danger')
                return render_template('admin/user_form.html')
            
            if User.query.filter_by(username=username).first():
                flash('Username sudah digunakan.', 'danger')
                return render_template('admin/user_form.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email sudah digunakan.', 'danger')
                return render_template('admin/user_form.html')
            
            # Create user
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                role=role,
                is_active=True
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash(f'User {username} berhasil ditambahkan!', 'success')
            return redirect(url_for('admin.users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/user_form.html', user=None)

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            full_name = request.form.get('full_name', '').strip()
            role = request.form.get('role', 'kasir')
            is_active = request.form.get('is_active') == 'on'
            password = request.form.get('password', '')
            
            # Check if email is already used by another user
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != user_id:
                flash('Email sudah digunakan oleh user lain.', 'danger')
                return render_template('admin/user_form.html', user=user)
            
            # Update user
            user.email = email
            user.full_name = full_name
            user.role = role
            user.is_active = is_active
            
            # Update password if provided
            if password:
                user.set_password(password)
            
            db.session.commit()
            flash(f'User {user.username} berhasil diupdate!', 'success')
            return redirect(url_for('admin.users'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('admin/user_form.html', user=user)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete user"""
    if user_id == current_user.id:
        flash('Anda tidak dapat menghapus akun Anda sendiri.', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User.query.get_or_404(user_id)
    
    try:
        # Soft delete - just deactivate
        user.is_active = False
        db.session.commit()
        flash(f'User {user.username} berhasil dinonaktifkan.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'message': 'Tidak dapat mengubah status akun sendiri'}), 400
    
    user = User.query.get_or_404(user_id)
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        
        status = 'diaktifkan' if user.is_active else 'dinonaktifkan'
        return jsonify({
            'success': True,
            'message': f'User {user.username} berhasil {status}',
            'is_active': user.is_active
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/stats/summary')
@login_required_with_role('admin', 'pemilik')
def stats_summary():
    """Get summary statistics for dashboard"""
    today = datetime.now().date()
    
    # Today's statistics
    today_transactions = Transaction.query.filter(
        func.date(Transaction.created_at) == today,
        Transaction.payment_status == 'paid'
    ).count()
    
    today_revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) == today
    ).scalar() or 0
    
    # Pending orders
    pending_orders = OnlineOrder.query.filter_by(payment_status='pending').count()
    
    return jsonify({
        'today_transactions': today_transactions,
        'today_revenue': float(today_revenue),
        'pending_orders': pending_orders
    })
