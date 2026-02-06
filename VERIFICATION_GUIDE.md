# 🔍 PANDUAN VERIFIKASI - KASIR Modern v3.0

## Cara Memverifikasi Semua Fitur Sudah Berfungsi

### 1. Login ke Aplikasi

```bash
# Jalankan aplikasi
python app.py

# Buka browser
http://localhost:8000
```

**Default Users:**
- Admin: `admin` / `admin123`
- Kasir: `kasir1` / `kasir123`
- Pemilik: `pemilik` / `pemilik123`

---

### 2. Cek Sidebar Menu

Setelah login, sidebar HARUS menampilkan menu sesuai role:

**Untuk Admin:**
```
📊 Dashboard
👥 Kelola User
💵 POS Kasir
🛒 Pesanan Online
💰 Dashboard (Finance)
📝 Catatan Keuangan
📊 Laporan
```

**Untuk Kasir:**
```
💵 POS Kasir
🛒 Pesanan Online
```

**Untuk Pemilik:**
```
💰 Dashboard
📝 Catatan Keuangan
📊 Laporan
```

**Jika sidebar kosong:**
- Logout dan login kembali
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)

---

### 3. Cek Halaman POS Kasir

1. Klik menu **"POS Kasir"** di sidebar
2. Halaman harus menampilkan:
   - ✅ Search box di atas
   - ✅ Category pills (Semua, Nasi Goreng, Mie, dll)
   - ✅ Product grid (54 items)
   - ✅ Cart sidebar di kanan
   - ✅ Payment section
   - ✅ Checkout & Clear buttons

---

### 4. Test Add to Cart

1. **Klik salah satu product card**
2. Product harus langsung masuk ke cart
3. Cart harus menampilkan:
   - Nama product
   - Harga per item
   - Quantity controls (+ dan -)
   - Remove button (🗑️)

**Jika tidak bisa klik:**
- Buka Console (F12)
- Lihat error messages
- Type: `console.log(products)` untuk cek data
- Pastikan products array tidak kosong

---

### 5. Test Cart Functions

**Increase Quantity:**
- Klik button **"+"** → Qty bertambah ✅

**Decrease Quantity:**
- Klik button **"-"** → Qty berkurang ✅

**Remove Item:**
- Klik button **"🗑️"** → Item terhapus ✅

**Subtotal/Tax/Total:**
- Harus auto-calculate ✅

---

### 6. Test Payment & Change

1. Input jumlah **"Bayar"** (misal: 100000)
2. **Kembalian** harus auto-calculate
3. Contoh:
   ```
   Subtotal: Rp 50,000
   Pajak 10%: Rp 5,000
   Total: Rp 55,000
   
   Bayar: Rp 100,000
   Kembalian: Rp 45,000 ✅
   ```

---

### 7. Test Checkout

1. Klik button **"Checkout"**
2. Alert muncul dengan detail transaksi
3. Cart harus kosong setelah confirm

---

## 🐛 Troubleshooting

### Problem 1: Sidebar Kosong
**Cause**: Session tidak ada
**Solution**:
```
1. Logout
2. Login kembali dengan user yang benar
3. Hard refresh (Ctrl+Shift+R)
```

### Problem 2: Product Tidak Bisa Diklik
**Cause**: JavaScript error
**Solution**:
```
1. Open Console (F12)
2. Look for errors in red
3. Check if products array exists
4. Try different browser
```

### Problem 3: Cart Tidak Muncul
**Cause**: CSS issue or grid problem
**Solution**:
```
1. Hard refresh (Ctrl+Shift+R)
2. Clear cache
3. Check browser zoom (should be 100%)
4. Try responsive view (Ctrl+Shift+M)
```

### Problem 4: Kembalian Tidak Muncul
**Cause**: Payment input kosong
**Solution**:
```
1. Input jumlah bayar yang lebih besar dari total
2. Kembalian akan auto-calculate
3. Jika masih tidak muncul, check console
```

---

## 📝 Checklist Verifikasi

Gunakan checklist ini untuk memastikan semua fitur berfungsi:

### Login & Sidebar
- [ ] Login berhasil
- [ ] Sidebar muncul
- [ ] Menu links tampil sesuai role
- [ ] Logout button ada

### POS Kasir Page
- [ ] Search box visible
- [ ] Category filters visible
- [ ] Product grid tampil (54 items)
- [ ] Cart section tampil di kanan
- [ ] Product cards clickable

### Cart Functions
- [ ] Klik product → masuk cart
- [ ] Quantity + button works
- [ ] Quantity - button works
- [ ] Remove item works
- [ ] Cart empty state shows

### Calculations
- [ ] Subtotal calculated
- [ ] Tax 10% calculated
- [ ] Total calculated
- [ ] Payment input works
- [ ] Change calculated
- [ ] Checkout works

### Responsive
- [ ] Desktop view (>992px) OK
- [ ] Tablet view (768-992px) OK
- [ ] Mobile view (<768px) OK

---

## 📞 Support

Jika masih ada masalah setelah verifikasi:

1. **Check Browser**: Chrome/Firefox/Safari latest version
2. **Check Python**: Version 3.8+
3. **Check Dependencies**: `pip install -r requirements.txt`
4. **Check Database**: Delete `kasir.db` and restart
5. **Check Logs**: Console output for errors

---

**Version**: 3.0.0
**Last Updated**: 2026-01-30
**Status**: Production Ready ✅
