package com.kasir.repositories

import com.kasir.models.*
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.transactions.transaction
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class DatabaseRepository {
    
    fun initializeDatabase() {
        transaction {
            SchemaUtils.create(Users, Transactions, TransactionItems, MenuItems, Notifications)
            
            // Initialize with default menu if empty
            if (MenuItems.selectAll().count() == 0L) {
                initializeDefaultMenu()
            }
            
            // Create default admin user if no users exist
            if (Users.selectAll().count() == 0L) {
                createDefaultAdmin()
            }
        }
    }
    
    private fun initializeDefaultMenu() {
        val defaultMenu = getDefaultMenuItems()
        defaultMenu.forEach { item ->
            MenuItems.insert {
                it[id] = item.id
                it[name] = item.name
                it[price] = item.price
                it[category] = item.category
                it[image] = item.image
                it[description] = item.description
                it[popular] = item.popular
            }
        }
    }
    
    private fun createDefaultAdmin() {
        val passwordHash = org.mindrot.jbcrypt.BCrypt.hashpw("admin123", org.mindrot.jbcrypt.BCrypt.gensalt())
        Users.insert {
            it[username] = "admin"
            it[email] = "admin@kasir.com"
            it[this.passwordHash] = passwordHash
            it[role] = "ADMIN"
            it[createdAt] = LocalDateTime.now()
        }
    }
    
    // User operations
    fun createUser(registration: UserRegistration): User? {
        return transaction {
            try {
                val passwordHash = org.mindrot.jbcrypt.BCrypt.hashpw(registration.password, org.mindrot.jbcrypt.BCrypt.gensalt())
                val id = Users.insertAndGetId {
                    it[username] = registration.username
                    it[email] = registration.email
                    it[this.passwordHash] = passwordHash
                    it[role] = registration.role.name
                    it[createdAt] = LocalDateTime.now()
                }
                
                User(
                    id = id.value,
                    username = registration.username,
                    email = registration.email,
                    role = registration.role,
                    createdAt = LocalDateTime.now().toString()
                )
            } catch (e: Exception) {
                null
            }
        }
    }
    
    fun getUserByUsername(username: String): Pair<User, String>? {
        return transaction {
            Users.select { Users.username eq username }
                .map { row ->
                    val user = User(
                        id = row[Users.id].value,
                        username = row[Users.username],
                        email = row[Users.email],
                        role = UserRole.valueOf(row[Users.role]),
                        createdAt = row[Users.createdAt].toString()
                    )
                    Pair(user, row[Users.passwordHash])
                }
                .firstOrNull()
        }
    }
    
    fun getAllUsers(): List<User> {
        return transaction {
            Users.selectAll().map { row ->
                User(
                    id = row[Users.id].value,
                    username = row[Users.username],
                    email = row[Users.email],
                    role = UserRole.valueOf(row[Users.role]),
                    createdAt = row[Users.createdAt].toString()
                )
            }
        }
    }
    
    // Menu operations
    fun getAllMenuItems(): List<MenuItem> {
        return transaction {
            MenuItems.selectAll().map { row ->
                MenuItem(
                    id = row[MenuItems.id].value,
                    name = row[MenuItems.name],
                    price = row[MenuItems.price],
                    category = row[MenuItems.category],
                    image = row[MenuItems.image],
                    description = row[MenuItems.description],
                    popular = row[MenuItems.popular]
                )
            }
        }
    }
    
    fun addMenuItem(item: MenuItem): MenuItem? {
        return transaction {
            try {
                val id = MenuItems.insertAndGetId {
                    it[name] = item.name
                    it[price] = item.price
                    it[category] = item.category
                    it[image] = item.image
                    it[description] = item.description
                    it[popular] = item.popular
                }
                item.copy(id = id.value)
            } catch (e: Exception) {
                null
            }
        }
    }
    
    fun updateMenuItem(id: Int, item: MenuItem): Boolean {
        return transaction {
            MenuItems.update({ MenuItems.id eq id }) {
                it[name] = item.name
                it[price] = item.price
                it[category] = item.category
                it[image] = item.image
                it[description] = item.description
                it[popular] = item.popular
            } > 0
        }
    }
    
    fun deleteMenuItem(id: Int): Boolean {
        return transaction {
            MenuItems.deleteWhere { MenuItems.id eq id } > 0
        }
    }
    
    // Transaction operations
    fun saveTransaction(txn: Transaction): Boolean {
        return transaction {
            try {
                val txnId = Transactions.insertAndGetId {
                    it[transactionId] = txn.transactionId
                    it[date] = txn.date
                    it[dateIso] = txn.dateIso
                    it[subtotal] = txn.subtotal
                    it[tax] = txn.tax
                    it[total] = txn.total
                    it[payment] = txn.payment
                    it[change] = txn.change
                    it[cashier] = txn.cashier
                    it[userId] = txn.userId
                }
                
                txn.items.forEach { item ->
                    TransactionItems.insert {
                        it[transactionId] = txnId
                        it[itemId] = item.id
                        it[itemName] = item.name
                        it[price] = item.price
                        it[quantity] = item.quantity
                    }
                }
                true
            } catch (e: Exception) {
                e.printStackTrace()
                false
            }
        }
    }
    
    fun getTodayTransactions(): List<Transaction> {
        val today = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE)
        return transaction {
            Transactions.select { Transactions.dateIso like "$today%" }
                .map { row ->
                    val txnId = row[Transactions.id]
                    val items = TransactionItems.select { TransactionItems.transactionId eq txnId }
                        .map { itemRow ->
                            CartItem(
                                id = itemRow[TransactionItems.itemId],
                                name = itemRow[TransactionItems.itemName],
                                price = itemRow[TransactionItems.price],
                                quantity = itemRow[TransactionItems.quantity]
                            )
                        }
                    
                    Transaction(
                        transactionId = row[Transactions.transactionId],
                        date = row[Transactions.date],
                        dateIso = row[Transactions.dateIso],
                        items = items,
                        subtotal = row[Transactions.subtotal],
                        tax = row[Transactions.tax],
                        total = row[Transactions.total],
                        payment = row[Transactions.payment],
                        change = row[Transactions.change],
                        cashier = row[Transactions.cashier],
                        userId = row[Transactions.userId]
                    )
                }
        }
    }
    
    fun getRecentTransactions(limit: Int = 10): List<Transaction> {
        return transaction {
            Transactions.selectAll()
                .orderBy(Transactions.id to SortOrder.DESC)
                .limit(limit)
                .map { row ->
                    val txnId = row[Transactions.id]
                    val items = TransactionItems.select { TransactionItems.transactionId eq txnId }
                        .map { itemRow ->
                            CartItem(
                                id = itemRow[TransactionItems.itemId],
                                name = itemRow[TransactionItems.itemName],
                                price = itemRow[TransactionItems.price],
                                quantity = itemRow[TransactionItems.quantity]
                            )
                        }
                    
                    Transaction(
                        transactionId = row[Transactions.transactionId],
                        date = row[Transactions.date],
                        dateIso = row[Transactions.dateIso],
                        items = items,
                        subtotal = row[Transactions.subtotal],
                        tax = row[Transactions.tax],
                        total = row[Transactions.total],
                        payment = row[Transactions.payment],
                        change = row[Transactions.change],
                        cashier = row[Transactions.cashier],
                        userId = row[Transactions.userId]
                    )
                }
        }
    }
    
    // Notification operations
    fun createNotification(notification: Notification): Boolean {
        return transaction {
            try {
                Notifications.insert {
                    it[message] = notification.message
                    it[type] = notification.type
                    it[timestamp] = notification.timestamp
                    it[userId] = notification.userId
                }
                true
            } catch (e: Exception) {
                false
            }
        }
    }
    
    fun getUserNotifications(userId: Int): List<Notification> {
        return transaction {
            Notifications.select { Notifications.userId eq userId }
                .orderBy(Notifications.id to SortOrder.DESC)
                .map { row ->
                    Notification(
                        id = row[Notifications.id].value.toString(),
                        message = row[Notifications.message],
                        type = row[Notifications.type],
                        timestamp = row[Notifications.timestamp],
                        userId = row[Notifications.userId]
                    )
                }
        }
    }
    
    private fun getDefaultMenuItems(): List<MenuItem> {
        return listOf(
            // Makanan
            MenuItem(1, "Nasi Goreng Spesial", 25000, "Makanan", 
                "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&h=200&fit=crop&auto=format",
                "Nasi goreng dengan telur, ayam, dan sayuran segar", true),
            MenuItem(2, "Mie Ayam Bakso", 20000, "Makanan",
                "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=300&h=200&fit=crop&auto=format",
                "Mie ayam dengan bakso sapi pilihan", true),
            MenuItem(3, "Ayam Goreng Crispy", 18000, "Makanan",
                "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=300&h=200&fit=crop&auto=format",
                "Ayam goreng crispy dengan bumbu rempah", false),
            MenuItem(4, "Sate Ayam (10 tusuk)", 22000, "Makanan",
                "https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?w=300&h=200&fit=crop&auto=format",
                "Sate ayam dengan bumbu kacang spesial", true),
            MenuItem(5, "Nasi Campur Komplit", 22000, "Makanan",
                "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop&auto=format",
                "Nasi dengan lauk lengkap dan sayuran", false),
            MenuItem(6, "Rendang Daging Sapi", 30000, "Makanan",
                "https://images.unsplash.com/photo-1555939614-8674f6df1389?w=300&h=200&fit=crop&auto=format",
                "Rendang daging sapi dengan bumbu rempah pilihan", true),
            MenuItem(7, "Soto Ayam Lamongan", 22000, "Makanan",
                "https://images.unsplash.com/photo-1553909489-cd47e0907980?w=300&h=200&fit=crop&auto=format",
                "Soto ayam dengan bumbu koya dan sambal", true),
            MenuItem(8, "Gado-gado", 18000, "Makanan",
                "https://images.unsplash.com/photo-1559054663-e8d23213f55c?w=300&h=200&fit=crop&auto=format",
                "Sayuran segar dengan bumbu kacang khas", false),
            
            // Minuman
            MenuItem(9, "Es Teh Manis", 5000, "Minuman",
                "https://images.unsplash.com/photo-1597481499753-6e63aca6d3f3?w=300&h=200&fit=crop&auto=format",
                "Es teh manis dengan gula aren", true),
            MenuItem(10, "Jus Alpukat", 15000, "Minuman",
                "https://images.unsplash.com/photo-1623063878630-7c10b5f6d0c9?w=300&h=200&fit=crop&auto=format",
                "Jus alpukat segar dengan susu kental", true),
            MenuItem(11, "Kopi Latte", 18000, "Minuman",
                "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop&auto=format",
                "Kopi latte dengan susu segar", true),
            MenuItem(12, "Air Mineral", 4000, "Minuman",
                "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=300&h=200&fit=crop&auto=format",
                "Air mineral botolan 600ml", false),
            MenuItem(13, "Es Jeruk Segar", 8000, "Minuman",
                "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=300&h=200&fit=crop&auto=format",
                "Es jeruk peras tanpa biji", true),
            MenuItem(14, "Milkshake Coklat", 20000, "Minuman",
                "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=300&h=200&fit=crop&auto=format",
                "Milkshake coklat dengan topping whipped cream", true),
            MenuItem(15, "Matcha Latte", 22000, "Minuman",
                "https://images.unsplash.com/photo-1561047029-3000c68339ca?w=300&h=200&fit=crop&auto=format",
                "Matcha latte dengan susu oat", false),
            MenuItem(16, "Boba Milk Tea", 18000, "Minuman",
                "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300&h=200&fit=crop&auto=format",
                "Milk tea dengan bubble boba", true),
            
            // Dessert
            MenuItem(17, "Brownies Coklat", 12000, "Dessert",
                "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=200&fit=crop&auto=format",
                "Brownies coklat premium dengan kacang", true),
            MenuItem(18, "Pisang Goreng", 8000, "Dessert",
                "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop&auto=format",
                "Pisang goreng dengan keju parut", false),
            MenuItem(19, "Donat Gula", 7000, "Dessert",
                "https://images.unsplash.com/photo-1551106652-a5bcf4b29ab6?w=300&h=200&fit=crop&auto=format",
                "Donat lembut dengan taburan gula", true),
            MenuItem(20, "Puding Coklat", 10000, "Dessert",
                "https://images.unsplash.com/photo-1623334044303-241021148842?w=300&h=200&fit=crop&auto=format",
                "Puding coklat dengan saus karamel", false),
            MenuItem(21, "Es Krim Vanilla", 15000, "Dessert",
                "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop&auto=format",
                "Es krim vanilla dengan topping coklat", true),
            MenuItem(22, "Cheesecake Berry", 25000, "Dessert",
                "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=300&h=200&fit=crop&auto=format",
                "Cheesecake dengan saus berry segar", true),
            MenuItem(23, "Tiramisu", 22000, "Dessert",
                "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=300&h=200&fit=crop&auto=format",
                "Tiramisu klasik Italia", true),
            MenuItem(24, "Waffle Madu", 18000, "Dessert",
                "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300&h=200&fit=crop&auto=format",
                "Waffle renyah dengan madu dan buah", false)
        )
    }
}
