package com.kasir.repositories

import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.javatime.datetime

object Users : IntIdTable() {
    val username = varchar("username", 100).uniqueIndex()
    val email = varchar("email", 255).uniqueIndex()
    val passwordHash = varchar("password_hash", 255)
    val role = varchar("role", 50)
    val createdAt = datetime("created_at")
}

object Transactions : IntIdTable() {
    val transactionId = varchar("transaction_id", 100).uniqueIndex()
    val date = varchar("date", 100)
    val dateIso = varchar("date_iso", 100)
    val subtotal = integer("subtotal")
    val tax = integer("tax")
    val total = integer("total")
    val payment = integer("payment")
    val change = integer("change_amount")
    val cashier = varchar("cashier", 100)
    val userId = integer("user_id").nullable()
}

object TransactionItems : IntIdTable() {
    val transactionId = reference("transaction_id", Transactions)
    val itemId = integer("item_id")
    val itemName = varchar("item_name", 255)
    val price = integer("price")
    val quantity = integer("quantity")
}

object MenuItems : IntIdTable() {
    val name = varchar("name", 255)
    val price = integer("price")
    val category = varchar("category", 100)
    val image = text("image")
    val description = text("description")
    val popular = bool("popular").default(false)
}

object Notifications : IntIdTable() {
    val message = text("message")
    val type = varchar("type", 50)
    val timestamp = varchar("timestamp", 100)
    val userId = integer("user_id").nullable()
    val read = bool("read").default(false)
}
