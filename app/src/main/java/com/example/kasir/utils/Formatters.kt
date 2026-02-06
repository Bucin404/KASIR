package com.example.kasir.utils

import java.text.NumberFormat
import java.text.SimpleDateFormat
import java.util.*

object CurrencyFormatter {
    private val indonesianLocale = Locale("id", "ID")
    private val currencyFormat = NumberFormat.getCurrencyInstance(indonesianLocale)
    
    fun format(amount: Double): String {
        return currencyFormat.format(amount)
    }
    
    fun formatWithoutSymbol(amount: Double): String {
        val formatted = currencyFormat.format(amount)
        return formatted.replace("Rp", "").trim()
    }
}

object DateFormatter {
    private val dateFormat = SimpleDateFormat("dd MMM yyyy", Locale("id", "ID"))
    private val timeFormat = SimpleDateFormat("HH:mm", Locale("id", "ID"))
    private val dateTimeFormat = SimpleDateFormat("dd MMM yyyy HH:mm", Locale("id", "ID"))
    private val transactionIdFormat = SimpleDateFormat("yyyyMMddHHmmss", Locale.getDefault())
    
    fun formatDate(timestamp: Long): String {
        return dateFormat.format(Date(timestamp))
    }
    
    fun formatTime(timestamp: Long): String {
        return timeFormat.format(Date(timestamp))
    }
    
    fun formatDateTime(timestamp: Long): String {
        return dateTimeFormat.format(Date(timestamp))
    }
    
    fun generateTransactionId(): String {
        return "TRX${transactionIdFormat.format(Date())}"
    }
    
    fun getStartOfDay(timestamp: Long = System.currentTimeMillis()): Long {
        val calendar = Calendar.getInstance()
        calendar.timeInMillis = timestamp
        calendar.set(Calendar.HOUR_OF_DAY, 0)
        calendar.set(Calendar.MINUTE, 0)
        calendar.set(Calendar.SECOND, 0)
        calendar.set(Calendar.MILLISECOND, 0)
        return calendar.timeInMillis
    }
    
    fun getEndOfDay(timestamp: Long = System.currentTimeMillis()): Long {
        val calendar = Calendar.getInstance()
        calendar.timeInMillis = timestamp
        calendar.set(Calendar.HOUR_OF_DAY, 23)
        calendar.set(Calendar.MINUTE, 59)
        calendar.set(Calendar.SECOND, 59)
        calendar.set(Calendar.MILLISECOND, 999)
        return calendar.timeInMillis
    }
    
    fun getStartOfMonth(timestamp: Long = System.currentTimeMillis()): Long {
        val calendar = Calendar.getInstance()
        calendar.timeInMillis = timestamp
        calendar.set(Calendar.DAY_OF_MONTH, 1)
        calendar.set(Calendar.HOUR_OF_DAY, 0)
        calendar.set(Calendar.MINUTE, 0)
        calendar.set(Calendar.SECOND, 0)
        calendar.set(Calendar.MILLISECOND, 0)
        return calendar.timeInMillis
    }
}

object ValidationUtils {
    fun isValidUsername(username: String): Boolean {
        return username.length >= 3 && username.matches(Regex("^[a-zA-Z0-9_]+$"))
    }
    
    fun isValidPassword(password: String): Boolean {
        return password.length >= 6
    }
    
    fun isValidEmail(email: String): Boolean {
        return email.matches(Regex("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"))
    }
    
    fun isValidPhone(phone: String): Boolean {
        return phone.matches(Regex("^\\+?[0-9]{10,13}$"))
    }
}
