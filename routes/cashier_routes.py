"""Cashier routes - POS Interface and Transaction Processing"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from auth import cashier_required
from models import db, Transaction, TransactionItem, Product
from datetime import datetime
import random
import string

cashier_bp = Blueprint('cashier', __name__, url_prefix='/cashier')

def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TRX{timestamp}{random_str}"

@cashier_bp.route('/')
@cashier_required
def index():
    """Main cashier/POS interface"""
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    products = Product.query.filter_by(is_active=True).order_by(Product.category, Product.name).all()
    # Convert Product objects to dictionaries for JSON serialization in template
    products_dict = [p.to_dict() for p in products]
    
    return render_template('cashier/index.html', 
        products=products_dict,
        categories=categories
    )

@cashier_bp.route('/transactions')
@cashier_required
def transactions():
    """View transaction history"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filter by date if provided
    date_filter = request.args.get('date')
    query = Transaction.query
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Transaction.created_at) == filter_date)
        except ValueError:
            pass
    
    # Filter by cashier for non-admin users
    if current_user.role == 'kasir':
        query = query.filter_by(cashier_id=current_user.id)
    
    query = query.order_by(Transaction.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('cashier/transactions.html',
        transactions=pagination.items,
        pagination=pagination,
        date_filter=date_filter
    )

@cashier_bp.route('/transaction/<int:transaction_id>')
@cashier_required
def transaction_detail(transaction_id):
    """View transaction details"""
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Cashiers can only view their own transactions
    if current_user.role == 'kasir' and transaction.cashier_id != current_user.id:
        flash('Anda tidak memiliki akses ke transaksi ini.', 'danger')
        return redirect(url_for('cashier.transactions'))
    
    return render_template('cashier/transaction_detail.html', transaction=transaction)

@cashier_bp.route('/process-transaction', methods=['POST'])
@cashier_required
def process_transaction():
    """Process a new transaction"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'items' not in data or not data['items']:
            return jsonify({'success': False, 'message': 'Keranjang belanja kosong'}), 400
        
        # Get transaction data
        items = data.get('items', [])
        payment_method = data.get('payment_method', 'cash')
        payment_amount = float(data.get('payment_amount', 0))
        customer_name = data.get('customer_name', '')
        customer_phone = data.get('customer_phone', '')
        discount = float(data.get('discount', 0))
        tax = float(data.get('tax', 0))
        notes = data.get('notes', '')
        transaction_type = data.get('transaction_type', 'dine-in')
        
        # Calculate totals
        subtotal = 0
        transaction_items = []
        
        for item in items:
            product = Product.query.get(item['product_id'])
            if not product or not product.is_active:
                return jsonify({'success': False, 'message': f'Produk tidak ditemukan atau tidak aktif'}), 400
            
            quantity = int(item['quantity'])
            price = float(product.price)
            item_subtotal = quantity * price
            subtotal += item_subtotal
            
            transaction_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': quantity,
                'price': price,
                'subtotal': item_subtotal,
                'notes': item.get('notes', '')
            })
        
        # Calculate final total
        total = subtotal + tax - discount
        change_amount = payment_amount - total if payment_method == 'cash' else 0
        
        if payment_method == 'cash' and payment_amount < total:
            return jsonify({'success': False, 'message': 'Jumlah pembayaran kurang'}), 400
        
        # Create transaction
        transaction = Transaction(
            transaction_id=generate_transaction_id(),
            cashier_id=current_user.id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            payment_method=payment_method,
            payment_status='paid' if payment_method == 'cash' else 'pending',
            subtotal=subtotal,
            tax=tax,
            discount=discount,
            total=total,
            payment_amount=payment_amount,
            change_amount=change_amount,
            notes=notes,
            transaction_type=transaction_type
        )
        
        db.session.add(transaction)
        db.session.flush()  # Get transaction.id
        
        # Add transaction items
        for item_data in transaction_items:
            item = TransactionItem(
                transaction_id=transaction.id,
                product_id=item_data['product_id'],
                product_name=item_data['product_name'],
                quantity=item_data['quantity'],
                price=item_data['price'],
                subtotal=item_data['subtotal'],
                notes=item_data['notes']
            )
            db.session.add(item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transaksi berhasil diproses',
            'transaction_id': transaction.transaction_id,
            'id': transaction.id,
            'total': total,
            'change': change_amount
        })
        
    except ValueError as e:
        return jsonify({'success': False, 'message': f'Data tidak valid: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500

@cashier_bp.route('/print-receipt/<int:transaction_id>')
@cashier_required
def print_receipt(transaction_id):
    """Print receipt for transaction"""
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Cashiers can only print their own transactions
    if current_user.role == 'kasir' and transaction.cashier_id != current_user.id:
        flash('Anda tidak memiliki akses ke transaksi ini.', 'danger')
        return redirect(url_for('cashier.transactions'))
    
    return render_template('cashier/receipt.html', transaction=transaction)

@cashier_bp.route('/cancel-transaction/<int:transaction_id>', methods=['POST'])
@cashier_required
def cancel_transaction(transaction_id):
    """Cancel a transaction"""
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Only unpaid transactions can be cancelled
    if transaction.payment_status == 'paid':
        return jsonify({'success': False, 'message': 'Transaksi yang sudah dibayar tidak dapat dibatalkan'}), 400
    
    # Cashiers can only cancel their own transactions
    if current_user.role == 'kasir' and transaction.cashier_id != current_user.id:
        return jsonify({'success': False, 'message': 'Anda tidak memiliki akses ke transaksi ini'}), 403
    
    try:
        transaction.payment_status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transaksi berhasil dibatalkan'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@cashier_bp.route('/products/search')
@cashier_required
def search_products():
    """Search products for POS"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    
    products_query = Product.query.filter_by(is_active=True)
    
    if query:
        products_query = products_query.filter(
            db.or_(
                Product.name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            )
        )
    
    if category:
        products_query = products_query.filter_by(category=category)
    
    products = products_query.order_by(Product.name).all()
    
    return jsonify({
        'success': True,
        'products': [p.to_dict() for p in products]
    })
