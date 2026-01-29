package com.kasir.services

import com.kasir.models.Notification
import com.kasir.repositories.DatabaseRepository
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.SharedFlow
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.*

class NotificationService(private val database: DatabaseRepository) {
    
    private val _notificationFlow = MutableSharedFlow<Notification>(replay = 0)
    val notificationFlow: SharedFlow<Notification> = _notificationFlow
    
    suspend fun sendNotification(message: String, type: String, userId: Int? = null) {
        val notification = Notification(
            id = UUID.randomUUID().toString(),
            message = message,
            type = type,
            timestamp = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME),
            userId = userId
        )
        
        database.createNotification(notification)
        _notificationFlow.emit(notification)
    }
    
    fun getUserNotifications(userId: Int): List<Notification> {
        return database.getUserNotifications(userId)
    }
}
