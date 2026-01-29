package com.kasir.data.local.database.dao

import androidx.room.*
import com.kasir.data.local.database.entities.ExpenseEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ExpenseDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(expense: ExpenseEntity): Long
    
    @Query("SELECT * FROM expenses ORDER BY createdAt DESC")
    fun getAllExpenses(): Flow<List<ExpenseEntity>>
    
    @Query("SELECT * FROM expenses WHERE date BETWEEN :startDate AND :endDate ORDER BY date DESC")
    fun getExpensesByDateRange(startDate: String, endDate: String): Flow<List<ExpenseEntity>>
    
    @Query("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date BETWEEN :startDate AND :endDate")
    suspend fun getTotalExpensesByDateRange(startDate: String, endDate: String): Int
    
    @Query("SELECT * FROM expenses WHERE id = :id")
    suspend fun getExpenseById(id: Int): ExpenseEntity?
    
    @Delete
    suspend fun delete(expense: ExpenseEntity)
    
    @Update
    suspend fun update(expense: ExpenseEntity)
}
