# Perubahan Database dan Menu - KASIR Modern

## 📋 Ringkasan Perubahan

### 1. Migrasi Database ke MySQL

Aplikasi sekarang mendukung **MySQL database** untuk production dengan fitur:

#### Konfigurasi Fleksibel
Dua cara konfigurasi database:

**Opsi 1: Connection String Lengkap**
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/kasir_db
```

**Opsi 2: Parameter Terpisah**
```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=kasir_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=kasir_db
```

#### Fitur Database
- ✅ Connection pooling otomatis
- ✅ Health checks (pool_pre_ping)
- ✅ Connection recycling setiap 1 jam
- ✅ Fallback ke SQLite untuk development
- ✅ Dukungan untuk MySQL dan SQLite

### 2. Update Menu dari Solaria

Menu aplikasi telah diupdate dengan **menu asli Solaria** yang diambil dari PDF:
- 📄 File: `halaman 2 menu solaria_260129_224254.pdf`
- 🍽️ Total: **54 item menu**
- 💰 Harga: Rp 3.000 - Rp 45.000

#### Kategori Menu (7 kategori):

1. **Nasi Goreng** - 8 items
   - Nasi Goreng Mlarat (Rp 20.000)
   - Nasi Goreng Spesial (Rp 22.000)
   - Nasi Goreng Cabe Ijo (Rp 22.000)
   - Nasi Goreng Sosis (Rp 23.000)
   - Nasi Goreng Modern Warno (Rp 24.000)
   - Nasi Goreng Terimaskenthir (Rp 25.000)
   - Nasi Goreng Pete (Rp 25.000)
   - Nasi Goreng Seafood (Rp 28.000)

2. **Mie** - 6 items
   - Mie Goreng/Siram Ayam (Rp 22.000)
   - Mie Goreng/Siram Seafood (Rp 28.000)
   - Mie Goreng/Siram Sapi (Rp 30.000)

3. **Kwetiau** - 6 items
   - Kwetiau Goreng/Siram Ayam (Rp 25.000)
   - Kwetiau Goreng/Siram Seafood (Rp 28.000)
   - Kwetiau Goreng/Siram Sapi (Rp 30.000)

4. **Snack** - 6 items
   - Fish Cake (Rp 12.000)
   - Kentang Goreng (Rp 15.000)
   - Otak Otak (Rp 15.000)
   - Sosis Goreng/Bakar (Rp 15.000)
   - Mix OTP (Rp 20.000)

5. **Menu Lain** - 6 items
   - Cap Cay Goreng Ayam (Rp 23.000)
   - Cap Cay Goreng Seafood (Rp 28.000)
   - Sapo Tahu Ayam (Rp 27.000)
   - Sapo Tahu Seafood (Rp 30.000)
   - Nasi Putih (Rp 5.000)
   - Telur Mata Sapi/Dadar (Rp 5.000)

6. **Paket** - 8 items (Paket lengkap dengan minuman)
   - Nasi Goreng Cabe Ijo + Teh (Rp 25.000)
   - Kwetiau Ayam Goreng + Teh (Rp 28.000)
   - Nasi Goreng Spesial + Lemon Tea (Rp 33.000)
   - Kwetiau Ayam Goreng + Thai Tea (Rp 35.000)
   - 2 Thai Tea + Kentang Goreng (Rp 38.000)
   - 2 Cappucino + Mix OTP (Rp 45.000)
   - Nasi + Capcay + Blackcurant (Rp 45.000)
   - Nasi + Sapo Tahu + Lemonade (Rp 45.000)

7. **Minuman** - 14 items
   - Teh Mlarat (Rp 3.000)
   - Teh Manis (Rp 5.000)
   - Air Mineral (Rp 5.000)
   - Kopi Hitam (Rp 6.000)
   - Green Tea (Rp 13.000)
   - Thai Tea, Milo, Cappucino, Lemon Tea, dll. (Rp 15.000)

## 🔧 File yang Dimodifikasi

1. **requirements.txt**
   - ➕ pymysql==1.1.0
   - ➕ cryptography==41.0.7

2. **config.py**
   - ➕ Support MySQL connection string
   - ➕ Support individual MySQL parameters
   - ➕ Connection pooling configuration
   - ➕ Auto-fallback ke SQLite

3. **.env.example**
   - ➕ MySQL configuration template
   - ➕ Connection string examples
   - ➕ Individual parameter examples

4. **data/sample_products.py**
   - 🔄 Completely replaced dengan menu Solaria (54 items)
   - ✅ Original item codes dari PDF (111, 121, 131, dst.)
   - ✅ Harga sesuai menu asli
   - ✅ 7 kategori menu

5. **README.md**
   - ➕ Section "Database Configuration"
   - ➕ MySQL installation guide
   - ➕ Database setup instructions
   - ➕ Section "Menu Solaria"
   - 🔄 Updated installation steps

## 📦 Dependencies Baru

```txt
pymysql==1.1.0          # MySQL connector untuk Python
cryptography==41.0.7    # Required oleh pymysql untuk secure connections
```

## 🚀 Cara Setup MySQL

### 1. Install MySQL Server

**Windows:**
```bash
# Download dari https://dev.mysql.com/downloads/mysql/
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install mysql-server
```

**macOS:**
```bash
brew install mysql
```

### 2. Buat Database dan User

```sql
# Login ke MySQL
mysql -u root -p

# Buat database
CREATE DATABASE kasir_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Buat user (optional, untuk keamanan)
CREATE USER 'kasir_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON kasir_db.* TO 'kasir_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Konfigurasi Environment

Edit file `.env`:

```env
# MySQL Configuration
DATABASE_URL=mysql+pymysql://kasir_user:your_secure_password@localhost:3306/kasir_db

# Atau gunakan parameter terpisah:
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=kasir_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=kasir_db
```

### 4. Jalankan Aplikasi

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi (akan otomatis create tables dan import menu)
python app.py
```

## ✅ Testing

```bash
# Test konfigurasi
python -c "from config import Config; print(Config.SQLALCHEMY_DATABASE_URI)"

# Test menu loading
python -c "from data.sample_products import FOOD_MENU; print(f'Total menu: {len(FOOD_MENU)}')"

# Test database connection
python app.py
```

## 📝 Catatan Penting

1. **SQLite Fallback**: Jika MySQL tidak dikonfigurasi, aplikasi akan otomatis menggunakan SQLite
2. **Menu IDs**: Menggunakan ID asli dari menu Solaria (111, 121, 131, dst.)
3. **Security**: Gunakan password yang kuat untuk MySQL user
4. **Backup**: Lakukan backup database secara berkala
5. **Production**: Gunakan MySQL untuk production, SQLite hanya untuk development

## 🎯 Keuntungan MySQL

✅ **Performance**: Lebih cepat untuk concurrent users
✅ **Scalability**: Mudah di-scale untuk pertumbuhan bisnis
✅ **Reliability**: ACID compliance, transactions support
✅ **Features**: Full-text search, stored procedures, triggers
✅ **Backup**: Tools backup yang mature dan reliable

## 📞 Support

Jika ada masalah dengan setup database atau menu:
1. Check error logs di terminal
2. Verify MySQL service is running
3. Check database credentials di .env
4. Ensure database kasir_db sudah dibuat
5. Check koneksi: `mysql -u kasir_user -p kasir_db`

---

**Tanggal Update**: 30 Januari 2026
**Versi**: 2.0.0
**Status**: ✅ Tested & Working
