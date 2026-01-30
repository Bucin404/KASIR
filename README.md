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
- **MySQL Server** (untuk production) atau SQLite (untuk development)

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

4. **Setup database MySQL (opsional, untuk production)**

**a. Install MySQL Server** (jika belum terinstall)
- Windows: Download dari [MySQL Official](https://dev.mysql.com/downloads/mysql/)
- Linux: `sudo apt-get install mysql-server`
- macOS: `brew install mysql`

**b. Buat database**
```sql
# Login ke MySQL
mysql -u root -p

# Buat database
CREATE DATABASE kasir_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Buat user dan berikan akses (opsional, untuk keamanan)
CREATE USER 'kasir_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON kasir_db.* TO 'kasir_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

5. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env file dengan konfigurasi Anda
```

**Konfigurasi untuk MySQL:**
```env
# Pilihan 1: Gunakan connection string lengkap
DATABASE_URL=mysql+pymysql://kasir_user:your_secure_password@localhost:3306/kasir_db

# Pilihan 2: Gunakan parameter terpisah
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=kasir_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=kasir_db
```

**Konfigurasi untuk SQLite (development):**
```env
# Biarkan kosong atau gunakan SQLite
DATABASE_URL=sqlite:///kasir.db
```

6. **Inisialisasi database**
```bash
python app.py
# Database akan otomatis dibuat dengan menu Solaria
```

7. **Jalankan aplikasi**
```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:8000`

## 🔧 Konfigurasi

### Database Configuration

Aplikasi mendukung dua jenis database:

#### 1. **MySQL (Recommended untuk Production)**
- Performa lebih baik untuk concurrent users
- Scalable untuk growth
- Support transactions dan ACID compliance
- Konfigurasi via environment variables

**Connection String Format:**
```env
DATABASE_URL=mysql+pymysql://[user]:[password]@[host]:[port]/[database]
```

**Atau parameter terpisah:**
```env
MYSQL_HOST=localhost          # atau IP server MySQL
MYSQL_PORT=3306               # default MySQL port
MYSQL_USER=kasir_user         # MySQL username
MYSQL_PASSWORD=your_password  # MySQL password
MYSQL_DATABASE=kasir_db       # Nama database
```

#### 2. **SQLite (Default untuk Development)**
- Tidak perlu instalasi server database
- Portable dan mudah untuk testing
- Auto-fallback jika MySQL tidak dikonfigurasi

```env
DATABASE_URL=sqlite:///kasir.db
```

### Environment Variables (.env)

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
# Untuk MySQL:
DATABASE_URL=mysql+pymysql://kasir_user:password@localhost:3306/kasir_db

# Untuk SQLite (default):
# DATABASE_URL=sqlite:///kasir.db

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
│   └── sample_products.py  # Menu Solaria (54 items)
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
- [x] Gunakan database production (MySQL) - **Sudah dikonfigurasi!**
- [ ] Enable rate limiting
- [ ] Setup logging dan monitoring
- [ ] Regular security updates
- [ ] Backup database secara berkala

## 🍽️ Menu Solaria

Aplikasi ini menggunakan menu asli dari **Solaria Restaurant** dengan 54 item menu yang diambil dari PDF menu resmi.

### Kategori Menu:

1. **Nasi Goreng** (8 items) - Rp 20.000 - Rp 28.000
   - Nasi Goreng Mlarat, Spesial, Cabe Ijo, Sosis, dll.

2. **Mie** (6 items) - Rp 22.000 - Rp 30.000
   - Mie Goreng/Siram dengan Ayam, Seafood, atau Sapi

3. **Kwetiau** (6 items) - Rp 25.000 - Rp 30.000
   - Kwetiau Goreng/Siram dengan berbagai topping

4. **Snack** (6 items) - Rp 12.000 - Rp 20.000
   - Fish Cake, Kentang Goreng, Otak-otak, Sosis, Mix OTP

5. **Menu Lain** (6 items) - Rp 5.000 - Rp 30.000
   - Cap Cay, Sapo Tahu, Nasi Putih, Telur

6. **Paket** (8 items) - Rp 25.000 - Rp 45.000
   - Paket lengkap dengan minuman (Nasi/Mie/Kwetiau + Minuman)

7. **Minuman** (14 items) - Rp 3.000 - Rp 15.000
   - Teh, Kopi, Thai Tea, Lemon Tea, Lemonade, Cappucino, dll.

**Sumber Menu**: `halaman 2 menu solaria_260129_224254.pdf`

**Catatan**: 
- Semua harga sesuai dengan menu asli Solaria
- Kode item menggunakan kode asli dari menu (111, 121, 131, dll.)
- Menu dapat dikustomisasi melalui admin panel

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
