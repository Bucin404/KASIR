package com.kasir.models

import kotlinx.serialization.Serializable

@Serializable
data class MenuItem(
    val id: Int,
    val name: String,
    val price: Int,
    val category: String,
    val image: String,
    val description: String,
    val popular: Boolean = false
)

@Serializable
data class CartItem(
    val id: Int,
    val name: String,
    val price: Int,
    val quantity: Int
)

@Serializable
data class Transaction(
    val transactionId: String,
    val date: String,
    val dateIso: String,
    val items: List<CartItem>,
    val subtotal: Int,
    val tax: Int,
    val total: Int,
    val payment: Int,
    val change: Int,
    val cashier: String,
    val userId: Int? = null
)

@Serializable
data class TransactionRequest(
    val items: List<CartItem>,
    val payment: Int
)

@Serializable
data class Stats(
    val totalIncome: Int,
    val totalTransactions: Int,
    val mostPopular: List<Pair<String, Int>>,
    val averageTransaction: Double
)

@Serializable
data class User(
    val id: Int,
    val username: String,
    val email: String,
    val role: UserRole,
    val createdAt: String
)

@Serializable
enum class UserRole {
    ADMIN,
    CASHIER,
    MANAGER
}

@Serializable
data class UserCredentials(
    val username: String,
    val password: String
)

@Serializable
data class UserRegistration(
    val username: String,
    val email: String,
    val password: String,
    val role: UserRole = UserRole.CASHIER
)

@Serializable
data class AuthResponse(
    val token: String,
    val user: User
)

@Serializable
data class Notification(
    val id: String,
    val message: String,
    val type: String, // success, error, info, warning
    val timestamp: String,
    val userId: Int? = null
)

@Serializable
data class PrinterConfig(
    val deviceName: String,
    val deviceAddress: String,
    val connected: Boolean = false
)

@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val error: String? = null
)
