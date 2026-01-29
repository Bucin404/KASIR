package com.example.kasir.model

// Enums
enum class UserRole {
    ADMIN, MANAGER, CASHIER
}

enum class PaymentMethod {
    CASH, DEBIT, CREDIT, E_WALLET
}

enum class ExpenseCategory(val displayName: String, val color: Long) {
    BAHAN_BAKU("Bahan Baku", 0xFFE74C3C),
    GAJI("Gaji Karyawan", 0xFF3498DB),
    LISTRIK_AIR("Listrik & Air", 0xFFF39C12),
    SEWA("Sewa Tempat", 0xFF9B59B6),
    TRANSPORTASI("Transportasi", 0xFF1ABC9C),
    PEMASARAN("Pemasaran", 0xFFE67E22),
    PERALATAN("Peralatan", 0xFF34495E),
    LAINNYA("Lainnya", 0xFF95A5A6)
}

// UI Models
data class MenuItem(
    val id: Long,
    val name: String,
    val category: String,
    val price: Double,
    val description: String,
    val imageUrl: String,
    val isPopular: Boolean,
    val isAvailable: Boolean
)

data class CartItem(
    val menuItem: MenuItem,
    var quantity: Int
) {
    val subtotal: Double
        get() = menuItem.price * quantity
}

data class Transaction(
    val id: String,
    val userId: Long,
    val userName: String,
    val items: List<CartItem>,
    val subtotal: Double,
    val tax: Double,
    val total: Double,
    val paymentMethod: PaymentMethod,
    val createdAt: Long
)

data class Expense(
    val id: Long,
    val category: ExpenseCategory,
    val description: String,
    val amount: Double,
    val userId: Long,
    val userName: String,
    val createdAt: Long
)

data class User(
    val id: Long,
    val username: String,
    val fullName: String,
    val role: UserRole,
    val email: String?,
    val phone: String?
)

data class FinancialSummary(
    val totalRevenue: Double,
    val totalExpenses: Double,
    val netProfit: Double,
    val profitMargin: Double, // percentage
    val transactionCount: Int,
    val averageTransaction: Double
)

data class DashboardStats(
    val todayRevenue: Double,
    val todayTransactions: Int,
    val todayExpenses: Double,
    val todayProfit: Double,
    val monthRevenue: Double,
    val monthTransactions: Int
)
