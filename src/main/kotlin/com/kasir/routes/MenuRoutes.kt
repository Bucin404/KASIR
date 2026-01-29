package com.kasir.routes

import com.kasir.models.ApiResponse
import com.kasir.models.MenuItem
import com.kasir.repositories.DatabaseRepository
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Route.menuRoutes(database: DatabaseRepository) {
    
    route("/api/menu") {
        
        get {
            try {
                val menu = database.getAllMenuItems()
                call.respond(HttpStatusCode.OK, menu)
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to fetch menu"
                ))
            }
        }
        
        // Admin only routes
        post {
            try {
                // TODO: Add authentication check for admin role
                val item = call.receive<MenuItem>()
                val newItem = database.addMenuItem(item)
                
                if (newItem != null) {
                    call.respond(HttpStatusCode.Created, ApiResponse(
                        success = true,
                        data = newItem
                    ))
                } else {
                    call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                        success = false,
                        error = "Failed to add menu item"
                    ))
                }
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to add menu item"
                ))
            }
        }
        
        put("/{id}") {
            try {
                // TODO: Add authentication check for admin role
                val id = call.parameters["id"]?.toIntOrNull() ?: return@put call.respond(
                    HttpStatusCode.BadRequest, ApiResponse<String>(
                        success = false,
                        error = "Invalid ID"
                    )
                )
                
                val item = call.receive<MenuItem>()
                val updated = database.updateMenuItem(id, item)
                
                if (updated) {
                    call.respond(HttpStatusCode.OK, ApiResponse(
                        success = true,
                        data = item.copy(id = id)
                    ))
                } else {
                    call.respond(HttpStatusCode.NotFound, ApiResponse<String>(
                        success = false,
                        error = "Menu item not found"
                    ))
                }
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to update menu item"
                ))
            }
        }
        
        delete("/{id}") {
            try {
                // TODO: Add authentication check for admin role
                val id = call.parameters["id"]?.toIntOrNull() ?: return@delete call.respond(
                    HttpStatusCode.BadRequest, ApiResponse<String>(
                        success = false,
                        error = "Invalid ID"
                    )
                )
                
                val deleted = database.deleteMenuItem(id)
                
                if (deleted) {
                    call.respond(HttpStatusCode.OK, ApiResponse(
                        success = true,
                        data = "Menu item deleted successfully"
                    ))
                } else {
                    call.respond(HttpStatusCode.NotFound, ApiResponse<String>(
                        success = false,
                        error = "Menu item not found"
                    ))
                }
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to delete menu item"
                ))
            }
        }
    }
}
