package com.kasir.models

import kotlinx.serialization.Serializable

@Serializable
data class Expense(
    val id: Int = 0,
    val category: String,
    val amount: Int,
    val description: String,
    val date: String,
    val userId: Int? = null
)

@Serializable
data class ExpenseCategory(
    val name: String,
    val color: String
)

@Serializable
data class FinancialReport(
    val period: String,
    val totalRevenue: Int,
    val totalExpenses: Int,
    val netProfit: Int,
    val profitMargin: Double,
    val transactionCount: Int,
    val averageTransaction: Double,
    val topSellingItems: List<Pair<String, Int>>,
    val expenseBreakdown: Map<String, Int>,
    val dailyRevenue: Map<String, Int>
)

@Serializable
data class CashFlowEntry(
    val date: String,
    val type: String, // "income" or "expense"
    val amount: Int,
    val balance: Int,
    val description: String
)

@Serializable
data class ReportRequest(
    val startDate: String,
    val endDate: String,
    val reportType: String, // "daily", "weekly", "monthly", "custom"
    val format: String = "json" // "json", "excel", "pdf"
)
