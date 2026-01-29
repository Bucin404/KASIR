package com.example.kasir.data.local.database.dao

import androidx.room.*
import com.example.kasir.data.local.database.entities.TransactionEntity
import com.example.kasir.data.local.database.entities.TransactionItemEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface TransactionDao {
    
    // Transaction operations
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTransaction(transaction: TransactionEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTransactionItems(items: List<TransactionItemEntity>)
    
    @Query("SELECT * FROM transactions ORDER BY createdAt DESC")
    fun getAllTransactions(): Flow<List<TransactionEntity>>
    
    @Query("SELECT * FROM transactions WHERE id = :transactionId")
    suspend fun getTransactionById(transactionId: String): TransactionEntity?
    
    @Query("SELECT * FROM transaction_items WHERE transactionId = :transactionId")
    suspend fun getTransactionItems(transactionId: String): List<TransactionItemEntity>
    
    @Query("SELECT * FROM transactions WHERE createdAt >= :startTime AND createdAt <= :endTime ORDER BY createdAt DESC")
    fun getTransactionsByDateRange(startTime: Long, endTime: Long): Flow<List<TransactionEntity>>
    
    // Statistics queries
    @Query("SELECT COUNT(*) FROM transactions WHERE createdAt >= :startTime AND createdAt <= :endTime")
    suspend fun getTransactionCount(startTime: Long, endTime: Long): Int
    
    @Query("SELECT SUM(total) FROM transactions WHERE createdAt >= :startTime AND createdAt <= :endTime")
    suspend fun getTotalRevenue(startTime: Long, endTime: Long): Double?
    
    @Query("SELECT AVG(total) FROM transactions WHERE createdAt >= :startTime AND createdAt <= :endTime")
    suspend fun getAverageTransaction(startTime: Long, endTime: Long): Double?
    
    @Query("""
        SELECT ti.menuItemName, SUM(ti.quantity) as totalQuantity, SUM(ti.subtotal) as totalRevenue
        FROM transaction_items ti
        INNER JOIN transactions t ON ti.transactionId = t.id
        WHERE t.createdAt >= :startTime AND t.createdAt <= :endTime
        GROUP BY ti.menuItemId, ti.menuItemName
        ORDER BY totalQuantity DESC
        LIMIT :limit
    """)
    suspend fun getTopSellingItems(startTime: Long, endTime: Long, limit: Int): List<TopSellingItem>
    
    @Query("DELETE FROM transactions WHERE id = :transactionId")
    suspend fun deleteTransaction(transactionId: String)
}

data class TopSellingItem(
    val menuItemName: String,
    val totalQuantity: Int,
    val totalRevenue: Double
)
