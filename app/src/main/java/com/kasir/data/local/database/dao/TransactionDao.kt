package com.kasir.data.local.database.dao

import androidx.room.*
import com.kasir.data.local.database.entities.TransactionEntity
import com.kasir.data.local.database.entities.TransactionItemEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface TransactionDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTransaction(transaction: TransactionEntity): Long
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTransactionItems(items: List<TransactionItemEntity>)
    
    @Query("SELECT * FROM transactions ORDER BY id DESC")
    fun getAllTransactions(): Flow<List<TransactionEntity>>
    
    @Query("SELECT * FROM transactions WHERE dateIso = :date ORDER BY id DESC")
    fun getTransactionsByDate(date: String): Flow<List<TransactionEntity>>
    
    @Query("SELECT * FROM transactions WHERE dateIso BETWEEN :startDate AND :endDate ORDER BY id DESC")
    fun getTransactionsByDateRange(startDate: String, endDate: String): Flow<List<TransactionEntity>>
    
    @Query("SELECT * FROM transactions WHERE id = :id")
    suspend fun getTransactionById(id: Int): TransactionEntity?
    
    @Query("SELECT * FROM transaction_items WHERE transactionId = :transactionId")
    suspend fun getTransactionItems(transactionId: Int): List<TransactionItemEntity>
    
    @Query("SELECT COUNT(*) FROM transactions WHERE dateIso = :date")
    suspend fun getTransactionCountByDate(date: String): Int
    
    @Query("SELECT COALESCE(SUM(total), 0) FROM transactions WHERE dateIso = :date")
    suspend fun getTotalIncomeByDate(date: String): Int
    
    @Query("SELECT COALESCE(SUM(total), 0) FROM transactions WHERE dateIso BETWEEN :startDate AND :endDate")
    suspend fun getTotalIncomeByDateRange(startDate: String, endDate: String): Int
    
    @Query("SELECT COUNT(*) FROM transactions WHERE dateIso BETWEEN :startDate AND :endDate")
    suspend fun getTransactionCountByDateRange(startDate: String, endDate: String): Int
}
