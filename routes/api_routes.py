"""API routes - JSON endpoints for AJAX calls"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
from auth import cashier_required, login_required_with_role
from models import db, Product, Transaction, User, OnlineOrder, FinancialRecord
from sqlalchemy import func, desc, or_
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Product API

@api_bp.route('/products', methods=['GET'])
def get_products():
    """Get all active products"""
    try:
        category = request.args.get('category', '')
        search = request.args.get('search', '')
        popular_only = request.args.get('popular', '').lower() == 'true'
        
        query = Product.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )
        
        if popular_only:
            query = query.filter_by(is_popular=True)
        
        products = query.order_by(Product.category, Product.name).all()
        
        return jsonify({
            'success': True,
            'products': [p.to_dict() for p in products]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product details"""
    try:
        product = Product.query.get_or_404(product_id)
        
        return jsonify({
            'success': True,
            'product': product.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/products/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = db.session.query(Product.category).distinct().all()
        categories = [cat[0] for cat in categories if cat[0]]
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Transaction API

@api_bp.route('/transactions', methods=['GET'])
@cashier_required
def get_transactions():
    """Get transactions with filters"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status', '')
        date = request.args.get('date', '')
        cashier_id = request.args.get('cashier_id', type=int)
        
        query = Transaction.query
        
        if status:
            query = query.filter_by(payment_status=status)
        
        if date:
            try:
                filter_date = datetime.strptime(date, '%Y-%m-%d').date()
                query = query.filter(func.date(Transaction.created_at) == filter_date)
            except ValueError:
                pass
        
        if cashier_id:
            query = query.filter_by(cashier_id=cashier_id)
        elif current_user.role == 'kasir':
            query = query.filter_by(cashier_id=current_user.id)
        
        query = query.order_by(desc(Transaction.created_at))
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'transactions': [t.to_dict() for t in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
@cashier_required
def get_transaction(transaction_id):
    """Get single transaction details"""
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        
        # Cashiers can only view their own transactions
        if current_user.role == 'kasir' and transaction.cashier_id != current_user.id:
            return jsonify({'success': False, 'message': 'Akses ditolak'}), 403
        
        return jsonify({
            'success': True,
            'transaction': transaction.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/transactions/search', methods=['GET'])
@cashier_required
def search_transactions():
    """Search transactions"""
    try:
        query_str = request.args.get('q', '').strip()
        limit = request.args.get('limit', 20, type=int)
        
        if not query_str:
            return jsonify({'success': True, 'transactions': []})
        
        query = Transaction.query.filter(
            or_(
                Transaction.transaction_id.ilike(f'%{query_str}%'),
                Transaction.customer_name.ilike(f'%{query_str}%'),
                Transaction.customer_phone.ilike(f'%{query_str}%')
            )
        )
        
        if current_user.role == 'kasir':
            query = query.filter_by(cashier_id=current_user.id)
        
        transactions = query.order_by(desc(Transaction.created_at)).limit(limit).all()
        
        return jsonify({
            'success': True,
            'transactions': [t.to_dict() for t in transactions]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Statistics API

@api_bp.route('/stats', methods=['GET'])
@cashier_required
def get_stats():
    """Get basic statistics for POS dashboard"""
    try:
        today = datetime.now().date()
        
        # Today's transactions
        today_transactions = Transaction.query.filter(
            func.date(Transaction.created_at) == today
        ).count()
        
        # Today's revenue
        today_revenue = db.session.query(func.sum(Transaction.total)).filter(
            Transaction.payment_status == 'paid',
            func.date(Transaction.created_at) == today
        ).scalar() or 0
        
        # Active products
        active_products = Product.query.filter_by(is_active=True).count()
        
        # Pending online orders
        pending_orders = OnlineOrder.query.filter_by(order_status='pending').count()
        
        return jsonify({
            'success': True,
            'stats': {
                'today_transactions': today_transactions,
                'today_revenue': float(today_revenue),
                'active_products': active_products,
                'pending_orders': pending_orders
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/stats/dashboard', methods=['GET'])
@login_required_with_role('admin', 'pemilik')
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Transactions
        total_transactions = Transaction.query.filter_by(payment_status='paid').count()
        today_transactions = Transaction.query.filter(
            Transaction.payment_status == 'paid',
            func.date(Transaction.created_at) == today
        ).count()
        
        # Revenue
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
        
        # Orders
        pending_orders = OnlineOrder.query.filter_by(order_status='pending').count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_transactions': total_transactions,
                'today_transactions': today_transactions,
                'total_revenue': float(total_revenue),
                'today_revenue': float(today_revenue),
                'week_revenue': float(week_revenue),
                'month_revenue': float(month_revenue),
                'pending_orders': pending_orders
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/stats/sales', methods=['GET'])
@login_required_with_role('admin', 'pemilik')
def get_sales_stats():
    """Get sales statistics for charts"""
    try:
        period = request.args.get('period', 'week')  # week, month, year
        
        today = datetime.now().date()
        
        if period == 'week':
            start_date = today - timedelta(days=7)
            group_by = func.date(Transaction.created_at)
        elif period == 'month':
            start_date = today - timedelta(days=30)
            group_by = func.date(Transaction.created_at)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
            group_by = func.strftime('%Y-%m', Transaction.created_at)
        else:
            start_date = today - timedelta(days=7)
            group_by = func.date(Transaction.created_at)
        
        # Daily/Monthly sales
        sales_data = db.session.query(
            group_by.label('period'),
            func.count(Transaction.id).label('count'),
            func.sum(Transaction.total).label('total')
        ).filter(
            Transaction.payment_status == 'paid',
            func.date(Transaction.created_at) >= start_date
        ).group_by(group_by).order_by(group_by).all()
        
        return jsonify({
            'success': True,
            'sales': [
                {
                    'period': str(row.period),
                    'count': row.count,
                    'total': float(row.total)
                }
                for row in sales_data
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/stats/top-products', methods=['GET'])
@login_required_with_role('admin', 'pemilik')
def get_top_products():
    """Get top selling products"""
    try:
        limit = request.args.get('limit', 10, type=int)
        period_days = request.args.get('days', 30, type=int)
        
        start_date = datetime.now().date() - timedelta(days=period_days)
        
        # Get top products by quantity sold - import TransactionItem model
        from models import TransactionItem
        
        top_products = db.session.query(
            Product.name,
            func.sum(TransactionItem.quantity).label('quantity'),
            func.sum(TransactionItem.subtotal).label('revenue')
        ).join(TransactionItem, Product.id == TransactionItem.product_id
        ).join(Transaction, TransactionItem.transaction_id == Transaction.id
        ).filter(
            Transaction.payment_status == 'paid',
            func.date(Transaction.created_at) >= start_date
        ).group_by(Product.name).order_by(desc('revenue')).limit(limit).all()
        
        return jsonify({
            'success': True,
            'products': [
                {
                    'name': row.name,
                    'quantity': row.quantity or 0,
                    'revenue': float(row.revenue or 0)
                }
                for row in top_products
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# User API

@api_bp.route('/users', methods=['GET'])
@login_required_with_role('admin')
def get_users():
    """Get all users"""
    try:
        role = request.args.get('role', '')
        active_only = request.args.get('active', '').lower() == 'true'
        
        query = User.query
        
        if role:
            query = query.filter_by(role=role)
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        users = query.order_by(User.username).all()
        
        return jsonify({
            'success': True,
            'users': [u.to_dict() for u in users]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Order API

@api_bp.route('/orders', methods=['GET'])
@cashier_required
def get_orders():
    """Get online orders"""
    try:
        status = request.args.get('status', '')
        limit = request.args.get('limit', 20, type=int)
        
        query = OnlineOrder.query
        
        if status:
            query = query.filter_by(order_status=status)
        
        orders = query.order_by(desc(OnlineOrder.created_at)).limit(limit).all()
        
        return jsonify({
            'success': True,
            'orders': [o.to_dict() for o in orders]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get single order details (public endpoint with limited info)"""
    try:
        order = OnlineOrder.query.filter_by(order_id=order_id).first_or_404()
        
        # Return limited information for public access
        # For full details, user should authenticate or provide phone verification
        order_data = {
            'order_id': order.order_id,
            'order_status': order.order_status,
            'payment_status': order.payment_status,
            'total_amount': order.total_amount,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify({
            'success': True,
            'order': order_data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Financial API

@api_bp.route('/finance/summary', methods=['GET'])
@login_required_with_role('admin', 'pemilik')
def get_finance_summary():
    """Get financial summary"""
    try:
        period = request.args.get('period', 'month')  # today, week, month, year
        
        today = datetime.now().date()
        
        if period == 'today':
            start_date = today
        elif period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today.replace(day=1)
        elif period == 'year':
            start_date = today.replace(month=1, day=1)
        else:
            start_date = today.replace(day=1)
        
        # Income
        income = db.session.query(func.sum(FinancialRecord.amount)).filter(
            FinancialRecord.record_type == 'income',
            FinancialRecord.transaction_date >= start_date
        ).scalar() or 0
        
        # Expenses
        expense = db.session.query(func.sum(FinancialRecord.amount)).filter(
            FinancialRecord.record_type == 'expense',
            FinancialRecord.transaction_date >= start_date
        ).scalar() or 0
        
        # Revenue from transactions
        revenue = db.session.query(func.sum(Transaction.total)).filter(
            Transaction.payment_status == 'paid',
            func.date(Transaction.created_at) >= start_date
        ).scalar() or 0
        
        # Net profit
        profit = revenue + income - expense
        
        return jsonify({
            'success': True,
            'summary': {
                'income': float(income),
                'expense': float(expense),
                'revenue': float(revenue),
                'profit': float(profit)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Health check

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers

@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Resource not found'}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'success': False, 'message': 'Internal server error'}), 500
