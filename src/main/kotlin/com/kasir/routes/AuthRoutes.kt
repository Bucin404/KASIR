package com.kasir.routes

import com.kasir.models.*
import com.kasir.services.AuthService
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Route.authRoutes(authService: AuthService) {
    
    route("/api/auth") {
        
        post("/register") {
            try {
                val registration = call.receive<UserRegistration>()
                
                // Validate input
                if (registration.username.isBlank() || registration.password.isBlank() || registration.email.isBlank()) {
                    call.respond(HttpStatusCode.BadRequest, ApiResponse<String>(
                        success = false,
                        error = "Username, email, and password are required"
                    ))
                    return@post
                }
                
                val user = authService.register(registration)
                
                if (user != null) {
                    call.respond(HttpStatusCode.Created, ApiResponse(
                        success = true,
                        data = user
                    ))
                } else {
                    call.respond(HttpStatusCode.Conflict, ApiResponse<String>(
                        success = false,
                        error = "User already exists"
                    ))
                }
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Registration failed"
                ))
            }
        }
        
        post("/login") {
            try {
                val credentials = call.receive<UserCredentials>()
                
                if (credentials.username.isBlank() || credentials.password.isBlank()) {
                    call.respond(HttpStatusCode.BadRequest, ApiResponse<String>(
                        success = false,
                        error = "Username and password are required"
                    ))
                    return@post
                }
                
                val authResponse = authService.login(credentials)
                
                if (authResponse != null) {
                    call.respond(HttpStatusCode.OK, ApiResponse(
                        success = true,
                        data = authResponse
                    ))
                } else {
                    call.respond(HttpStatusCode.Unauthorized, ApiResponse<String>(
                        success = false,
                        error = "Invalid credentials"
                    ))
                }
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Login failed"
                ))
            }
        }
    }
}
