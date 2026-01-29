package com.kasir.data.local.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "expenses")
data class ExpenseEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val category: String,
    val amount: Int,
    val description: String,
    val date: String,
    val userId: Int? = null,
    val createdAt: Long
)
