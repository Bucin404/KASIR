package com.example.kasir.data.local.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.ForeignKey

@Entity(tableName = "transactions")
data class TransactionEntity(
    @PrimaryKey
    val id: String, // TRXyyyyMMddHHmmss
    val userId: Long,
    val userName: String,
    val subtotal: Double,
    val tax: Double, // 10%
    val total: Double,
    val paymentMethod: String, // CASH, DEBIT, CREDIT, E_WALLET
    val createdAt: Long = System.currentTimeMillis()
)

@Entity(
    tableName = "transaction_items",
    foreignKeys = [
        ForeignKey(
            entity = TransactionEntity::class,
            parentColumns = ["id"],
            childColumns = ["transactionId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class TransactionItemEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val transactionId: String,
    val menuItemId: Long,
    val menuItemName: String,
    val price: Double,
    val quantity: Int,
    val subtotal: Double // price * quantity
)
