"""Finance routes - Financial Management and Reporting"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from auth import owner_required
from models import db, FinancialRecord, Transaction
from sqlalchemy import func, extract
from datetime import datetime, timedelta

finance_bp = Blueprint('finance', __name__, url_prefix='/finance')

@finance_bp.route('/dashboard')
@owner_required
def dashboard():
    """Finance dashboard with summary"""
    today = datetime.now().date()
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)
    
    # Income summary
    today_income = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'income',
        func.date(FinancialRecord.transaction_date) == today
    ).scalar() or 0
    
    month_income = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'income',
        FinancialRecord.transaction_date >= month_start
    ).scalar() or 0
    
    year_income = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'income',
        FinancialRecord.transaction_date >= year_start
    ).scalar() or 0
    
    # Expense summary
    today_expense = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'expense',
        func.date(FinancialRecord.transaction_date) == today
    ).scalar() or 0
    
    month_expense = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'expense',
        FinancialRecord.transaction_date >= month_start
    ).scalar() or 0
    
    year_expense = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'expense',
        FinancialRecord.transaction_date >= year_start
    ).scalar() or 0
    
    # Transaction revenue
    today_revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) == today
    ).scalar() or 0
    
    month_revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) >= month_start
    ).scalar() or 0
    
    year_revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) >= year_start
    ).scalar() or 0
    
    # Net profit
    today_profit = today_revenue + today_income - today_expense
    month_profit = month_revenue + month_income - month_expense
    year_profit = year_revenue + year_income - year_expense
    
    # Recent records
    recent_records = FinancialRecord.query.order_by(
        FinancialRecord.transaction_date.desc(),
        FinancialRecord.created_at.desc()
    ).limit(10).all()
    
    return render_template('finance/dashboard.html',
        today_income=today_income,
        month_income=month_income,
        year_income=year_income,
        today_expense=today_expense,
        month_expense=month_expense,
        year_expense=year_expense,
        today_revenue=today_revenue,
        month_revenue=month_revenue,
        year_revenue=year_revenue,
        today_profit=today_profit,
        month_profit=month_profit,
        year_profit=year_profit,
        recent_records=recent_records
    )

@finance_bp.route('/records')
@owner_required
def records():
    """List financial records"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Filters
    record_type = request.args.get('type', '')
    category = request.args.get('category', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    query = FinancialRecord.query
    
    if record_type:
        query = query.filter_by(record_type=record_type)
    
    if category:
        query = query.filter_by(category=category)
    
    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(FinancialRecord.transaction_date >= start)
        except ValueError:
            pass
    
    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(FinancialRecord.transaction_date <= end)
        except ValueError:
            pass
    
    query = query.order_by(
        FinancialRecord.transaction_date.desc(),
        FinancialRecord.created_at.desc()
    )
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Get categories for filter
    categories = db.session.query(FinancialRecord.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    return render_template('finance/records.html',
        records=pagination.items,
        pagination=pagination,
        categories=categories,
        filters={
            'type': record_type,
            'category': category,
            'start_date': start_date,
            'end_date': end_date
        }
    )

@finance_bp.route('/records/add', methods=['GET', 'POST'])
@owner_required
def add_record():
    """Add new financial record"""
    if request.method == 'POST':
        try:
            record_type = request.form.get('record_type')
            category = request.form.get('category', '').strip()
            amount = float(request.form.get('amount', 0))
            description = request.form.get('description', '').strip()
            reference_id = request.form.get('reference_id', '').strip()
            transaction_date_str = request.form.get('transaction_date')
            
            # Validation
            if not record_type or record_type not in ['income', 'expense']:
                flash('Tipe transaksi tidak valid.', 'danger')
                return render_template('finance/record_form.html')
            
            if not category:
                flash('Kategori harus diisi.', 'danger')
                return render_template('finance/record_form.html')
            
            if amount <= 0:
                flash('Jumlah harus lebih dari 0.', 'danger')
                return render_template('finance/record_form.html')
            
            # Parse date
            try:
                transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                transaction_date = datetime.now().date()
            
            # Create record
            record = FinancialRecord(
                record_type=record_type,
                category=category,
                amount=amount,
                description=description,
                reference_id=reference_id,
                transaction_date=transaction_date,
                created_by=current_user.id
            )
            
            db.session.add(record)
            db.session.commit()
            
            flash('Catatan keuangan berhasil ditambahkan!', 'success')
            return redirect(url_for('finance.records'))
            
        except ValueError as e:
            flash(f'Data tidak valid: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('finance/record_form.html', record=None)

@finance_bp.route('/records/edit/<int:record_id>', methods=['GET', 'POST'])
@owner_required
def edit_record(record_id):
    """Edit financial record"""
    record = FinancialRecord.query.get_or_404(record_id)
    
    if request.method == 'POST':
        try:
            record_type = request.form.get('record_type')
            category = request.form.get('category', '').strip()
            amount = float(request.form.get('amount', 0))
            description = request.form.get('description', '').strip()
            reference_id = request.form.get('reference_id', '').strip()
            transaction_date_str = request.form.get('transaction_date')
            
            # Validation
            if not record_type or record_type not in ['income', 'expense']:
                flash('Tipe transaksi tidak valid.', 'danger')
                return render_template('finance/record_form.html', record=record)
            
            if not category:
                flash('Kategori harus diisi.', 'danger')
                return render_template('finance/record_form.html', record=record)
            
            if amount <= 0:
                flash('Jumlah harus lebih dari 0.', 'danger')
                return render_template('finance/record_form.html', record=record)
            
            # Parse date
            try:
                transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                transaction_date = record.transaction_date
            
            # Update record
            record.record_type = record_type
            record.category = category
            record.amount = amount
            record.description = description
            record.reference_id = reference_id
            record.transaction_date = transaction_date
            
            db.session.commit()
            
            flash('Catatan keuangan berhasil diupdate!', 'success')
            return redirect(url_for('finance.records'))
            
        except ValueError as e:
            flash(f'Data tidak valid: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return render_template('finance/record_form.html', record=record)

@finance_bp.route('/records/delete/<int:record_id>', methods=['POST'])
@owner_required
def delete_record(record_id):
    """Delete financial record"""
    record = FinancialRecord.query.get_or_404(record_id)
    
    try:
        db.session.delete(record)
        db.session.commit()
        flash('Catatan keuangan berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
    
    return redirect(url_for('finance.records'))

@finance_bp.route('/reports')
@owner_required
def reports():
    """Financial reports"""
    # Get current year and month
    now = datetime.now()
    year = request.args.get('year', now.year, type=int)
    month = request.args.get('month', now.month, type=int)
    
    # Monthly report for specified month
    month_start = datetime(year, month, 1).date()
    if month == 12:
        month_end = datetime(year + 1, 1, 1).date()
    else:
        month_end = datetime(year, month + 1, 1).date()
    
    # Get daily summary for the month
    daily_revenue = db.session.query(
        func.date(Transaction.created_at).label('date'),
        func.sum(Transaction.total).label('total')
    ).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) >= month_start,
        func.date(Transaction.created_at) < month_end
    ).group_by(func.date(Transaction.created_at)).all()
    
    # Get expense by category
    expense_by_category = db.session.query(
        FinancialRecord.category,
        func.sum(FinancialRecord.amount).label('total')
    ).filter(
        FinancialRecord.record_type == 'expense',
        FinancialRecord.transaction_date >= month_start,
        FinancialRecord.transaction_date < month_end
    ).group_by(FinancialRecord.category).all()
    
    # Get income by category
    income_by_category = db.session.query(
        FinancialRecord.category,
        func.sum(FinancialRecord.amount).label('total')
    ).filter(
        FinancialRecord.record_type == 'income',
        FinancialRecord.transaction_date >= month_start,
        FinancialRecord.transaction_date < month_end
    ).group_by(FinancialRecord.category).all()
    
    return render_template('finance/reports.html',
        year=year,
        month=month,
        daily_revenue=daily_revenue,
        expense_by_category=expense_by_category,
        income_by_category=income_by_category
    )

@finance_bp.route('/api/summary')
@owner_required
def api_summary():
    """API endpoint for financial summary"""
    period = request.args.get('period', 'today')  # today, week, month, year
    
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
        start_date = today
    
    # Calculate totals
    income = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'income',
        FinancialRecord.transaction_date >= start_date
    ).scalar() or 0
    
    expense = db.session.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.record_type == 'expense',
        FinancialRecord.transaction_date >= start_date
    ).scalar() or 0
    
    revenue = db.session.query(func.sum(Transaction.total)).filter(
        Transaction.payment_status == 'paid',
        func.date(Transaction.created_at) >= start_date
    ).scalar() or 0
    
    profit = revenue + income - expense
    
    return jsonify({
        'income': float(income),
        'expense': float(expense),
        'revenue': float(revenue),
        'profit': float(profit)
    })
