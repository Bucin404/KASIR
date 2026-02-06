package com.example.kasir.data.local.database.dao

import androidx.room.*
import com.example.kasir.data.local.database.entities.MenuItemEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface MenuItemDao {
    
    @Query("SELECT * FROM menu_items WHERE isAvailable = 1 ORDER BY category, name")
    fun getAllMenuItems(): Flow<List<MenuItemEntity>>
    
    @Query("SELECT * FROM menu_items WHERE category = :category AND isAvailable = 1 ORDER BY name")
    fun getMenuItemsByCategory(category: String): Flow<List<MenuItemEntity>>
    
    @Query("SELECT * FROM menu_items WHERE isPopular = 1 AND isAvailable = 1 ORDER BY name")
    fun getPopularItems(): Flow<List<MenuItemEntity>>
    
    @Query("SELECT * FROM menu_items WHERE id = :id")
    suspend fun getMenuItemById(id: Long): MenuItemEntity?
    
    @Query("SELECT * FROM menu_items WHERE name LIKE '%' || :query || '%' AND isAvailable = 1")
    fun searchMenuItems(query: String): Flow<List<MenuItemEntity>>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertMenuItem(item: MenuItemEntity): Long
    
    @Update
    suspend fun updateMenuItem(item: MenuItemEntity)
    
    @Delete
    suspend fun deleteMenuItem(item: MenuItemEntity)
    
    @Query("DELETE FROM menu_items WHERE id = :id")
    suspend fun deleteMenuItemById(id: Long)
    
    @Query("SELECT DISTINCT category FROM menu_items ORDER BY category")
    fun getAllCategories(): Flow<List<String>>
}
