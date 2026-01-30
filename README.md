# KASIR Modern - Point of Sale System

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

Aplikasi kasir modern berbasis web dengan fitur lengkap untuk manajemen penjualan, keuangan, dan pemesanan online. Dibangun dengan Flask dan Bootstrap 5.

## 🎯 Fitur Utama

### 1. **Autentikasi & Keamanan** 🔐
- Login dan registrasi dengan validasi
- Session management yang aman
- Password hashing dengan Werkzeug
- Role-based access control (RBAC)

### 2. **Role & Permission** 👥
Tiga tingkatan role pengguna:
- **Admin**: Akses penuh ke semua fitur
- **Pemilik/Manager**: Akses laporan dan manajemen
- **Kasir**: Akses transaksi dan POS

### 3. **Manajemen Admin (CRUD)** 👨‍💼
- Tambah, edit, hapus pengguna
- Daftar pengguna dengan pencarian dan filter
- Detail profil pengguna
- Manajemen role dan permission

### 4. **Manajemen Keuangan** 💰
- Pencatatan pemasukan dan pengeluaran
- Kategorisasi transaksi keuangan
- Laporan keuangan per periode
- Dashboard analitik finansial
- Export laporan ke CSV/PDF

### 5. **Pemesanan & Pembayaran** 🛒
**Pembayaran Manual:**
- Interface POS untuk kasir
- Multiple payment methods (cash, card, e-wallet)
- Auto calculate tax dan kembalian
- Print receipt otomatis

**Pemesanan Online:**
- Order via QR code
- Payment gateway Midtrans (sandbox)
- Tracking status pesanan
- Notifikasi real-time

### 6. **Fitur Tambahan** ✨
- History transaksi lengkap
- Pencarian dan filter advanced
- Export data ke CSV
- Dashboard statistik real-time
- Manajemen produk
- Laporan penjualan
- Mobile responsive

## 🚀 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Virtual environment (recommended)

### Langkah Instalasi

1. **Clone repository**
```bash
git clone https://github.com/Bucin404/KASIR.git
cd KASIR
```

2. **Buat virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env file dengan konfigurasi Anda
```

5. **Inisialisasi database**
```bash
python app_new.py
# Database akan otomatis dibuat dengan sample data
```

6. **Jalankan aplikasi**
```bash
python app_new.py
```

Aplikasi akan berjalan di `http://localhost:8000`

## 🔧 Konfigurasi

### Environment Variables (.env)

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///kasir.db

# Midtrans Payment Gateway (Sandbox)
MIDTRANS_SERVER_KEY=SB-Mid-server-YOUR_SERVER_KEY
MIDTRANS_CLIENT_KEY=SB-Mid-client-YOUR_CLIENT_KEY
MIDTRANS_IS_PRODUCTION=False
```

### Midtrans Integration (Sandbox Mode)

1. Daftar di [Midtrans Sandbox](https://dashboard.sandbox.midtrans.com/)
2. Dapatkan Server Key dan Client Key
3. Masukkan ke file `.env`
4. **PENTING**: Jangan commit key production ke repository public!

Untuk production, gunakan environment variables dari server/hosting:
```bash
export MIDTRANS_SERVER_KEY="your-production-key"
export MIDTRANS_CLIENT_KEY="your-production-key"
export MIDTRANS_IS_PRODUCTION=True
```

## 👤 Default Accounts

Setelah inisialisasi database, gunakan akun berikut untuk login:

| Role | Username | Password | Akses |
|------|----------|----------|-------|
| Admin | `admin` | `admin123` | Full access |
| Pemilik | `pemilik` | `pemilik123` | Reports & management |
| Kasir | `kasir1` | `kasir123` | POS & transactions |

**⚠️ PENTING**: Ubah password default setelah login pertama!

## 📱 Penggunaan

### Untuk Kasir
1. Login dengan akun kasir
2. Pilih menu "Kasir" di sidebar
3. Pilih produk untuk ditambahkan ke keranjang
4. Atur jumlah dan catatan jika perlu
5. Klik "Bayar" dan masukkan jumlah pembayaran
6. Cetak struk untuk pelanggan

### Untuk Admin/Pemilik
1. Login dengan akun admin/pemilik
2. Akses dashboard untuk melihat statistik
3. Kelola pengguna di menu "Manajemen Admin"
4. Lihat laporan keuangan di menu "Keuangan"
5. Monitor pesanan online di menu "Pesanan"

### Pemesanan Online
1. Generate QR code dari menu "Pesanan Online"
2. Customer scan QR code
3. Customer pilih menu dan checkout
4. Pembayaran via Midtrans
5. Notifikasi ke admin/kasir
6. Update status pesanan

## 🏗️ Struktur Proyek

```
KASIR/
├── app.py                 # Legacy app (backup)
├── app_new.py            # Main application file
├── config.py             # Configuration settings
├── models.py             # Database models
├── auth.py               # Authentication & authorization
├── utils.py              # Utility functions & services
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
│
├── data/
│   └── sample_products.py  # Sample product data
│
├── routes/               # Blueprint routes
│   ├── auth_routes.py   # Authentication routes
│   ├── admin_routes.py  # Admin management
│   ├── cashier_routes.py # Cashier POS
│   ├── finance_routes.py # Financial management
│   ├── order_routes.py  # Online orders
│   └── api_routes.py    # REST API endpoints
│
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── public/         # Public pages
│   ├── auth/           # Authentication pages
│   ├── admin/          # Admin pages
│   ├── cashier/        # Cashier POS pages
│   ├── finance/        # Finance pages
│   ├── orders/         # Order pages
│   └── errors/         # Error pages
│
└── static/             # Static files
    ├── css/           # Stylesheets
    ├── js/            # JavaScript files
    ├── images/        # Images
    └── uploads/       # User uploads
```

## 🔒 Keamanan

### Best Practices yang Diterapkan:
✅ Password hashing dengan Werkzeug  
✅ SQL injection prevention via SQLAlchemy ORM  
✅ CSRF protection dengan Flask-WTF  
✅ Session cookie security  
✅ Role-based access control  
✅ Environment variables untuk sensitive data  
✅ Secure payment integration  

### Rekomendasi untuk Production:
- [ ] Gunakan SECRET_KEY yang kuat dan unik
- [ ] Aktifkan HTTPS (SSL/TLS)
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Gunakan database production (PostgreSQL/MySQL)
- [ ] Enable rate limiting
- [ ] Setup logging dan monitoring
- [ ] Regular security updates
- [ ] Backup database secara berkala

## 🧪 Testing

### Manual Testing
```bash
# Test authentication
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Test API endpoints
curl http://localhost:8000/api/products
curl http://localhost:8000/api/transactions/today
```

### Browser Testing
1. Buka `http://localhost:8000`
2. Login dengan kredensial default
3. Test setiap fitur utama
4. Verifikasi responsive design di mobile

## 📊 API Documentation

### Authentication
```
POST /auth/login
POST /auth/logout
POST /auth/register
```

### Products
```
GET  /api/products
GET  /api/products/<id>
POST /api/products (admin only)
PUT  /api/products/<id> (admin only)
```

### Transactions
```
GET  /api/transactions
GET  /api/transactions/<id>
POST /api/checkout
GET  /api/transactions/today
GET  /api/stats
```

### Financial
```
GET  /api/finance/records
POST /api/finance/records
GET  /api/finance/summary
```

### Orders
```
GET  /api/orders
GET  /api/orders/<id>
POST /api/orders/create
PUT  /api/orders/<id>/status
```

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:
1. Fork repository
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Developer

**Bucin404**
- GitHub: [@Bucin404](https://github.com/Bucin404)
- Repository: [KASIR](https://github.com/Bucin404/KASIR)

## 📞 Support

Jika Anda menemukan bug atau memiliki saran, silakan buat [issue](https://github.com/Bucin404/KASIR/issues) di GitHub.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [Midtrans](https://midtrans.com/) - Payment gateway
- [Unsplash](https://unsplash.com/) - Food images

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/Bucin404">Bucin404</a>
  <br>
  ⭐ Star this repo if you find it helpful!
</div>
