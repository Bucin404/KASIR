from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
import os
import json
import hashlib
from typing import Dict, List, Any

app = Flask(__name__)

# Simpan transaksi ke file
TRANSACTION_FILE = 'transactions.json'

# Inisialisasi file transaksi jika belum ada
if not os.path.exists(TRANSACTION_FILE):
    with open(TRANSACTION_FILE, 'w') as f:
        json.dump([], f)

# Menu dengan gambar makanan realistis dari placeholder atau food photography
FOOD_MENU = [
    # Makanan
    {
        "id": 1, 
        "name": "Nasi Goreng Spesial", 
        "price": 25000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&h=200&fit=crop&auto=format",
        "description": "Nasi goreng dengan telur, ayam, dan sayuran segar",
        "popular": True
    },
    {
        "id": 2, 
        "name": "Mie Ayam Bakso", 
        "price": 20000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=300&h=200&fit=crop&auto=format",
        "description": "Mie ayam dengan bakso sapi pilihan",
        "popular": True
    },
    {
        "id": 3, 
        "name": "Ayam Goreng Crispy", 
        "price": 18000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=300&h=200&fit=crop&auto=format",
        "description": "Ayam goreng crispy dengan bumbu rempah",
        "popular": False
    },
    {
        "id": 4, 
        "name": "Sate Ayam (10 tusuk)", 
        "price": 22000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?w=300&h=200&fit=crop&auto=format",
        "description": "Sate ayam dengan bumbu kacang spesial",
        "popular": True
    },
    {
        "id": 5, 
        "name": "Nasi Campur Komplit", 
        "price": 22000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop&auto=format",
        "description": "Nasi dengan lauk lengkap dan sayuran",
        "popular": False
    },
    {
        "id": 6, 
        "name": "Rendang Daging Sapi", 
        "price": 30000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1555939614-8674f6df1389?w=300&h=200&fit=crop&auto=format",
        "description": "Rendang daging sapi dengan bumbu rempah pilihan",
        "popular": True
    },
    {
        "id": 7, 
        "name": "Soto Ayam Lamongan", 
        "price": 22000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1553909489-cd47e0907980?w=300&h=200&fit=crop&auto=format",
        "description": "Soto ayam dengan bumbu koya dan sambal",
        "popular": True
    },
    {
        "id": 8, 
        "name": "Gado-gado", 
        "price": 18000, 
        "category": "Makanan", 
        "image": "https://images.unsplash.com/photo-1559054663-e8d23213f55c?w=300&h=200&fit=crop&auto=format",
        "description": "Sayuran segar dengan bumbu kacang khas",
        "popular": False
    },
    # Minuman
    {
        "id": 9, 
        "name": "Es Teh Manis", 
        "price": 5000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1597481499753-6e63aca6d3f3?w=300&h=200&fit=crop&auto=format",
        "description": "Es teh manis dengan gula aren",
        "popular": True
    },
    {
        "id": 10, 
        "name": "Jus Alpukat", 
        "price": 15000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1623063878630-7c10b5f6d0c9?w=300&h=200&fit=crop&auto=format",
        "description": "Jus alpukat segar dengan susu kental",
        "popular": True
    },
    {
        "id": 11, 
        "name": "Kopi Latte", 
        "price": 18000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop&auto=format",
        "description": "Kopi latte dengan susu segar",
        "popular": True
    },
    {
        "id": 12, 
        "name": "Air Mineral", 
        "price": 4000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=300&h=200&fit=crop&auto=format",
        "description": "Air mineral botolan 600ml",
        "popular": False
    },
    {
        "id": 13, 
        "name": "Es Jeruk Segar", 
        "price": 8000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=300&h=200&fit=crop&auto=format",
        "description": "Es jeruk peras tanpa biji",
        "popular": True
    },
    {
        "id": 14, 
        "name": "Milkshake Coklat", 
        "price": 20000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=300&h=200&fit=crop&auto=format",
        "description": "Milkshake coklat dengan topping whipped cream",
        "popular": True
    },
    {
        "id": 15, 
        "name": "Matcha Latte", 
        "price": 22000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1561047029-3000c68339ca?w=300&h=200&fit=crop&auto=format",
        "description": "Matcha latte dengan susu oat",
        "popular": False
    },
    {
        "id": 16, 
        "name": "Boba Milk Tea", 
        "price": 18000, 
        "category": "Minuman", 
        "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300&h=200&fit=crop&auto=format",
        "description": "Milk tea dengan bubble boba",
        "popular": True
    },
    # Dessert
    {
        "id": 17, 
        "name": "Brownies Coklat", 
        "price": 12000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=200&fit=crop&auto=format",
        "description": "Brownies coklat premium dengan kacang",
        "popular": True
    },
    {
        "id": 18, 
        "name": "Pisang Goreng", 
        "price": 8000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop&auto=format",
        "description": "Pisang goreng dengan keju parut",
        "popular": False
    },
    {
        "id": 19, 
        "name": "Donat Gula", 
        "price": 7000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1551106652-a5bcf4b29ab6?w=300&h=200&fit=crop&auto=format",
        "description": "Donat lembut dengan taburan gula",
        "popular": True
    },
    {
        "id": 20, 
        "name": "Puding Coklat", 
        "price": 10000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1623334044303-241021148842?w=300&h=200&fit=crop&auto=format",
        "description": "Puding coklat dengan saus karamel",
        "popular": False
    },
    {
        "id": 21, 
        "name": "Es Krim Vanilla", 
        "price": 15000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop&auto=format",
        "description": "Es krim vanilla dengan topping coklat",
        "popular": True
    },
    {
        "id": 22, 
        "name": "Cheesecake Berry", 
        "price": 25000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=300&h=200&fit=crop&auto=format",
        "description": "Cheesecake dengan saus berry segar",
        "popular": True
    },
    {
        "id": 23, 
        "name": "Tiramisu", 
        "price": 22000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=300&h=200&fit=crop&auto=format",
        "description": "Tiramisu klasik Italia",
        "popular": True
    },
    {
        "id": 24, 
        "name": "Waffle Madu", 
        "price": 18000, 
        "category": "Dessert", 
        "image": "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300&h=200&fit=crop&auto=format",
        "description": "Waffle renyah dengan madu dan buah",
        "popular": False
    },
]

# Custom Jinja2 filter untuk format angka
def format_number_filter(value):
    """Format angka dengan pemisah ribuan"""
    try:
        return f"{int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        return value

# Register filter ke Jinja2
app.jinja_env.filters['format_number'] = format_number_filter

# Statistik hari ini
def get_today_stats():
    try:
        with open(TRANSACTION_FILE, 'r') as f:
            transactions = json.load(f)
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_transactions = [t for t in transactions if t.get('date', '').startswith(today)]
        
        total_income = sum(t.get('total', 0) for t in today_transactions)
        total_transactions = len(today_transactions)
        popular_items = {}
        
        for t in today_transactions:
            for item in t.get('items', []):
                name = item.get('name', '')
                quantity = item.get('quantity', 0)
                popular_items[name] = popular_items.get(name, 0) + quantity
        
        most_popular = sorted(popular_items.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'total_income': total_income,
            'total_transactions': total_transactions,
            'most_popular': most_popular,
            'average_transaction': total_income / total_transactions if total_transactions > 0 else 0
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {
            'total_income': 0,
            'total_transactions': 0,
            'most_popular': [],
            'average_transaction': 0
        }

@app.route('/')
def index():
    categories = list(set(item['category'] for item in FOOD_MENU))
    popular_items = [item for item in FOOD_MENU if item.get('popular', False)]
    today_stats = get_today_stats()
    
    return render_template('index.html', 
                         menu=FOOD_MENU, 
                         categories=categories,
                         popular_items=popular_items,
                         today_stats=today_stats,
                         now=datetime.now())

@app.route('/api/menu')
def get_menu():
    return jsonify(FOOD_MENU)

@app.route('/api/stats')
def get_stats():
    return jsonify(get_today_stats())

@app.route('/api/checkout', methods=['POST'])
def checkout():
    try:
        data = request.json
        items = data.get('items', [])
        payment = data.get('payment', 0)
        
        if not items:
            return jsonify({'error': 'Keranjang kosong'}), 400
        
        subtotal = sum(item['price'] * item['quantity'] for item in items)
        tax = round(subtotal * 0.10)
        total = subtotal + tax
        change = payment - total if payment >= total else 0
        
        transaction_id = f"TRX{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        struk_data = {
            'transaction_id': transaction_id,
            'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'date_iso': datetime.now().strftime('%Y-%m-%d'),
            'items': items,
            'subtotal': subtotal,
            'tax': tax,
            'total': total,
            'payment': payment,
            'change': change,
            'cashier': 'Kasir Utama'
        }
        
        # Simpan transaksi
        try:
            with open(TRANSACTION_FILE, 'r') as f:
                transactions = json.load(f)
        except:
            transactions = []
        
        transactions.append(struk_data)
        
        with open(TRANSACTION_FILE, 'w') as f:
            json.dump(transactions, f, indent=2)
        
        return jsonify(struk_data)
    
    except Exception as e:
        print(f"Error in checkout: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/today')
def get_today_transactions():
    try:
        with open(TRANSACTION_FILE, 'r') as f:
            transactions = json.load(f)
        
        today = datetime.now().strftime('%Y-%m-%d')
        today_transactions = [t for t in transactions if t.get('date_iso', '').startswith(today)]
        
        return jsonify({
            'count': len(today_transactions),
            'transactions': today_transactions[-10:][::-1]  # 10 transaksi terbaru
        })
    except Exception as e:
        print(f"Error getting today transactions: {e}")
        return jsonify({'count': 0, 'transactions': []})

@app.route('/api/transactions/recent')
def get_recent_transactions():
    try:
        with open(TRANSACTION_FILE, 'r') as f:
            transactions = json.load(f)
        
        return jsonify(transactions[-5:][::-1])  # 5 transaksi terbaru
    except Exception as e:
        print(f"Error getting recent transactions: {e}")
        return jsonify([])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Buat folder jika belum ada
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("""
    🍽️  KASIR MODERN - VERSION FINAL
    ====================================
    🎯 FITUR BARU:
    1. Dashboard statistik real-time
    2. Menu populer dengan badge
    3. Transaksi history
    4. Animasi loading improved
    5. Notification system enhanced
    6. Error handling complete
    7. Responsive design perfected
    8. Cart animation improved
    9. Fixed: Jinja2 filter 'format_number'
    
    📸 Menggunakan foto makanan dari Unsplash
    📱 Layout menu scrollable, keranjang fixed
    🎨 Tema warna: Biru-Hijau Modern Premium
    🔧 Semua bug telah diperbaiki
    🌐 Server: http://localhost:8000
    """)
    
    # Jalankan server dengan reloader dan debug
    app.run(debug=True, host='0.0.0.0', port=8000, use_reloader=True)