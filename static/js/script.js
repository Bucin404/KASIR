// ============================================
// KASIR MODERN - ENHANCED SCRIPT
// ============================================

// Global State
let cart = [];
let menuItems = [];
let selectedCategory = 'all';
let cartHistory = [];
let orderHolds = [];
let discount = 0;
let currentPaymentMethod = 'cash';
let sessionStartTime = new Date();
let searchTimeout = null;

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Kasir Modern...');
    
    // Initialize with animations
    initAnimations();
    
    // Setup all event listeners
    setupEventListeners();
    
    // Load data
    loadInitialData();
    
    // Start background services
    startBackgroundServices();
    
    // Show welcome notification
    showNotification('Selamat datang di Kasir Modern!', 'Sistem siap digunakan', 'success');
});

// Initialize animations and effects
function initAnimations() {
    // Add page transition
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
    
    // Add hover effects to interactive elements
    document.querySelectorAll('button, .menu-item, .cart-item').forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.2s ease';
        });
    });
    
    // Create floating particles
    createFloatingParticles();
}

// Setup all event listeners
function setupEventListeners() {
    // Category buttons
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', handleCategoryClick);
    });
    
    // Payment buttons
    document.getElementById('payBtn').addEventListener('click', processPayment);
    document.getElementById('clearBtn').addEventListener('click', clearCart);
    document.getElementById('holdBtn').addEventListener('click', holdOrder);
    
    // Modal buttons
    document.getElementById('printStruk').addEventListener('click', printStruk);
    document.getElementById('closeStruk').addEventListener('click', closeStruk);
    document.getElementById('newTransaction').addEventListener('click', newTransaction);
    
    // Payment input
    const paymentInput = document.getElementById('paymentAmount');
    paymentInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            processPayment();
        }
    });
    
    paymentInput.addEventListener('focus', function() {
        this.select();
        this.style.transform = 'scale(1.02)';
        this.style.boxShadow = '0 8px 30px rgba(0, 198, 255, 0.4)';
    });
    
    paymentInput.addEventListener('blur', function() {
        this.style.transform = 'scale(1)';
        this.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.2)';
        if (this.value === '') this.value = '0';
    });
    
    // Search functionality
    document.getElementById('searchMenu').addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchMenu(this.value);
        }, 300);
    });
    
    // Drag and drop setup
    setupDragAndDrop();
    
    // Keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Window events
    window.addEventListener('resize', handleResize);
    window.addEventListener('beforeunload', handleBeforeUnload);
}

// Load initial data
async function loadInitialData() {
    try {
        showLoading('Memuat menu...');
        
        // Load menu
        const menuResponse = await fetch('/api/menu');
        menuItems = await menuResponse.json();
        
        // Load stats
        await loadTodayStats();
        
        // Load recent transactions
        await loadRecentTransactions();
        
        // Render menu
        renderMenu(menuItems);
        
        // Check for saved cart
        checkSavedCart();
        
        hideLoading();
        
        // Animate menu items
        setTimeout(animateMenuItems, 300);
        
    } catch (error) {
        console.error('Error loading initial data:', error);
        showNotification('Gagal memuat data', 'Periksa koneksi internet', 'error');
        hideLoading();
    }
}

// Start background services
function startBackgroundServices() {
    // Auto-save cart every 2 minutes
    setInterval(autoSaveCart, 120000);
    
    // Update time every second
    updateClock();
    setInterval(updateClock, 1000);
    
    // Update stats every 30 seconds
    setInterval(loadTodayStats, 30000);
    
    // Auto-hide notifications after 5 seconds
    setInterval(checkNotifications, 1000);
}

// ============================================
// MENU FUNCTIONS
// ============================================

// Render menu with animations
function renderMenu(items) {
    const menuGrid = document.getElementById('menuGrid');
    if (!menuGrid) return;
    
    if (items.length === 0) {
        menuGrid.innerHTML = `
            <div class="empty-menu">
                <i class="fas fa-utensils"></i>
                <h3>Tidak ada item menu</h3>
                <p>Silakan coba lagi nanti</p>
            </div>
        `;
        return;
    }
    
    menuGrid.innerHTML = '';
    
    items.forEach((item, index) => {
        const menuItem = document.createElement('div');
        menuItem.className = 'menu-item';
        menuItem.dataset.id = item.id;
        menuItem.dataset.category = item.category;
        menuItem.style.animationDelay = `${index * 0.05}s`;
        
        // Create menu item HTML
        menuItem.innerHTML = `
            <div class="menu-item-header">
                <span class="menu-item-category">${item.category}</span>
                ${item.popular ? '<div class="menu-item-popular"><i class="fas fa-star"></i></div>' : ''}
            </div>
            <img src="${item.image}" alt="${item.name}" class="menu-item-image" loading="lazy">
            <div class="menu-item-content">
                <h3 class="menu-item-name">${item.name}</h3>
                <p class="menu-item-description">${item.description || ''}</p>
                <div class="menu-item-price">Rp ${formatNumber(item.price)}</div>
                <div class="menu-item-actions">
                    <div class="quantity-control">
                        <button class="qty-btn minus" data-id="${item.id}" aria-label="Kurangi">
                            <i class="fas fa-minus"></i>
                        </button>
                        <span class="qty-display" id="qty-${item.id}">0</span>
                        <button class="qty-btn plus" data-id="${item.id}" aria-label="Tambah">
                            <i class="fas fa-plus"></i>
                        </button>
                    </div>
                    <button class="add-btn" data-id="${item.id}">
                        <i class="fas fa-cart-plus"></i>
                        <span>Tambah</span>
                    </button>
                </div>
            </div>
        `;
        
        menuGrid.appendChild(menuItem);
    });
    
    // Add event listeners
    setTimeout(() => {
        document.querySelectorAll('.qty-btn.minus').forEach(btn => {
            btn.addEventListener('click', function(e) {
                const itemId = parseInt(this.dataset.id);
                changeQuantity(itemId, -1);
            });
        });
        
        document.querySelectorAll('.qty-btn.plus').forEach(btn => {
            btn.addEventListener('click', function(e) {
                const itemId = parseInt(this.dataset.id);
                changeQuantity(itemId, 1);
            });
        });
        
        document.querySelectorAll('.add-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                const itemId = parseInt(this.dataset.id);
                addToCart(itemId);
            });
        });
        
        // Add click event to menu items for quick add
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('dblclick', function() {
                const itemId = parseInt(this.dataset.id);
                quickAddToCart(itemId);
            });
            
            item.addEventListener('click', function(e) {
                if (!e.target.closest('.qty-btn') && !e.target.closest('.add-btn')) {
                    const itemId = parseInt(this.dataset.id);
                    showItemDetail(itemId);
                }
            });
        });
    }, 100);
}

// Animate menu items on load
function animateMenuItems() {
    const items = document.querySelectorAll('.menu-item');
    items.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0) scale(1)';
        }, index * 50);
    });
}

// Handle category filter
function handleCategoryClick(e) {
    const category = this.dataset.category;
    selectedCategory = category;
    
    // Update active button
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    this.classList.add('active');
    
    // Update filter info
    const filterInfo = document.getElementById('filterInfo');
    if (filterInfo) {
        filterInfo.textContent = category === 'all' ? 'Semua kategori' : category;
    }
    
    // Filter menu
    filterMenu(category);
}

// Filter menu by category
function filterMenu(category) {
    const filtered = category === 'all' 
        ? menuItems 
        : menuItems.filter(item => item.category === category);
    
    renderMenu(filtered);
    animateMenuItems();
}

// Search menu items
function searchMenu(query) {
    if (!query.trim()) {
        filterMenu(selectedCategory);
        return;
    }
    
    const searchTerm = query.toLowerCase();
    const filtered = menuItems.filter(item => 
        item.name.toLowerCase().includes(searchTerm) ||
        item.description?.toLowerCase().includes(searchTerm) ||
        item.category.toLowerCase().includes(searchTerm)
    );
    
    renderMenu(filtered);
    animateMenuItems();
    
    // Update menu count
    const menuCount = document.getElementById('menuCount');
    if (menuCount) {
        menuCount.textContent = `${filtered.length} items ditemukan`;
    }
}

// Show popular items
function showPopularItems() {
    const popular = menuItems.filter(item => item.popular);
    renderMenu(popular);
    animateMenuItems();
    
    // Update UI
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const menuCount = document.getElementById('menuCount');
    if (menuCount) {
        menuCount.textContent = `${popular.length} items populer`;
    }
    
    const filterInfo = document.getElementById('filterInfo');
    if (filterInfo) {
        filterInfo.textContent = 'Menu Populer';
    }
}

// Show all items
function showAllItems() {
    selectedCategory = 'all';
    filterMenu('all');
    
    // Update UI
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.category === 'all') {
            btn.classList.add('active');
        }
    });
}

// Change quantity
function changeQuantity(itemId, change) {
    const qtyElement = document.getElementById(`qty-${itemId}`);
    if (!qtyElement) return;
    
    let currentQty = parseInt(qtyElement.textContent) || 0;
    const newQty = Math.max(0, currentQty + change);
    
    // Animate the change
    qtyElement.style.transform = 'scale(1.2)';
    qtyElement.style.color = change > 0 ? 'var(--secondary)' : 'var(--danger)';
    
    setTimeout(() => {
        qtyElement.style.transition = 'all 0.2s ease';
        qtyElement.style.transform = 'scale(1)';
        qtyElement.style.color = 'var(--light)';
    }, 200);
    
    qtyElement.textContent = newQty;
    
    // Play sound
    playSound('click');
}

// Add to cart with animation
function addToCart(itemId) {
    const qtyElement = document.getElementById(`qty-${itemId}`);
    if (!qtyElement) return;
    
    const quantity = parseInt(qtyElement.textContent) || 0;
    
    if (quantity === 0) {
        showNotification('Pilih jumlah terlebih dahulu', 'Klik tombol + untuk menambah jumlah', 'warning');
        return;
    }
    
    const menuItem = menuItems.find(item => item.id === itemId);
    if (!menuItem) return;
    
    const existingItem = cart.find(item => item.id === itemId);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: menuItem.id,
            name: menuItem.name,
            price: menuItem.price,
            quantity: quantity,
            category: menuItem.category
        });
    }
    
    // Reset quantity with animation
    qtyElement.style.transform = 'rotate(360deg) scale(0)';
    qtyElement.style.opacity = '0';
    setTimeout(() => {
        qtyElement.textContent = '0';
        qtyElement.style.transition = 'all 0.3s ease';
        qtyElement.style.transform = 'rotate(0deg) scale(1)';
        qtyElement.style.opacity = '1';
    }, 300);
    
    updateCart();
    
    // Show flying animation
    showFlyingItem(menuItem);
    
    // Show notification
    showNotification('Berhasil ditambahkan', `${menuItem.name} (${quantity}x)`, 'success');
    
    // Play sound
    playSound('add');
}

// Quick add to cart (double click)
function quickAddToCart(itemId) {
    const menuItem = menuItems.find(item => item.id === itemId);
    if (!menuItem) return;
    
    const existingItem = cart.find(item => item.id === itemId);
    const quantity = existingItem ? 1 : 1;
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: menuItem.id,
            name: menuItem.name,
            price: menuItem.price,
            quantity: quantity,
            category: menuItem.category
        });
    }
    
    updateCart();
    showFlyingItem(menuItem);
    showNotification('Quick Add', `${menuItem.name} (+1)`, 'info');
    playSound('add');
}

// Show item detail
function showItemDetail(itemId) {
    const menuItem = menuItems.find(item => item.id === itemId);
    if (!menuItem) return;
    
    const modal = document.getElementById('itemDetailModal');
    const content = document.getElementById('itemDetailContent');
    const title = document.getElementById('detailTitle');
    
    title.textContent = menuItem.name;
    
    content.innerHTML = `
        <div class="item-detail">
            <img src="${menuItem.image}" alt="${menuItem.name}" class="detail-image">
            <div class="detail-content">
                <div class="detail-category">${menuItem.category}</div>
                <h3 class="detail-name">${menuItem.name}</h3>
                <p class="detail-description">${menuItem.description || 'Tidak ada deskripsi'}</p>
                <div class="detail-price">Rp ${formatNumber(menuItem.price)}</div>
                <div class="detail-actions">
                    <button class="detail-btn add" onclick="quickAddToCart(${itemId}); closeItemDetail()">
                        <i class="fas fa-cart-plus"></i>
                        Tambah ke Keranjang
                    </button>
                    <button class="detail-btn close" onclick="closeItemDetail()">
                        <i class="fas fa-times"></i>
                        Tutup
                    </button>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

// Close item detail
function closeItemDetail() {
    const modal = document.getElementById('itemDetailModal');
    modal.style.display = 'none';
}

// ============================================
// CART FUNCTIONS
// ============================================

// Update cart display
function updateCart() {
    updateCartDisplay();
    updateCartSummary();
    updateQuickActions();
    updateMobileBadge();
    saveCartToLocal();
    
    // Update cart history
    if (cart.length > 0) {
        cartHistory.push({
            timestamp: new Date(),
            items: [...cart],
            total: calculateTotal()
        });
        
        // Keep only last 10 entries
        if (cartHistory.length > 10) {
            cartHistory.shift();
        }
    }
}

// Update cart display
function updateCartDisplay() {
    const cartContainer = document.getElementById('cartItemsContainer');
    const cartItems = document.getElementById('cartItems');
    const emptyState = document.getElementById('cartEmptyState');
    const cartCount = document.getElementById('cartCount');
    const mobileCartBadge = document.getElementById('mobileCartBadge');
    
    if (cart.length === 0) {
        cartContainer.classList.remove('has-items');
        cartItems.innerHTML = '';
        
        // Animate cart count
        if (cartCount) {
            cartCount.style.transform = 'scale(1.4)';
            setTimeout(() => {
                cartCount.style.transition = 'transform 0.3s ease';
                cartCount.style.transform = 'scale(1)';
            }, 300);
            cartCount.textContent = '0';
        }
        
        if (mobileCartBadge) {
            mobileCartBadge.textContent = '0';
        }
        
        return;
    }
    
    cartContainer.classList.add('has-items');
    
    // Update cart count with animation
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    animateNumberChange(cartCount, totalItems, true);
    if (mobileCartBadge) {
        mobileCartBadge.textContent = totalItems;
    }
    
    // Render cart items
    cartItems.innerHTML = '';
    
    cart.forEach((item, index) => {
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.style.animationDelay = `${index * 0.05}s`;
        
        const itemTotal = item.price * item.quantity;
        
        cartItem.innerHTML = `
            <div class="cart-item-header">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">Rp ${formatNumber(item.price)}</div>
            </div>
            <div class="cart-item-body">
                <div class="cart-item-quantity">
                    <button class="cart-qty-btn minus" data-id="${item.id}" aria-label="Kurangi">
                        <i class="fas fa-minus"></i>
                    </button>
                    <div class="quantity-display">${item.quantity}</div>
                    <button class="cart-qty-btn plus" data-id="${item.id}" aria-label="Tambah">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
                <div class="cart-item-total">Rp ${formatNumber(itemTotal)}</div>
            </div>
            <div class="cart-item-actions">
                <button class="remove-btn" data-id="${item.id}" aria-label="Hapus">
                    <i class="fas fa-trash"></i>
                    <span>Hapus</span>
                </button>
            </div>
        `;
        
        cartItems.appendChild(cartItem);
    });
    
    // Add event listeners
    setTimeout(() => {
        document.querySelectorAll('.cart-qty-btn.minus').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = parseInt(this.dataset.id);
                updateCartItem(itemId, -1);
            });
        });
        
        document.querySelectorAll('.cart-qty-btn.plus').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = parseInt(this.dataset.id);
                updateCartItem(itemId, 1);
            });
        });
        
        document.querySelectorAll('.remove-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const itemId = parseInt(this.dataset.id);
                removeFromCart(itemId);
            });
        });
    }, 50);
}

// Update cart summary
function updateCartSummary() {
    const subtotal = calculateSubtotal();
    const tax = Math.round(subtotal * 0.10);
    const total = subtotal + tax - discount;
    
    // Update summary elements
    const subtotalElement = document.getElementById('subtotal');
    const taxElement = document.getElementById('tax');
    const totalElement = document.getElementById('total');
    const itemCountElement = document.getElementById('itemCount');
    const uniqueItemsElement = document.getElementById('uniqueItems');
    
    if (subtotalElement) animateNumberChange(subtotalElement, `Rp ${formatNumber(subtotal)}`);
    if (taxElement) animateNumberChange(taxElement, `Rp ${formatNumber(tax)}`);
    if (totalElement) animateNumberChange(totalElement, `Rp ${formatNumber(total)}`);
    
    if (itemCountElement) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        animateNumberChange(itemCountElement, totalItems, true);
    }
    
    if (uniqueItemsElement) {
        animateNumberChange(uniqueItemsElement, cart.length, true);
    }
}

// Update quick actions visibility
function updateQuickActions() {
    const quickActions = document.getElementById('cartQuickActions');
    if (quickActions) {
        quickActions.style.display = cart.length > 0 ? 'flex' : 'none';
    }
}

// Update mobile badge
function updateMobileBadge() {
    const badge = document.getElementById('mobileCartBadge');
    if (badge) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = totalItems;
        
        // Animate badge on update
        if (totalItems > 0) {
            badge.style.transform = 'scale(1.3)';
            setTimeout(() => {
                badge.style.transition = 'transform 0.2s ease';
                badge.style.transform = 'scale(1)';
            }, 200);
        }
    }
}

// Update cart item quantity
function updateCartItem(itemId, change) {
    const item = cart.find(item => item.id === itemId);
    if (!item) return;
    
    item.quantity += change;
    
    if (item.quantity <= 0) {
        removeFromCart(itemId);
    } else {
        updateCart();
        showNotification(`Diperbarui`, `${item.name}: ${item.quantity}x`, 'info');
        playSound('click');
    }
}

// Remove item from cart
function removeFromCart(itemId) {
    const item = cart.find(item => item.id === itemId);
    if (!item) return;
    
    cart = cart.filter(item => item.id !== itemId);
    updateCart();
    
    showNotification('Dihapus', `${item.name} dihapus dari keranjang`, 'warning');
    playSound('remove');
}

// Clear cart
function clearCart() {
    if (cart.length === 0) {
        showNotification('Keranjang sudah kosong', 'Tambahkan item terlebih dahulu', 'info');
        return;
    }
    
    if (confirm('Yakin ingin mengosongkan keranjang?')) {
        const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);
        cart = [];
        updateCart();
        
        showNotification('Keranjang dikosongkan', `${itemCount} item dihapus`, 'success');
        playSound('remove');
    }
}

// Hold order
function holdOrder() {
    if (cart.length === 0) {
        showNotification('Keranjang kosong', 'Tambahkan item untuk ditahan', 'warning');
        return;
    }
    
    const holdNumber = orderHolds.length + 1;
    orderHolds.push({
        number: holdNumber,
        timestamp: new Date(),
        items: [...cart],
        total: calculateTotal()
    });
    
    const previousCart = [...cart];
    cart = [];
    updateCart();
    
    showNotification(`Pesanan ditahan #${holdNumber}`, 'Pesanan disimpan sementara', 'info');
    
    // Show hold notification with restore option
    showNotification(
        `Pesanan #${holdNumber} ditahan`, 
        'Klik untuk memulihkan', 
        'warning',
        10000,
        () => {
            cart = previousCart;
            updateCart();
            orderHolds = orderHolds.filter(h => h.number !== holdNumber);
            showNotification('Pesanan dipulihkan', `Pesanan #${holdNumber} dikembalikan`, 'success');
        }
    );
}

// Apply discount
function applyDiscount(percent) {
    discount = percent;
    updateCartSummary();
    
    if (percent > 0) {
        showNotification(`Diskon ${percent}% diterapkan`, 'Total telah diperbarui', 'success');
    } else {
        showNotification('Diskon direset', 'Total kembali normal', 'info');
    }
}

// Update all quantities
function updateAllQuantities(change) {
    if (cart.length === 0) return;
    
    cart.forEach(item => {
        item.quantity += change;
        if (item.quantity <= 0) {
            item.quantity = 1; // Keep at least 1
        }
    });
    
    updateCart();
    showNotification(
        change > 0 ? 'Semua ditambah' : 'Semua dikurangi', 
        `Jumlah semua item di${change > 0 ? 'tambah' : 'kurangi'}`, 
        'info'
    );
}

// ============================================
// PAYMENT FUNCTIONS
// ============================================

// Process payment
async function processPayment() {
    if (cart.length === 0) {
        showNotification('Keranjang kosong!', 'Tambahkan item sebelum membayar', 'error');
        return;
    }
    
    const paymentInput = document.getElementById('paymentAmount');
    const payment = parseFloat(paymentInput.value.replace(/\./g, '')) || 0;
    
    if (payment <= 0) {
        showNotification('Masukkan jumlah pembayaran', 'Isi jumlah pembayaran yang valid', 'error');
        paymentInput.focus();
        return;
    }
    
    const total = calculateTotal();
    
    if (payment < total) {
        const kurang = total - payment;
        showNotification(`Pembayaran kurang`, `Rp ${formatNumber(kurang)}`, 'error');
        paymentInput.focus();
        return;
    }
    
    try {
        showLoading('Memproses pembayaran...');
        
        const response = await fetch('/api/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                items: cart,
                payment: payment,
                discount: discount
            })
        });
        
        const strukData = await response.json();
        
        if (strukData.error) {
            throw new Error(strukData.error);
        }
        
        showStruk(strukData);
        
        // Reset after successful payment
        cart = [];
        discount = 0;
        updateCart();
        paymentInput.value = '0';
        
        // Update stats
        await loadTodayStats();
        
        hideLoading();
        
        // Show success notification
        showNotification('Pembayaran berhasil!', 'Transaksi selesai', 'success');
        playSound('checkout');
        
    } catch (error) {
        console.error('Error processing payment:', error);
        showNotification('Gagal memproses pembayaran', error.message || 'Coba lagi', 'error');
        hideLoading();
    }
}

// Show struk
function showStruk(strukData) {
    const modal = document.getElementById('strukModal');
    const strukContent = document.getElementById('strukContent');
    
    if (!modal || !strukContent) return;
    
    let itemsHtml = '';
    strukData.items.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        itemsHtml += `
            <div class="struk-item" style="animation-delay: ${index * 0.1}s">
                <div>
                    <div class="struk-item-name">${item.name}</div>
                    <small class="struk-item-detail">${item.quantity} × Rp ${formatNumber(item.price)}</small>
                </div>
                <div class="struk-item-total">Rp ${formatNumber(itemTotal)}</div>
            </div>
        `;
    });
    
    const change = strukData.change;
    const changeClass = change > 0 ? 'success' : '';
    
    strukContent.innerHTML = `
        <div class="struk-header">
            <div class="struk-id">${strukData.transaction_id}</div>
            <div class="struk-date">${strukData.date}</div>
            <div class="struk-cashier">${strukData.cashier || 'Kasir Utama'}</div>
        </div>
        
        <div class="struk-items">
            ${itemsHtml}
        </div>
        
        <div class="struk-summary">
            <div class="struk-row">
                <span>Subtotal</span>
                <span>Rp ${formatNumber(strukData.subtotal)}</span>
            </div>
            <div class="struk-row">
                <span>Pajak (10%)</span>
                <span>Rp ${formatNumber(strukData.tax)}</span>
            </div>
            ${discount > 0 ? `
                <div class="struk-row discount">
                    <span>Diskon (${discount}%)</span>
                    <span>- Rp ${formatNumber(discount)}</span>
                </div>
            ` : ''}
            <div class="struk-row total">
                <span>TOTAL</span>
                <span>Rp ${formatNumber(strukData.total)}</span>
            </div>
            <div class="struk-row payment">
                <span>Pembayaran</span>
                <span>Rp ${formatNumber(strukData.payment)}</span>
            </div>
            <div class="struk-row change ${changeClass}">
                <span>Kembalian</span>
                <span>Rp ${formatNumber(change)}</span>
            </div>
        </div>
        
        <div class="struk-footer">
            <div class="thank-you">Terima kasih telah berbelanja!</div>
            <div class="footer-note">Barang yang sudah dibeli tidak dapat dikembalikan</div>
        </div>
    `;
    
    modal.style.display = 'flex';
    
    // Animate struk items
    setTimeout(() => {
        const items = strukContent.querySelectorAll('.struk-item');
        items.forEach((item, index) => {
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, index * 50);
        });
    }, 100);
}

// Close struk
function closeStruk() {
    const modal = document.getElementById('strukModal');
    if (modal) {
        modal.style.animation = 'modalFadeIn 0.3s ease reverse';
        setTimeout(() => {
            modal.style.display = 'none';
            modal.style.animation = '';
        }, 300);
    }
}

// Print struk
function printStruk() {
    const printContent = document.getElementById('strukContent');
    if (!printContent) return;
    
    const originalContent = printContent.innerHTML;
    const printWindow = window.open('', '_blank');
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Struk Pembayaran</title>
            <style>
                @media print {
                    @page { 
                        size: 80mm auto; 
                        margin: 0; 
                        padding: 0;
                    }
                    body { 
                        margin: 0; 
                        padding: 10px; 
                        font-family: 'Courier New', monospace;
                        font-size: 12px;
                        max-width: 80mm;
                    }
                }
                body { 
                    margin: 0; 
                    padding: 10px; 
                    font-family: 'Courier New', monospace;
                    font-size: 12px;
                    max-width: 80mm;
                }
                .struk-header { text-align: center; margin-bottom: 15px; }
                .struk-id { font-weight: bold; font-size: 14px; }
                .struk-date, .struk-cashier { font-size: 11px; }
                .struk-item { 
                    display: flex; 
                    justify-content: space-between;
                    margin-bottom: 5px;
                    border-bottom: 1px dashed #ccc;
                    padding-bottom: 5px;
                }
                .struk-item-name { font-weight: bold; }
                .struk-item-detail { color: #666; }
                .struk-summary { margin-top: 15px; }
                .struk-row { 
                    display: flex; 
                    justify-content: space-between;
                    margin-bottom: 5px;
                }
                .struk-row.total { 
                    font-weight: bold; 
                    font-size: 14px;
                    border-top: 2px dashed #000;
                    padding-top: 10px;
                    margin-top: 10px;
                }
                .struk-footer { 
                    text-align: center; 
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px dashed #000;
                }
                .thank-you { font-weight: bold; margin-bottom: 10px; }
                .footer-note { font-size: 10px; color: #666; }
            </style>
        </head>
        <body>
            ${originalContent}
            <script>
                setTimeout(() => {
                    window.print();
                    setTimeout(() => window.close(), 500);
                }, 100);
            </script>
        </body>
        </html>
    `);
    
    printWindow.document.close();
}

// New transaction
function newTransaction() {
    closeStruk();
    showNotification('Transaksi baru', 'Siap untuk transaksi berikutnya', 'info');
}

// Email struk
function emailStruk() {
    showNotification('Fitur dalam pengembangan', 'Fitur email struk akan segera hadir', 'info');
}

// Share struk
function shareStruk() {
    if (navigator.share) {
        navigator.share({
            title: 'Struk Pembayaran Kasir Modern',
            text: 'Lihat struk pembayaran Anda',
            url: window.location.href
        });
    } else {
        showNotification('Sharing tidak didukung', 'Browser Anda tidak mendukung fitur sharing', 'warning');
    }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

// Format payment input
function formatPaymentInput(input) {
    let value = input.value.replace(/[^\d]/g, '');
    if (value === '') {
        input.value = '0';
    } else {
        const num = parseInt(value);
        input.value = formatNumber(num);
    }
}

// Set payment amount
function setPaymentAmount(amount) {
    const paymentInput = document.getElementById('paymentAmount');
    paymentInput.value = formatNumber(amount);
    paymentInput.focus();
}

// Format number with thousands separator
function formatNumber(num) {
    return new Intl.NumberFormat('id-ID').format(num);
}

// Calculate subtotal
function calculateSubtotal() {
    return cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}

// Calculate total with tax and discount
function calculateTotal() {
    const subtotal = calculateSubtotal();
    const tax = Math.round(subtotal * 0.10);
    return subtotal + tax - discount;
}

// Animate number change
function animateNumberChange(element, newValue, isCount = false) {
    if (!element) return;
    
    const oldValue = isCount ? parseInt(element.textContent) || 0 : element.textContent;
    
    if (oldValue !== newValue.toString()) {
        element.classList.add('number-pop');
        element.style.color = 'var(--accent)';
        
        setTimeout(() => {
            element.textContent = newValue;
            element.style.transition = 'all 0.3s ease';
            element.style.color = '';
            element.classList.remove('number-pop');
        }, 150);
    }
}

// Show loading overlay
function showLoading(message = 'Memproses...') {
    const loading = document.getElementById('loading');
    const loadingTitle = document.getElementById('loadingTitle');
    const loadingText = document.getElementById('loadingText');
    
    if (loading) loading.style.display = 'flex';
    if (loadingTitle) loadingTitle.textContent = message;
    if (loadingText) loadingText.textContent = 'Mohon tunggu sebentar';
}

// Hide loading overlay
function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) loading.style.display = 'none';
}

// Show notification
function showNotification(title, message, type = 'info', duration = 5000, onClick = null) {
    const notificationSystem = document.getElementById('notificationSystem');
    if (!notificationSystem) return;
    
    // Remove existing notifications
    const existingNotifications = notificationSystem.querySelectorAll('.notification');
    if (existingNotifications.length >= 5) {
        existingNotifications[0].remove();
    }
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    const icon = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    }[type] || 'fas fa-info-circle';
    
    notification.innerHTML = `
        <div class="notification-icon">
            <i class="${icon}"></i>
        </div>
        <div class="notification-content">
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
        <div class="notification-progress"></div>
    `;
    
    // Add click handler if provided
    if (onClick) {
        notification.style.cursor = 'pointer';
        notification.addEventListener('click', onClick);
    }
    
    notificationSystem.appendChild(notification);
    
    // Add close button handler
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        removeNotification(notification);
    });
    
    // Auto remove after duration
    setTimeout(() => {
        removeNotification(notification);
    }, duration);
}

// Remove notification
function removeNotification(notification) {
    if (notification && notification.parentNode) {
        notification.classList.add('slide-out');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }
}

// Check and clean up old notifications
function checkNotifications() {
    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(notification => {
        const progress = notification.querySelector('.notification-progress');
        if (progress && progress.style.animationPlayState === 'paused') {
            removeNotification(notification);
        }
    });
}

// Play sound
function playSound(type) {
    const audio = document.getElementById(`${type}Sound`);
    if (audio) {
        audio.currentTime = 0;
        audio.play().catch(e => console.log('Audio play failed:', e));
    }
}

// Show flying item animation
function showFlyingItem(item) {
    const cartCount = document.querySelector('.cart-count');
    if (!cartCount) return;
    
    // Find the clicked add button
    const addButton = document.querySelector(`.add-btn[data-id="${item.id}"]`);
    if (!addButton) return;
    
    const startRect = addButton.getBoundingClientRect();
    const endRect = cartCount.getBoundingClientRect();
    
    const flyingItem = document.createElement('div');
    flyingItem.className = 'flying-item';
    flyingItem.innerHTML = `<i class="fas fa-${getIconByCategory(item.category)}"></i>`;
    
    flyingItem.style.cssText = `
        position: fixed;
        left: ${startRect.left + startRect.width / 2}px;
        top: ${startRect.top + startRect.height / 2}px;
        font-size: 1.2rem;
        color: var(--primary);
        z-index: 2000;
        pointer-events: none;
        transform: translate(-50%, -50%);
        transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        filter: drop-shadow(0 0 5px rgba(0, 198, 255, 0.5));
    `;
    
    document.body.appendChild(flyingItem);
    
    // Animate to cart
    requestAnimationFrame(() => {
        flyingItem.style.left = `${endRect.left + endRect.width / 2}px`;
        flyingItem.style.top = `${endRect.top + endRect.height / 2}px`;
        flyingItem.style.transform = 'translate(-50%, -50%) scale(0.5)';
        flyingItem.style.opacity = '0';
    });
    
    // Remove after animation
    setTimeout(() => {
        if (flyingItem.parentNode) {
            flyingItem.remove();
        }
    }, 600);
}

// Get icon by category
function getIconByCategory(category) {
    const icons = {
        'Makanan': 'utensils',
        'Minuman': 'glass-martini-alt',
        'Dessert': 'ice-cream'
    };
    return icons[category] || 'utensils';
}

// Update clock
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('id-ID', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    const dateString = now.toLocaleDateString('id-ID', {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    });
    
    const currentTimeElement = document.getElementById('currentTime');
    if (currentTimeElement) {
        currentTimeElement.textContent = `${dateString} ${timeString}`;
    }
}

// Load today's stats
async function loadTodayStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        // Update UI
        const todayTransactions = document.getElementById('todayTransactions');
        const todayIncome = document.getElementById('todayIncome');
        const avgTransaction = document.getElementById('avgTransaction');
        
        if (todayTransactions) {
            animateNumberChange(todayTransactions, stats.total_transactions, true);
        }
        if (todayIncome) {
            todayIncome.textContent = `Rp ${formatNumber(stats.total_income)}`;
        }
        if (avgTransaction) {
            avgTransaction.textContent = `Rp ${formatNumber(Math.round(stats.average_transaction))}`;
        }
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load recent transactions
async function loadRecentTransactions() {
    try {
        const response = await fetch('/api/transactions/recent');
        const transactions = await response.json();
        
        // Update transactions list if modal is open
        const transactionsList = document.getElementById('transactionsList');
        if (transactionsList && transactionsList.parentElement.style.display === 'block') {
            renderTransactionsList(transactions);
        }
        
    } catch (error) {
        console.error('Error loading recent transactions:', error);
    }
}

// Show recent transactions modal
function showRecentTransactions() {
    const modal = document.getElementById('transactionsModal');
    modal.style.display = 'flex';
    
    // Load and render transactions
    loadRecentTransactions().then(transactions => {
        renderTransactionsList(transactions);
    });
}

// Render transactions list
function renderTransactionsList(transactions) {
    const transactionsList = document.getElementById('transactionsList');
    if (!transactionsList) return;
    
    if (transactions.length === 0) {
        transactionsList.innerHTML = `
            <div class="empty-transactions">
                <i class="fas fa-history"></i>
                <h3>Belum ada transaksi</h3>
                <p>Transaksi akan muncul di sini</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    transactions.forEach(transaction => {
        html += `
            <div class="transaction-item">
                <div class="transaction-header">
                    <span class="transaction-id">${transaction.transaction_id}</span>
                    <span class="transaction-time">${transaction.date}</span>
                </div>
                <div class="transaction-body">
                    <div class="transaction-total">Rp ${formatNumber(transaction.total)}</div>
                    <div class="transaction-items">${transaction.items.length} items</div>
                </div>
            </div>
        `;
    });
    
    transactionsList.innerHTML = html;
}

// Close transactions modal
function closeTransactionsModal() {
    const modal = document.getElementById('transactionsModal');
    modal.style.display = 'none';
}

// Setup drag and drop
function setupDragAndDrop() {
    const menuGrid = document.getElementById('menuGrid');
    const cartSection = document.querySelector('.cart-section');
    
    if (!menuGrid || !cartSection) return;
    
    let draggedItem = null;
    
    // Drag start
    document.addEventListener('dragstart', function(e) {
        if (e.target.closest('.menu-item')) {
            draggedItem = e.target.closest('.menu-item');
            e.dataTransfer.setData('text/plain', draggedItem.dataset.id);
            draggedItem.style.opacity = '0.5';
        }
    });
    
    // Drag end
    document.addEventListener('dragend', function(e) {
        if (draggedItem) {
            draggedItem.style.opacity = '1';
            draggedItem = null;
        }
    });
    
    // Drag over cart
    cartSection.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = 'var(--secondary)';
        this.style.boxShadow = '0 0 20px rgba(46, 204, 113, 0.3)';
    });
    
    // Drag leave cart
    cartSection.addEventListener('dragleave', function(e) {
        this.style.borderColor = 'rgba(46, 204, 113, 0.4)';
        this.style.boxShadow = '';
    });
    
    // Drop in cart
    cartSection.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.borderColor = 'rgba(46, 204, 113, 0.4)';
        this.style.boxShadow = '';
        
        const itemId = parseInt(e.dataTransfer.getData('text/plain'));
        if (itemId) {
            quickAddToCart(itemId);
        }
    });
}

// Setup keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Don't trigger shortcuts if user is typing in input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        
        // Escape to close modals
        if (e.key === 'Escape') {
            closeStruk();
            closeTransactionsModal();
            closeItemDetail();
        }
        
        // F1 for help
        if (e.key === 'F1') {
            e.preventDefault();
            showNotification('Keyboard Shortcuts', 
                'Enter: Bayar • Esc: Tutup modal • F1: Bantuan', 
                'info', 5000);
        }
        
        // Ctrl+S to save cart
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            saveCart();
        }
        
        // Ctrl+L to load cart
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            loadCart();
        }
    });
}

// Handle window resize
function handleResize() {
    // Update cart header visibility on mobile
    const cartHeader = document.querySelector('.cart-items-header');
    if (window.innerWidth <= 767) {
        if (cartHeader) cartHeader.style.display = 'none';
    } else {
        if (cartHeader) cartHeader.style.display = 'grid';
    }
    
    // Update menu grid columns based on screen size
    const menuGrid = document.getElementById('menuGrid');
    if (menuGrid) {
        if (window.innerWidth < 768) {
            menuGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(140px, 1fr))';
        } else if (window.innerWidth < 1024) {
            menuGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(160px, 1fr))';
        } else {
            menuGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(180px, 1fr))';
        }
    }
}

// Handle before unload
function handleBeforeUnload(e) {
    if (cart.length > 0) {
        e.preventDefault();
        e.returnValue = 'Anda memiliki item dalam keranjang. Yakin ingin meninggalkan halaman?';
        return e.returnValue;
    }
}

// Save cart to localStorage
function saveCartToLocal() {
    try {
        localStorage.setItem('kasirCart', JSON.stringify(cart));
        localStorage.setItem('kasirCartTimestamp', new Date().toISOString());
    } catch (error) {
        console.error('Error saving cart to localStorage:', error);
    }
}

// Check for saved cart
function checkSavedCart() {
    try {
        const savedCart = localStorage.getItem('kasirCart');
        const savedTimestamp = localStorage.getItem('kasirCartTimestamp');
        
        if (savedCart && savedTimestamp) {
            const timestamp = new Date(savedTimestamp);
            const now = new Date();
            const hoursDiff = (now - timestamp) / (1000 * 60 * 60);
            
            // Only restore if less than 24 hours old
            if (hoursDiff < 24) {
                const parsedCart = JSON.parse(savedCart);
                if (parsedCart.length > 0) {
                    cart = parsedCart;
                    updateCart();
                    
                    showNotification('Keranjang dipulihkan', 
                        `${cart.length} item dari sesi sebelumnya`, 
                        'info');
                }
            }
        }
    } catch (error) {
        console.error('Error checking saved cart:', error);
    }
}

// Auto-save cart
function autoSaveCart() {
    if (cart.length > 0) {
        saveCartToLocal();
        console.log('🔄 Cart auto-saved:', cart.length, 'items');
    }
}

// Manual save cart
function saveCart() {
    saveCartToLocal();
    showNotification('Keranjang disimpan', 
        `${cart.length} item disimpan ke localStorage`, 
        'success');
}

// Load cart
function loadCart() {
    checkSavedCart();
}

// Create floating particles
function createFloatingParticles() {
    const colors = ['rgba(52, 152, 219, 0.1)', 'rgba(46, 204, 113, 0.08)', 'rgba(26, 188, 156, 0.06)'];
    
    for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        const size = Math.random() * 40 + 10;
        const duration = Math.random() * 20 + 10;
        const delay = Math.random() * 5;
        const color = colors[Math.floor(Math.random() * colors.length)];
        
        particle.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            left: ${Math.random() * 100}%;
            background: ${color};
            animation-duration: ${duration}s;
            animation-delay: ${delay}s;
        `;
        
        document.body.appendChild(particle);
    }
}

// Toggle dark mode
function toggleDarkMode() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    showNotification(
        newTheme === 'dark' ? 'Mode Gelap' : 'Mode Terang',
        newTheme === 'dark' ? 'Tema gelap diaktifkan' : 'Tema terang diaktifkan',
        'info'
    );
}

// Toggle stats
function toggleStats() {
    const statsBar = document.getElementById('statsBar');
    if (statsBar) {
        statsBar.style.display = statsBar.style.display === 'none' ? 'block' : 'none';
    }
}

// Refresh stats
function refreshStats() {
    loadTodayStats();
    showNotification('Statistik diperbarui', 'Data terkini telah dimuat', 'info');
}

// Show settings
function showSettings() {
    showNotification('Pengaturan', 
        'Fitur pengaturan akan segera hadir', 
        'info');
}

// Fix scroll behavior and layout
function fixLayout() {
    const menuSection = document.querySelector('.menu-section');
    const cartSection = document.querySelector('.cart-section');
    const menuGrid = document.getElementById('menuGrid');
    const cartItemsContainer = document.querySelector('.cart-items-container');
    
    if (menuSection && menuGrid) {
        // Set menu grid height
        const menuHeaderHeight = document.querySelector('.menu-header').offsetHeight;
        const categoryHeight = document.querySelector('.category-filter-container').offsetHeight;
        const popularHeight = document.querySelector('.popular-section')?.offsetHeight || 0;
        const menuFooterHeight = document.querySelector('.menu-footer')?.offsetHeight || 0;
        
        const availableHeight = menuSection.offsetHeight - menuHeaderHeight - categoryHeight - popularHeight - menuFooterHeight - 40;
        menuGrid.style.maxHeight = `${Math.max(availableHeight, 300)}px`;
    }
    
    if (cartSection && cartItemsContainer) {
        // Set cart items container height
        const cartHeaderHeight = document.querySelector('.cart-header').offsetHeight;
        const quickActionsHeight = document.querySelector('.cart-quick-actions')?.offsetHeight || 0;
        const summaryHeight = document.querySelector('.summary')?.offsetHeight || 0;
        const paymentHeight = document.querySelector('.payment-section').offsetHeight;
        
        const availableCartHeight = cartSection.offsetHeight - cartHeaderHeight - quickActionsHeight - summaryHeight - paymentHeight - 40;
        cartItemsContainer.style.maxHeight = `${Math.max(availableCartHeight, 200)}px`;
    }
}

// Call on load and resize
window.addEventListener('load', fixLayout);
window.addEventListener('resize', fixLayout);

// Export to window for inline event handlers
window.formatNumber = formatNumber;
window.scrollToMenu = function() {
    document.querySelector('.menu-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
};
window.scrollToCart = function() {
    document.querySelector('.cart-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
};
window.scrollToTop = function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
};
window.updateAllQuantities = updateAllQuantities;
window.applyDiscount = applyDiscount;
window.setPaymentAmount = setPaymentAmount;
window.formatPaymentInput = formatPaymentInput;
window.showNotification = showNotification;
window.closeItemDetail = closeItemDetail;
window.closeTransactionsModal = closeTransactionsModal;
window.showRecentTransactions = showRecentTransactions;
window.showSettings = showSettings;

// Initialize on load
setTimeout(() => {
    handleResize(); // Set initial layout
}, 100);