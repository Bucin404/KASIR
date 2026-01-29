# KASIR Android - Complete POS Application

## Deskripsi Aplikasi
Aplikasi kasir modern berbasis Android dengan fitur lengkap untuk manajemen Point of Sale (POS), keuangan, dan pelaporan.

## Fitur Utama

### 1. **Menu & Katalog Produk**
- 24 item menu dalam 3 kategori (Makanan, Minuman, Dessert)
- Tampilan grid dengan gambar produk
- Badge "Popular" untuk item terlaris
- Harga dalam Rupiah
- Deskripsi produk

### 2. **Keranjang Belanja**
- Tambah/kurang jumlah item
- Hapus item dari keranjang
- Perhitungan otomatis:
  - Subtotal
  - Pajak (10%)
  - Total
- Tampilan real-time

### 3. **Transaksi & Checkout**
- Input pembayaran
- Perhitungan kembalian
- Generate ID transaksi (TRXyyyyMMddHHmmss)
- Simpan riwayat transaksi
- Cetak struk (Bluetooth)

### 4. **Autentikasi & Manajemen User**
- Login dengan username & password
- 3 role: Admin, Manager, Cashier
- Enkripsi password (BCrypt)
- Session management

### 5. **Manajemen Keuangan**
- Tracking pengeluaran dengan 8 kategori:
  - Bahan Baku
  - Gaji Karyawan  
  - Listrik & Air
  - Sewa Tempat
  - Transportasi
  - Pemasaran
  - Peralatan
  - Lain-lain
- Dashboard keuangan:
  - Total pendapatan
  - Total pengeluaran
  - Laba bersih
  - Margin laba (%)
- Grafik cash flow
- Analisis profit

### 6. **Laporan & Export**
- Filter periode (harian, mingguan, bulanan, custom)
- Export ke Excel (Apache POI)
- Export ke PDF (iText)
- Laporan meliputi:
  - Ringkasan keuangan
  - Detail transaksi
  - Top 10 produk terlaris
  - Breakdown pengeluaran
  - Grafik pendapatan harian

### 7. **Bluetooth Printing**
- Scan printer Bluetooth
- Connect/disconnect printer
- Format struk ESC/POS
- Cetak otomatis setelah transaksi

### 8. **Statistik & Dashboard**
- Transaksi hari ini
- Pendapatan hari ini
- Rata-rata transaksi
- Produk terlaris
- Grafik penjualan

## Desain UI

### Tema: Blue-Green Modern Premium
**Warna Utama:**
- Primary: #3498DB (Blue)
- Secondary: #2ECC71 (Green)
- Accent: #1ABC9C (Turquoise)
- Background: #0C141C (Dark)
- Surface: #1A252F, #2C3E50

**Typography:**
- Poppins (Heading)
- Inter (Body)

**Style:**
- Material Design 3
- Dark theme
- Glassmorphism effects
- Smooth animations
- Neon accents
- Modern gradients

## Teknologi

### Core
- Kotlin
- Jetpack Compose
- Material Design 3
- Coroutines & Flow

### Database
- Room (SQLite)
- DataStore (Preferences)

### Libraries
- Navigation Compose
- ViewModel & LiveData
- Apache POI (Excel)
- iText7 (PDF)
- Bluetooth API
- MPAndroidChart (Charts)

## Struktur Database

### Tabel Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT,
    password_hash TEXT,
    role TEXT,
    created_at INTEGER
)
```

### Tabel MenuItems
```sql
CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER,
    category TEXT,
    image_url TEXT,
    description TEXT,
    is_popular INTEGER
)
```

### Tabel Transactions
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    transaction_id TEXT UNIQUE,
    date TEXT,
    date_iso TEXT,
    subtotal INTEGER,
    tax INTEGER,
    total INTEGER,
    payment INTEGER,
    change_amount INTEGER,
    cashier TEXT,
    user_id INTEGER
)
```

### Tabel TransactionItems
```sql
CREATE TABLE transaction_items (
    id INTEGER PRIMARY KEY,
    transaction_id INTEGER,
    item_id INTEGER,
    item_name TEXT,
    price INTEGER,
    quantity INTEGER
)
```

### Tabel Expenses
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    category TEXT,
    amount INTEGER,
    description TEXT,
    date TEXT,
    user_id INTEGER,
    created_at INTEGER
)
```

## Setup & Installation

### Prerequisites
- Android Studio Hedgehog | 2023.1.1 atau lebih baru
- Min SDK: 24 (Android 7.0)
- Target SDK: 34 (Android 14)
- Kotlin 1.9.22
- Gradle 8.2

### Build
```bash
./gradlew build
```

### Run
```bash
./gradlew installDebug
```

## Default Credentials
- **Username**: admin
- **Password**: admin123
- **Role**: Admin

## Permissions
```xml
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

## Screenshots
(Akan ditambahkan setelah build)

## Menu Items (24 Items)

### Makanan (8 items)
1. Nasi Goreng Spesial - Rp 25.000
2. Mie Ayam Bakso - Rp 20.000
3. Ayam Goreng Crispy - Rp 18.000
4. Sate Ayam (10 tusuk) - Rp 22.000
5. Nasi Campur Komplit - Rp 22.000
6. Rendang Daging Sapi - Rp 30.000
7. Soto Ayam Lamongan - Rp 22.000
8. Gado-gado - Rp 18.000

### Minuman (8 items)
9. Es Teh Manis - Rp 5.000
10. Jus Alpukat - Rp 15.000
11. Kopi Latte - Rp 18.000
12. Air Mineral - Rp 4.000
13. Es Jeruk Segar - Rp 8.000
14. Milkshake Coklat - Rp 20.000
15. Matcha Latte - Rp 22.000
16. Boba Milk Tea - Rp 18.000

### Dessert (8 items)
17. Brownies Coklat - Rp 12.000
18. Pisang Goreng - Rp 8.000
19. Donat Gula - Rp 7.000
20. Puding Coklat - Rp 10.000
21. Es Krim Vanilla - Rp 15.000
22. Cheesecake Berry - Rp 25.000
23. Tiramisu - Rp 22.000
24. Waffle Madu - Rp 18.000

## Integrasi ke KASIR-KOTLIN

File-file yang disediakan sudah siap untuk diintegrasikan ke repository KASIR-KOTLIN:

1. Copy folder `app/src/main/java/com/kasir/` ke KASIR-KOTLIN
2. Merge `app/build.gradle.kts` dependencies
3. Copy resource files di `app/src/main/res/`
4. Update `AndroidManifest.xml`
5. Sync Gradle

## Lisensi
MIT License

## Author
KASIR Modern Team

---
**Dibuat dengan ❤️ menggunakan Kotlin & Jetpack Compose**
