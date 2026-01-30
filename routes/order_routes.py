"""Order routes - Online Orders and QR Code Ordering"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import current_user
from auth import cashier_required
from models import db, OnlineOrder, Transaction, TransactionItem, Product
from datetime import datetime
import random
import string
import json
import hashlib
import base64

order_bp = Blueprint('order', __name__, url_prefix='/order')

def generate_order_id():
    """Generate unique order ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ORD{timestamp}{random_str}"

def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TRX{timestamp}{random_str}"

@order_bp.route('/menu')
def menu():
    """Public menu page for online ordering"""
    categories = db.session.query(Product.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    products = Product.query.filter_by(is_active=True).order_by(Product.category, Product.name).all()
    
    # Get table number from query param if ordering from QR code
    table_number = request.args.get('table', '')
    
    return render_template('order/menu.html', 
        products=products,
        categories=categories,
        table_number=table_number
    )

@order_bp.route('/place-order', methods=['POST'])
def place_order():
    """Place a new online order"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'items' not in data or not data['items']:
            return jsonify({'success': False, 'message': 'Keranjang belanja kosong'}), 400
        
        # Get order data
        items = data.get('items', [])
        customer_name = data.get('customer_name', '').strip()
        customer_phone = data.get('customer_phone', '').strip()
        customer_email = data.get('customer_email', '').strip()
        table_number = data.get('table_number', '').strip()
        payment_method = data.get('payment_method', 'online')
        
        # Validation
        if not customer_name:
            return jsonify({'success': False, 'message': 'Nama pelanggan harus diisi'}), 400
        
        if not customer_phone:
            return jsonify({'success': False, 'message': 'Nomor telepon harus diisi'}), 400
        
        # Calculate totals
        subtotal = 0
        order_items = []
        
        for item in items:
            product = Product.query.get(item['product_id'])
            if not product or not product.is_active:
                return jsonify({'success': False, 'message': f'Produk tidak ditemukan'}), 400
            
            quantity = int(item['quantity'])
            price = float(product.price)
            item_subtotal = quantity * price
            subtotal += item_subtotal
            
            order_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': quantity,
                'price': price,
                'subtotal': item_subtotal,
                'notes': item.get('notes', '')
            })
        
        # Tax and total (10% tax)
        tax = subtotal * 0.10
        total = subtotal + tax
        
        # Create transaction first
        transaction = Transaction(
            transaction_id=generate_transaction_id(),
            cashier_id=None,  # Online orders don't have cashier initially
            customer_name=customer_name,
            customer_phone=customer_phone,
            payment_method=payment_method,
            payment_status='pending',
            subtotal=subtotal,
            tax=tax,
            discount=0,
            total=total,
            payment_amount=None,
            change_amount=0,
            notes=f"Pesanan online - Meja {table_number}" if table_number else "Pesanan online",
            transaction_type='online'
        )
        
        db.session.add(transaction)
        db.session.flush()
        
        # Add transaction items
        for item_data in order_items:
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
        
        # Create online order
        order_id = generate_order_id()
        online_order = OnlineOrder(
            order_id=order_id,
            transaction_id=transaction.id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            table_number=table_number,
            order_status='pending',
            payment_status='pending',
            total_amount=total
        )
        
        # Generate payment URL for Midtrans if needed
        if payment_method == 'online':
            payment_url = generate_midtrans_payment(online_order, transaction)
            online_order.payment_url = payment_url
        
        db.session.add(online_order)
        db.session.commit()
        
        response_data = {
            'success': True,
            'message': 'Pesanan berhasil dibuat',
            'order_id': order_id,
            'total': total
        }
        
        if payment_method == 'online' and online_order.payment_url:
            response_data['payment_url'] = online_order.payment_url
        
        return jsonify(response_data)
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Data tidak valid: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500

def generate_midtrans_payment(order, transaction):
    """Generate Midtrans payment URL (Snap API)"""
    try:
        # This is a simplified version - you'll need to integrate with actual Midtrans API
        # For now, return a placeholder URL
        
        server_key = current_app.config.get('MIDTRANS_SERVER_KEY')
        is_production = current_app.config.get('MIDTRANS_IS_PRODUCTION', False)
        
        # Midtrans Snap API endpoint
        if is_production:
            snap_url = 'https://app.midtrans.com/snap/v1/transactions'
        else:
            snap_url = 'https://app.sandbox.midtrans.com/snap/v1/transactions'
        
        # Prepare transaction details
        transaction_details = {
            'order_id': order.order_id,
            'gross_amount': int(order.total_amount)
        }
        
        item_details = []
        for item in transaction.items:
            item_details.append({
                'id': str(item.product_id),
                'price': int(item.price),
                'quantity': item.quantity,
                'name': item.product_name
            })
        
        customer_details = {
            'first_name': order.customer_name,
            'email': order.customer_email or f"{order.order_id}@customer.com",
            'phone': order.customer_phone
        }
        
        # For demo purposes, return a mock payment URL
        # In production, you would make an actual API call to Midtrans
        payment_url = f"/order/payment/{order.order_id}"
        
        return payment_url
        
    except Exception as e:
        print(f"Error generating Midtrans payment: {e}")
        return None

@order_bp.route('/payment/<order_id>')
def payment_page(order_id):
    """Payment page for online order"""
    order = OnlineOrder.query.filter_by(order_id=order_id).first_or_404()
    
    if order.payment_status == 'paid':
        return redirect(url_for('order.order_status', order_id=order_id))
    
    return render_template('order/payment.html', order=order)

@order_bp.route('/payment-callback', methods=['POST'])
def payment_callback():
    """Handle payment callback from Midtrans"""
    try:
        data = request.get_json()
        
        order_id = data.get('order_id')
        transaction_status = data.get('transaction_status')
        fraud_status = data.get('fraud_status')
        
        order = OnlineOrder.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify({'success': False, 'message': 'Order not found'}), 404
        
        # Update payment status based on Midtrans response
        if transaction_status == 'capture':
            if fraud_status == 'accept':
                order.payment_status = 'paid'
                order.order_status = 'confirmed'
                if order.transaction_ref:
                    order.transaction_ref.payment_status = 'paid'
        elif transaction_status == 'settlement':
            order.payment_status = 'paid'
            order.order_status = 'confirmed'
            if order.transaction_ref:
                order.transaction_ref.payment_status = 'paid'
        elif transaction_status in ['cancel', 'deny', 'expire']:
            order.payment_status = 'cancelled'
            order.order_status = 'cancelled'
            if order.transaction_ref:
                order.transaction_ref.payment_status = 'cancelled'
        elif transaction_status == 'pending':
            order.payment_status = 'pending'
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@order_bp.route('/status/<order_id>')
def order_status(order_id):
    """Check order status"""
    order = OnlineOrder.query.filter_by(order_id=order_id).first_or_404()
    
    return render_template('order/status.html', order=order)

@order_bp.route('/manage')
@cashier_required
def manage_orders():
    """Manage online orders (for staff)"""
    status_filter = request.args.get('status', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = OnlineOrder.query
    
    if status_filter:
        query = query.filter_by(order_status=status_filter)
    
    query = query.order_by(OnlineOrder.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('order/manage.html',
        orders=pagination.items,
        pagination=pagination,
        status_filter=status_filter
    )

@order_bp.route('/update-status/<int:order_id>', methods=['POST'])
@cashier_required
def update_order_status(order_id):
    """Update order status"""
    order = OnlineOrder.query.get_or_404(order_id)
    
    try:
        new_status = request.form.get('status')
        
        if new_status not in ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']:
            return jsonify({'success': False, 'message': 'Status tidak valid'}), 400
        
        order.order_status = new_status
        
        # If completed, mark transaction as paid
        if new_status == 'completed' and order.transaction_ref:
            order.transaction_ref.payment_status = 'paid'
            order.payment_status = 'paid'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Status pesanan diubah menjadi {new_status}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@order_bp.route('/qr-generate')
@cashier_required
def generate_qr():
    """Generate QR code for table ordering"""
    table_number = request.args.get('table', '1')
    
    # Generate QR code URL
    base_url = request.host_url.rstrip('/')
    qr_url = f"{base_url}/order/menu?table={table_number}"
    
    return render_template('order/qr_generate.html', 
        qr_url=qr_url,
        table_number=table_number
    )

@order_bp.route('/api/orders')
@cashier_required
def api_orders():
    """API endpoint to get orders"""
    status = request.args.get('status', '')
    limit = request.args.get('limit', 10, type=int)
    
    query = OnlineOrder.query
    
    if status:
        query = query.filter_by(order_status=status)
    
    orders = query.order_by(OnlineOrder.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'success': True,
        'orders': [order.to_dict() for order in orders]
    })
