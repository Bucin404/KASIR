package com.example.kasir.data.local.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "expenses")
data class ExpenseEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val category: String, // BAHAN_BAKU, GAJI, LISTRIK_AIR, SEWA, TRANSPORTASI, PEMASARAN, PERALATAN, LAINNYA
    val description: String,
    val amount: Double,
    val userId: Long,
    val userName: String,
    val createdAt: Long = System.currentTimeMillis()
)
