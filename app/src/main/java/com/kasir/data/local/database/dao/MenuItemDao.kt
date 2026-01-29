package com.kasir.data.local.database.dao

import androidx.room.*
import com.kasir.data.local.database.entities.MenuItemEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface MenuItemDao {
    @Query("SELECT * FROM menu_items ORDER BY id ASC")
    fun getAllItems(): Flow<List<MenuItemEntity>>
    
    @Query("SELECT * FROM menu_items WHERE category = :category ORDER BY id ASC")
    fun getItemsByCategory(category: String): Flow<List<MenuItemEntity>>
    
    @Query("SELECT * FROM menu_items WHERE id = :id")
    suspend fun getItemById(id: Int): MenuItemEntity?
    
    @Query("SELECT * FROM menu_items WHERE isPopular = 1 ORDER BY id ASC")
    fun getPopularItems(): Flow<List<MenuItemEntity>>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<MenuItemEntity>)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(item: MenuItemEntity)
    
    @Update
    suspend fun update(item: MenuItemEntity)
    
    @Delete
    suspend fun delete(item: MenuItemEntity)
    
    @Query("SELECT COUNT(*) FROM menu_items")
    suspend fun getCount(): Int
    
    @Query("DELETE FROM menu_items")
    suspend fun deleteAll()
}
