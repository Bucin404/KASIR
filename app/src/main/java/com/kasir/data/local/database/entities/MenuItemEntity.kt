package com.kasir.data.local.database.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "menu_items")
data class MenuItemEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val price: Int,
    val category: String,
    val imageUrl: String,
    val description: String,
    val isPopular: Boolean
)
