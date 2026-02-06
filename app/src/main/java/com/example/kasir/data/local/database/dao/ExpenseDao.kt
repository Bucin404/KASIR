package com.example.kasir.data.local.database.dao

import androidx.room.*
import com.example.kasir.data.local.database.entities.ExpenseEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface ExpenseDao {
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertExpense(expense: ExpenseEntity): Long
    
    @Update
    suspend fun updateExpense(expense: ExpenseEntity)
    
    @Delete
    suspend fun deleteExpense(expense: ExpenseEntity)
    
    @Query("SELECT * FROM expenses ORDER BY createdAt DESC")
    fun getAllExpenses(): Flow<List<ExpenseEntity>>
    
    @Query("SELECT * FROM expenses WHERE id = :id")
    suspend fun getExpenseById(id: Long): ExpenseEntity?
    
    @Query("SELECT * FROM expenses WHERE createdAt >= :startTime AND createdAt <= :endTime ORDER BY createdAt DESC")
    fun getExpensesByDateRange(startTime: Long, endTime: Long): Flow<List<ExpenseEntity>>
    
    @Query("SELECT * FROM expenses WHERE category = :category ORDER BY createdAt DESC")
    fun getExpensesByCategory(category: String): Flow<List<ExpenseEntity>>
    
    @Query("SELECT SUM(amount) FROM expenses WHERE createdAt >= :startTime AND createdAt <= :endTime")
    suspend fun getTotalExpenses(startTime: Long, endTime: Long): Double?
    
    @Query("""
        SELECT category, SUM(amount) as totalAmount, COUNT(*) as count
        FROM expenses
        WHERE createdAt >= :startTime AND createdAt <= :endTime
        GROUP BY category
        ORDER BY totalAmount DESC
    """)
    suspend fun getExpensesByCategory(startTime: Long, endTime: Long): List<ExpenseSummary>
    
    @Query("DELETE FROM expenses WHERE id = :id")
    suspend fun deleteExpenseById(id: Long)
}

data class ExpenseSummary(
    val category: String,
    val totalAmount: Double,
    val count: Int
)
