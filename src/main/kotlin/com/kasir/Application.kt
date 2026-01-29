package com.kasir

import com.kasir.plugins.*
import com.kasir.repositories.DatabaseRepository
import com.kasir.services.*
import io.ktor.server.application.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import org.jetbrains.exposed.sql.Database

fun main() {
    embeddedServer(Netty, port = 8000, host = "0.0.0.0", module = Application::module)
        .start(wait = true)
}

fun Application.module() {
    // Initialize database
    Database.connect("jdbc:sqlite:kasir.db", driver = "org.sqlite.JDBC")
    
    val database = DatabaseRepository()
    database.initializeDatabase()
    
    // Initialize services
    val authService = AuthService(database)
    val transactionService = TransactionService(database)
    val notificationService = NotificationService(database)
    val printService = BluetoothPrintService()
    
    // Configure plugins
    configureSerialization()
    configureCORS()
    configureMonitoring()
    configureWebSockets()
    configureRouting(database, authService, transactionService, notificationService, printService)
    
    println("""
    🍽️  KASIR MODERN - KOTLIN EDITION
    ====================================
    🎯 NEW FEATURES:
    1. ✅ Authentication & JWT-based login
    2. ✅ Role-based access control (Admin, Cashier, Manager)
    3. ✅ Real-time notifications via WebSocket
    4. ✅ Bluetooth receipt printer support
    5. ✅ Admin menu management (Add/Edit/Delete items)
    6. ✅ Enhanced transaction tracking with user attribution
    7. ✅ RESTful API architecture
    8. ✅ SQLite database persistence
    
    📸 Preserves original UI/UX design
    📱 Same layout: scrollable menu, fixed cart
    🎨 Theme: Blue-Green Modern Premium
    🔧 Backend: Kotlin + Ktor
    🌐 Server: http://0.0.0.0:8000
    
    🔐 Default Admin Credentials:
       Username: admin
       Password: admin123
    
    📡 API Endpoints:
       - POST /api/auth/register - Register new user
       - POST /api/auth/login - Login
       - GET  /api/menu - Get menu items
       - POST /api/menu - Add menu item (Admin)
       - PUT  /api/menu/:id - Update menu item (Admin)
       - DELETE /api/menu/:id - Delete menu item (Admin)
       - POST /api/checkout - Process transaction
       - GET  /api/stats - Get today's statistics
       - GET  /api/transactions/today - Get today's transactions
       - GET  /api/transactions/recent - Get recent transactions
       - GET  /api/notifications/:userId - Get user notifications
       - WS   /ws/notifications - Real-time notification stream
       - GET  /api/printer/discover - Discover Bluetooth printers
       - POST /api/printer/connect - Connect to printer
       - POST /api/printer/disconnect - Disconnect from printer
       - POST /api/printer/print - Print receipt
    ====================================
    """.trimIndent())
}
