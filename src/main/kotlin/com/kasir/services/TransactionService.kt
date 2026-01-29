package com.kasir.services

import com.kasir.models.*
import com.kasir.repositories.DatabaseRepository
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

class TransactionService(private val database: DatabaseRepository) {
    
    fun processCheckout(request: TransactionRequest, userId: Int?, cashierName: String): Transaction {
        val subtotal = request.items.sumOf { it.price * it.quantity }
        val tax = (subtotal * 0.10).toInt()
        val total = subtotal + tax
        val change = if (request.payment >= total) request.payment - total else 0
        
        val now = LocalDateTime.now()
        val transactionId = "TRX${now.format(DateTimeFormatter.ofPattern("yyyyMMddHHmmss"))}"
        
        val transaction = Transaction(
            transactionId = transactionId,
            date = now.format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss")),
            dateIso = now.format(DateTimeFormatter.ISO_DATE),
            items = request.items,
            subtotal = subtotal,
            tax = tax,
            total = total,
            payment = request.payment,
            change = change,
            cashier = cashierName,
            userId = userId
        )
        
        database.saveTransaction(transaction)
        return transaction
    }
    
    fun getTodayStats(): Stats {
        val transactions = database.getTodayTransactions()
        
        val totalIncome = transactions.sumOf { it.total.toLong() }.toInt()
        val totalTransactions = transactions.size
        
        val itemCounts = mutableMapOf<String, Int>()
        transactions.forEach { txn ->
            txn.items.forEach { item ->
                itemCounts[item.name] = (itemCounts[item.name] ?: 0) + item.quantity
            }
        }
        
        val mostPopular = itemCounts.entries
            .sortedByDescending { it.value }
            .take(3)
            .map { Pair(it.key, it.value) }
        
        val averageTransaction = if (totalTransactions > 0) {
            totalIncome.toDouble() / totalTransactions
        } else 0.0
        
        return Stats(
            totalIncome = totalIncome,
            totalTransactions = totalTransactions,
            mostPopular = mostPopular,
            averageTransaction = averageTransaction
        )
    }
    
    fun getRecentTransactions(limit: Int = 10): List<Transaction> {
        return database.getRecentTransactions(limit)
    }
}
