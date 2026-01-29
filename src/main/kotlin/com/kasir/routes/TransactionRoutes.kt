package com.kasir.routes

import com.kasir.models.ApiResponse
import com.kasir.models.TransactionRequest
import com.kasir.services.TransactionService
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Route.transactionRoutes(transactionService: TransactionService) {
    
    route("/api") {
        
        get("/stats") {
            try {
                val stats = transactionService.getTodayStats()
                call.respond(HttpStatusCode.OK, stats)
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to fetch stats"
                ))
            }
        }
        
        post("/checkout") {
            try {
                val request = call.receive<TransactionRequest>()
                
                if (request.items.isEmpty()) {
                    call.respond(HttpStatusCode.BadRequest, ApiResponse<String>(
                        success = false,
                        error = "Keranjang kosong"
                    ))
                    return@post
                }
                
                // TODO: Get userId from authentication
                val userId: Int? = null
                val cashierName = "Kasir Utama" // TODO: Get from authenticated user
                
                val transaction = transactionService.processCheckout(request, userId, cashierName)
                
                call.respond(HttpStatusCode.OK, transaction)
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Checkout failed"
                ))
            }
        }
        
        get("/transactions/today") {
            try {
                val transactions = transactionService.getTodayStats()
                call.respond(HttpStatusCode.OK, mapOf(
                    "count" to transactions.totalTransactions,
                    "transactions" to transactionService.getRecentTransactions(10)
                ))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to fetch transactions"
                ))
            }
        }
        
        get("/transactions/recent") {
            try {
                val transactions = transactionService.getRecentTransactions(5)
                call.respond(HttpStatusCode.OK, transactions)
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to fetch recent transactions"
                ))
            }
        }
    }
}
