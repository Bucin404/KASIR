package com.kasir.model

data class MenuItem(
    val id: Int,
    val name: String,
    val price: Int,
    val category: String,
    val imageUrl: String,
    val description: String,
    val isPopular: Boolean = false
)

data class CartItem(
    val menuItem: MenuItem,
    var quantity: Int = 1
) {
    val subtotal: Int
        get() = menuItem.price * quantity
}

data class Transaction(
    val id: Int = 0,
    val transactionId: String,
    val date: String,
    val dateIso: String,
    val items: List<TransactionItem>,
    val subtotal: Int,
    val tax: Int,
    val total: Int,
    val payment: Int,
    val change: Int,
    val cashier: String,
    val userId: Int? = null
)

data class TransactionItem(
    val id: Int = 0,
    val transactionId: Int,
    val itemId: Int,
    val itemName: String,
    val price: Int,
    val quantity: Int
)

data class Expense(
    val id: Int = 0,
    val category: String,
    val amount: Int,
    val description: String,
    val date: String,
    val userId: Int? = null,
    val createdAt: Long = System.currentTimeMillis()
)

enum class ExpenseCategory(val displayName: String, val color: String) {
    BAHAN_BAKU("Bahan Baku", "#FF6B6B"),
    GAJI("Gaji Karyawan", "#4ECDC4"),
    LISTRIK_AIR("Listrik & Air", "#45B7D1"),
    SEWA("Sewa Tempat", "#96CEB4"),
    TRANSPORTASI("Transportasi", "#FFEAA7"),
    PEMASARAN("Pemasaran", "#DFE6E9"),
    PERALATAN("Peralatan", "#74B9FF"),
    LAIN_LAIN("Lain-lain", "#A29BFE")
}

data class User(
    val id: Int = 0,
    val username: String,
    val email: String,
    val passwordHash: String,
    val role: UserRole,
    val createdAt: Long = System.currentTimeMillis()
)

enum class UserRole {
    ADMIN,
    MANAGER,
    CASHIER
}

data class FinancialReport(
    val period: String,
    val totalRevenue: Int,
    val totalExpenses: Int,
    val netProfit: Int,
    val profitMargin: Double,
    val transactionCount: Int,
    val averageTransaction: Double,
    val topSellingItems: List<Pair<String, Int>>,
    val expenseBreakdown: Map<String, Int>,
    val dailyRevenue: Map<String, Int>
)

data class DashboardStats(
    val todayTransactions: Int,
    val todayIncome: Int,
    val averageTransaction: Int,
    val topItems: List<Pair<String, Int>>
)
