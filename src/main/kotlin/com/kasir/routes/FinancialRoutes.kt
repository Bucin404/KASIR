package com.kasir.routes

import com.kasir.models.ApiResponse
import com.kasir.models.Expense
import com.kasir.models.ReportRequest
import com.kasir.services.FinancialService
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import java.time.LocalDate
import java.time.format.DateTimeFormatter

fun Route.financialRoutes(financialService: FinancialService) {
    
    route("/api/financial") {
        
        // Get financial report
        get("/report") {
            try {
                val startDate = call.request.queryParameters["startDate"] ?: LocalDate.now().minusDays(30).toString()
                val endDate = call.request.queryParameters["endDate"] ?: LocalDate.now().toString()
                
                val report = financialService.generateFinancialReport(startDate, endDate)
                call.respond(HttpStatusCode.OK, ApiResponse(
                    success = true,
                    data = report
                ))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to generate report"
                ))
            }
        }
        
        // Export report to Excel
        get("/report/excel") {
            try {
                val startDate = call.request.queryParameters["startDate"] ?: LocalDate.now().minusDays(30).toString()
                val endDate = call.request.queryParameters["endDate"] ?: LocalDate.now().toString()
                
                val excelBytes = financialService.exportReportToExcel(startDate, endDate)
                
                call.response.header(
                    HttpHeaders.ContentDisposition,
                    ContentDisposition.Attachment.withParameter(
                        ContentDisposition.Parameters.FileName,
                        "laporan_${startDate}_${endDate}.xlsx"
                    ).toString()
                )
                call.respondBytes(
                    excelBytes,
                    ContentType.Application.OctetStream
                )
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to export Excel"
                ))
            }
        }
        
        // Export report to PDF
        get("/report/pdf") {
            try {
                val startDate = call.request.queryParameters["startDate"] ?: LocalDate.now().minusDays(30).toString()
                val endDate = call.request.queryParameters["endDate"] ?: LocalDate.now().toString()
                
                val pdfBytes = financialService.exportReportToPDF(startDate, endDate)
                
                call.response.header(
                    HttpHeaders.ContentDisposition,
                    ContentDisposition.Attachment.withParameter(
                        ContentDisposition.Parameters.FileName,
                        "laporan_${startDate}_${endDate}.pdf"
                    ).toString()
                )
                call.respondBytes(
                    pdfBytes,
                    ContentType.Application.Pdf
                )
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to export PDF"
                ))
            }
        }
        
        // Get cash flow
        get("/cashflow") {
            try {
                val startDate = call.request.queryParameters["startDate"] ?: LocalDate.now().minusDays(30).toString()
                val endDate = call.request.queryParameters["endDate"] ?: LocalDate.now().toString()
                
                val cashFlow = financialService.getCashFlow(startDate, endDate)
                call.respond(HttpStatusCode.OK, ApiResponse(
                    success = true,
                    data = cashFlow
                ))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to get cash flow"
                ))
            }
        }
        
        // Add expense
        post("/expense") {
            try {
                // TODO: Add authentication check
                val expense = call.receive<Expense>()
                val saved = financialService.addExpense(expense)
                
                if (saved) {
                    call.respond(HttpStatusCode.Created, ApiResponse(
                        success = true,
                        data = "Expense added successfully"
                    ))
                } else {
                    call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                        success = false,
                        error = "Failed to add expense"
                    ))
                }
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to add expense"
                ))
            }
        }
        
        // Get expenses
        get("/expenses") {
            try {
                val startDate = call.request.queryParameters["startDate"] ?: LocalDate.now().minusDays(30).toString()
                val endDate = call.request.queryParameters["endDate"] ?: LocalDate.now().toString()
                
                val expenses = financialService.getExpenses(startDate, endDate)
                call.respond(HttpStatusCode.OK, ApiResponse(
                    success = true,
                    data = expenses
                ))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to get expenses"
                ))
            }
        }
        
        // Get expense categories
        get("/expense-categories") {
            try {
                val categories = financialService.getExpenseCategories()
                call.respond(HttpStatusCode.OK, ApiResponse(
                    success = true,
                    data = categories
                ))
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, ApiResponse<String>(
                    success = false,
                    error = e.message ?: "Failed to get expense categories"
                ))
            }
        }
    }
}
