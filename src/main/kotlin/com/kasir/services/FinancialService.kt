package com.kasir.services

import com.kasir.models.*
import com.kasir.repositories.DatabaseRepository
import com.kasir.services.report.ExcelReportGenerator
import com.kasir.services.report.PDFReportGenerator
import java.time.LocalDate
import java.time.format.DateTimeFormatter

class FinancialService(private val database: DatabaseRepository) {
    
    private val excelGenerator = ExcelReportGenerator()
    private val pdfGenerator = PDFReportGenerator()
    
    fun generateFinancialReport(startDate: String, endDate: String): FinancialReport {
        val transactions = database.getTransactionsByDateRange(startDate, endDate)
        val expenses = database.getExpensesByDateRange(startDate, endDate)
        
        val totalRevenue = transactions.sumOf { it.total }
        val totalExpenses = expenses.sumOf { it.amount }
        val netProfit = totalRevenue - totalExpenses
        val profitMargin = if (totalRevenue > 0) (netProfit.toDouble() / totalRevenue) * 100 else 0.0
        
        val transactionCount = transactions.size
        val averageTransaction = if (transactionCount > 0) totalRevenue.toDouble() / transactionCount else 0.0
        
        // Top selling items
        val itemCounts = mutableMapOf<String, Int>()
        for (txn in transactions) {
            for (item in txn.items) {
                itemCounts[item.name] = (itemCounts[item.name] ?: 0) + item.quantity
            }
        }
        val topSellingItems = itemCounts.entries
            .sortedByDescending { it.value }
            .take(10)
            .map { Pair(it.key, it.value) }
        
        // Expense breakdown
        val expenseBreakdown = expenses.groupBy { it.category }
            .mapValues { (_, expList) -> expList.sumOf { it.amount } }
        
        // Daily revenue
        val dailyRevenue = transactions.groupBy { it.dateIso }
            .mapValues { (_, txnList) -> txnList.sumOf { it.total } }
        
        return FinancialReport(
            period = "$startDate s/d $endDate",
            totalRevenue = totalRevenue,
            totalExpenses = totalExpenses,
            netProfit = netProfit,
            profitMargin = profitMargin,
            transactionCount = transactionCount,
            averageTransaction = averageTransaction,
            topSellingItems = topSellingItems,
            expenseBreakdown = expenseBreakdown,
            dailyRevenue = dailyRevenue
        )
    }
    
    fun exportReportToExcel(startDate: String, endDate: String): ByteArray {
        val transactions = database.getTransactionsByDateRange(startDate, endDate)
        val report = generateFinancialReport(startDate, endDate)
        return excelGenerator.generateTransactionReport(transactions, report)
    }
    
    fun exportReportToPDF(startDate: String, endDate: String): ByteArray {
        val transactions = database.getTransactionsByDateRange(startDate, endDate)
        val report = generateFinancialReport(startDate, endDate)
        return pdfGenerator.generateTransactionReport(transactions, report)
    }
    
    fun getCashFlow(startDate: String, endDate: String): List<CashFlowEntry> {
        val transactions = database.getTransactionsByDateRange(startDate, endDate)
        val expenses = database.getExpensesByDateRange(startDate, endDate)
        
        val entries = mutableListOf<CashFlowEntry>()
        var balance = 0
        
        // Combine and sort by date
        val allEntries = mutableListOf<Pair<String, Pair<String, Int>>>()
        
        transactions.forEach { txn ->
            allEntries.add(Pair(txn.dateIso, Pair("income", txn.total)))
        }
        
        expenses.forEach { exp ->
            allEntries.add(Pair(exp.date, Pair("expense", exp.amount)))
        }
        
        allEntries.sortBy { it.first }
        
        allEntries.forEach { (date, entry) ->
            val (type, amount) = entry
            balance += if (type == "income") amount else -amount
            
            entries.add(
                CashFlowEntry(
                    date = date,
                    type = type,
                    amount = amount,
                    balance = balance,
                    description = if (type == "income") "Pendapatan" else "Pengeluaran"
                )
            )
        }
        
        return entries
    }
    
    fun addExpense(expense: Expense): Boolean {
        return database.saveExpense(expense)
    }
    
    fun getExpenses(startDate: String, endDate: String): List<Expense> {
        return database.getExpensesByDateRange(startDate, endDate)
    }
    
    fun getExpenseCategories(): List<ExpenseCategory> {
        return listOf(
            ExpenseCategory("Bahan Baku", "#FF6B6B"),
            ExpenseCategory("Gaji Karyawan", "#4ECDC4"),
            ExpenseCategory("Listrik & Air", "#45B7D1"),
            ExpenseCategory("Sewa Tempat", "#96CEB4"),
            ExpenseCategory("Transportasi", "#FFEAA7"),
            ExpenseCategory("Pemasaran", "#DFE6E9"),
            ExpenseCategory("Peralatan", "#74B9FF"),
            ExpenseCategory("Lain-lain", "#A29BFE")
        )
    }
}
