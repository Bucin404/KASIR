package com.kasir.routes

import com.kasir.models.ApiResponse
import com.kasir.services.NotificationService
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.flow.onEach
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

fun Route.notificationRoutes(notificationService: NotificationService) {
    
    route("/api/notifications") {
        
        get("/{userId}") {
            try {
                val userId = call.parameters["userId"]?.toIntOrNull() ?: return@get call.respond(
                    HttpStatusCode.BadRequest, ApiResponse<String>(
                        success = false,
                        error = "Invalid user ID"
                    )
                )
                
                val notifications = notificationService.getUserNotifications(userId)
                call.respond(HttpStatusCode.OK, notifications)
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to fetch notifications"
                ))
            }
        }
    }
    
    // WebSocket route for real-time notifications
    webSocket("/ws/notifications") {
        try {
            // Send a welcome message
            send(Frame.Text(Json.encodeToString(mapOf(
                "type" to "connected",
                "message" to "Connected to notification stream"
            ))))
            
            // Subscribe to notification flow
            notificationService.notificationFlow
                .onEach { notification ->
                    send(Frame.Text(Json.encodeToString(notification)))
                }
                .collect()
                
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
