package com.kasir.services.report

import com.itextpdf.kernel.pdf.PdfDocument
import com.itextpdf.kernel.pdf.PdfWriter
import com.itextpdf.layout.Document
import com.itextpdf.layout.element.Paragraph
import com.itextpdf.layout.element.Table
import com.itextpdf.layout.properties.TextAlignment
import com.itextpdf.layout.properties.UnitValue
import com.kasir.models.FinancialReport
import com.kasir.models.Transaction
import java.io.ByteArrayOutputStream
import java.text.NumberFormat
import java.util.*

class PDFReportGenerator {
    
    fun generateTransactionReport(transactions: List<Transaction>, report: FinancialReport): ByteArray {
        val outputStream = ByteArrayOutputStream()
        val writer = PdfWriter(outputStream)
        val pdf = PdfDocument(writer)
        val document = Document(pdf)
        
        // Title
        document.add(
            Paragraph("LAPORAN KEUANGAN")
                .setFontSize(20f)
                .setBold()
                .setTextAlignment(TextAlignment.CENTER)
        )
        
        document.add(Paragraph("\n"))
        
        // Period
        document.add(
            Paragraph("Periode: ${report.period}")
                .setFontSize(12f)
                .setTextAlignment(TextAlignment.CENTER)
        )
        
        document.add(Paragraph("\n"))
        
        // Financial Summary
        document.add(Paragraph("RINGKASAN KEUANGAN").setFontSize(14f).setBold())
        
        val summaryTable = Table(2)
        summaryTable.setWidth(UnitValue.createPercentValue(100f))
        
        addSummaryRow(summaryTable, "Total Pendapatan", formatCurrency(report.totalRevenue))
        addSummaryRow(summaryTable, "Total Pengeluaran", formatCurrency(report.totalExpenses))
        addSummaryRow(summaryTable, "Laba Bersih", formatCurrency(report.netProfit))
        addSummaryRow(summaryTable, "Margin Laba", "${String.format("%.2f", report.profitMargin)}%")
        addSummaryRow(summaryTable, "Jumlah Transaksi", report.transactionCount.toString())
        addSummaryRow(summaryTable, "Rata-rata Transaksi", formatCurrency(report.averageTransaction.toInt()))
        
        document.add(summaryTable)
        document.add(Paragraph("\n"))
        
        // Top Selling Items
        if (report.topSellingItems.isNotEmpty()) {
            document.add(Paragraph("PRODUK TERLARIS").setFontSize(14f).setBold())
            
            val topItemsTable = Table(2)
            topItemsTable.setWidth(UnitValue.createPercentValue(100f))
            
            // Header
            topItemsTable.addCell(Paragraph("Nama Produk").setBold())
            topItemsTable.addCell(Paragraph("Jumlah Terjual").setBold())
            
            // Data
            report.topSellingItems.forEach { (name, quantity) ->
                topItemsTable.addCell(name)
                topItemsTable.addCell(quantity.toString())
            }
            
            document.add(topItemsTable)
            document.add(Paragraph("\n"))
        }
        
        // Transactions
        document.add(Paragraph("DETAIL TRANSAKSI").setFontSize(14f).setBold())
        
        val transactionTable = Table(floatArrayOf(2f, 2f, 2f, 1.5f, 1.5f))
        transactionTable.setWidth(UnitValue.createPercentValue(100f))
        
        // Header
        transactionTable.addCell(Paragraph("ID Transaksi").setBold())
        transactionTable.addCell(Paragraph("Tanggal").setBold())
        transactionTable.addCell(Paragraph("Kasir").setBold())
        transactionTable.addCell(Paragraph("Total").setBold())
        transactionTable.addCell(Paragraph("Pembayaran").setBold())
        
        // Data (limit to first 50 transactions for PDF)
        transactions.take(50).forEach { txn ->
            transactionTable.addCell(txn.transactionId)
            transactionTable.addCell(txn.date)
            transactionTable.addCell(txn.cashier)
            transactionTable.addCell(formatCurrency(txn.total))
            transactionTable.addCell(formatCurrency(txn.payment))
        }
        
        document.add(transactionTable)
        
        if (transactions.size > 50) {
            document.add(Paragraph("\n"))
            document.add(Paragraph("... dan ${transactions.size - 50} transaksi lainnya").setItalic())
        }
        
        document.close()
        
        return outputStream.toByteArray()
    }
    
    private fun addSummaryRow(table: Table, label: String, value: String) {
        table.addCell(Paragraph(label).setBold())
        table.addCell(value)
    }
    
    private fun formatCurrency(amount: Int): String {
        val format = NumberFormat.getCurrencyInstance(Locale("id", "ID"))
        return format.format(amount)
    }
}
