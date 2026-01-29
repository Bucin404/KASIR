package com.kasir.data.local.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "transactions")
data class TransactionEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val transactionId: String,
    val date: String,
    val dateIso: String,
    val subtotal: Int,
    val tax: Int,
    val total: Int,
    val payment: Int,
    val changeAmount: Int,
    val cashier: String,
    val userId: Int? = null
)

@Entity(tableName = "transaction_items")
data class TransactionItemEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val transactionId: Int,
    val itemId: Int,
    val itemName: String,
    val price: Int,
    val quantity: Int
)
