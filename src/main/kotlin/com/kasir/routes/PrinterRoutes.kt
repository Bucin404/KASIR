package com.kasir.routes

import com.kasir.models.ApiResponse
import com.kasir.models.PrinterConfig
import com.kasir.models.Transaction
import com.kasir.services.BluetoothPrintService
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Route.printerRoutes(printService: BluetoothPrintService) {
    
    route("/api/printer") {
        
        get("/discover") {
            try {
                val devices = printService.discoverPrinters()
                val printers = devices.map { (name, address) ->
                    PrinterConfig(deviceName = name, deviceAddress = address)
                }
                call.respond(HttpStatusCode.OK, ApiResponse(
                    success = true,
                    data = printers
                ))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to discover printers"
                ))
            }
        }
        
        post("/connect") {
            try {
                val config = call.receive<PrinterConfig>()
                val connected = printService.connectToPrinter(config.deviceAddress)
                
                if (connected) {
                    call.respond(HttpStatusCode.OK, ApiResponse(
                        success = true,
                        data = "Connected to printer: ${config.deviceName}"
                    ))
                } else {
                    call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                        success = false,
                        error = "Failed to connect to printer"
                    ))
                }
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Connection failed"
                ))
            }
        }
        
        post("/disconnect") {
            try {
                printService.disconnectPrinter()
                call.respond(HttpStatusCode.OK, ApiResponse(
                    success = true,
                    data = "Disconnected from printer"
                ))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Disconnect failed"
                ))
            }
        }
        
        post("/print") {
            try {
                val transaction = call.receive<Transaction>()
                val printed = printService.printReceipt(transaction)
                
                if (printed) {
                    call.respond(HttpStatusCode.OK, ApiResponse(
                        success = true,
                        data = "Receipt printed successfully"
                    ))
                } else {
                    call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                        success = false,
                        error = "Failed to print receipt. Please check printer connection."
                    ))
                }
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Print failed"
                ))
            }
        }
    }
}
