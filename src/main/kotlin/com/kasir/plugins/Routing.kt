package com.kasir.plugins

import com.kasir.repositories.DatabaseRepository
import com.kasir.routes.*
import com.kasir.services.*
import io.ktor.server.application.*
import io.ktor.server.http.content.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import java.io.File

fun Application.configureRouting(
    database: DatabaseRepository,
    authService: AuthService,
    transactionService: TransactionService,
    notificationService: NotificationService,
    printService: BluetoothPrintService
) {
    routing {
        // API Routes
        authRoutes(authService)
        menuRoutes(database)
        transactionRoutes(transactionService)
        notificationRoutes(notificationService)
        printerRoutes(printService)
        
        // Static files - serve the existing HTML/CSS/JS
        static("/static") {
            staticRootFolder = File("static")
            files("css")
            files("js")
            files("images")
        }
        
        // Serve templates
        static("/templates") {
            staticRootFolder = File("templates")
            files(".")
        }
        
        // Home route - serve the index.html
        get("/") {
            val indexFile = File("templates/index.html")
            if (indexFile.exists()) {
                call.respondFile(indexFile)
            } else {
                call.respondText("Welcome to Kasir Modern - Kotlin Edition!", status = io.ktor.http.HttpStatusCode.OK)
            }
        }
        
        // Error pages
        get("/404") {
            val errorFile = File("templates/404.html")
            if (errorFile.exists()) {
                call.respondFile(errorFile)
            } else {
                call.respondText("404 - Page Not Found", status = io.ktor.http.HttpStatusCode.NotFound)
            }
        }
        
        get("/500") {
            val errorFile = File("templates/500.html")
            if (errorFile.exists()) {
                call.respondFile(errorFile)
            } else {
                call.respondText("500 - Internal Server Error", status = io.ktor.http.HttpStatusCode.InternalServerError)
            }
        }
    }
}
