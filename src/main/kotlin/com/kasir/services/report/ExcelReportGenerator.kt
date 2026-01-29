package com.kasir.services.report

import com.kasir.models.FinancialReport
import com.kasir.models.Transaction
import org.apache.poi.ss.usermodel.*
import org.apache.poi.xssf.usermodel.XSSFWorkbook
import java.io.ByteArrayOutputStream
import java.text.NumberFormat
import java.util.*

class ExcelReportGenerator {
    
    fun generateTransactionReport(transactions: List<Transaction>, report: FinancialReport): ByteArray {
        val workbook = XSSFWorkbook()
        
        // Create summary sheet
        createSummarySheet(workbook, report)
        
        // Create transactions sheet
        createTransactionsSheet(workbook, transactions)
        
        // Create top items sheet
        createTopItemsSheet(workbook, report)
        
        val outputStream = ByteArrayOutputStream()
        workbook.write(outputStream)
        workbook.close()
        
        return outputStream.toByteArray()
    }
    
    private fun createSummarySheet(workbook: Workbook, report: FinancialReport) {
        val sheet = workbook.createSheet("Summary")
        
        // Create header style
        val headerStyle = workbook.createCellStyle()
        val headerFont = workbook.createFont()
        headerFont.bold = true
        headerFont.fontHeightInPoints = 14
        headerStyle.setFont(headerFont)
        headerStyle.fillForegroundColor = IndexedColors.LIGHT_BLUE.index
        headerStyle.fillPattern = FillPatternType.SOLID_FOREGROUND
        
        // Create currency style
        val currencyStyle = workbook.createCellStyle()
        val format = workbook.createDataFormat()
        currencyStyle.dataFormat = format.getFormat("Rp #,##0")
        
        var rowNum = 0
        
        // Title
        val titleRow = sheet.createRow(rowNum++)
        val titleCell = titleRow.createCell(0)
        titleCell.setCellValue("LAPORAN KEUANGAN")
        titleCell.cellStyle = headerStyle
        
        rowNum++ // Skip a row
        
        // Period
        createRow(sheet, rowNum++, "Periode", report.period)
        
        rowNum++ // Skip a row
        
        // Financial metrics
        createRow(sheet, rowNum++, "Total Pendapatan", formatCurrency(report.totalRevenue), currencyStyle)
        createRow(sheet, rowNum++, "Total Pengeluaran", formatCurrency(report.totalExpenses), currencyStyle)
        createRow(sheet, rowNum++, "Laba Bersih", formatCurrency(report.netProfit), currencyStyle)
        createRow(sheet, rowNum++, "Margin Laba", "${String.format("%.2f", report.profitMargin)}%")
        
        rowNum++ // Skip a row
        
        // Transaction metrics
        createRow(sheet, rowNum++, "Jumlah Transaksi", report.transactionCount.toString())
        createRow(sheet, rowNum++, "Rata-rata Transaksi", formatCurrency(report.averageTransaction.toInt()), currencyStyle)
        
        // Auto-size columns
        for (i in 0..1) {
            sheet.autoSizeColumn(i)
        }
    }
    
    private fun createTransactionsSheet(workbook: Workbook, transactions: List<Transaction>) {
        val sheet = workbook.createSheet("Transaksi")
        
        // Create header style
        val headerStyle = workbook.createCellStyle()
        val headerFont = workbook.createFont()
        headerFont.bold = true
        headerStyle.setFont(headerFont)
        headerStyle.fillForegroundColor = IndexedColors.GREY_25_PERCENT.index
        headerStyle.fillPattern = FillPatternType.SOLID_FOREGROUND
        
        // Create currency style
        val currencyStyle = workbook.createCellStyle()
        val format = workbook.createDataFormat()
        currencyStyle.dataFormat = format.getFormat("Rp #,##0")
        
        // Header row
        val headerRow = sheet.createRow(0)
        val headers = listOf("ID Transaksi", "Tanggal", "Kasir", "Subtotal", "Pajak", "Total", "Pembayaran", "Kembalian")
        headers.forEachIndexed { index, header ->
            val cell = headerRow.createCell(index)
            cell.setCellValue(header)
            cell.cellStyle = headerStyle
        }
        
        // Data rows
        transactions.forEachIndexed { index, txn ->
            val row = sheet.createRow(index + 1)
            row.createCell(0).setCellValue(txn.transactionId)
            row.createCell(1).setCellValue(txn.date)
            row.createCell(2).setCellValue(txn.cashier)
            
            val subtotalCell = row.createCell(3)
            subtotalCell.setCellValue(txn.subtotal.toDouble())
            subtotalCell.cellStyle = currencyStyle
            
            val taxCell = row.createCell(4)
            taxCell.setCellValue(txn.tax.toDouble())
            taxCell.cellStyle = currencyStyle
            
            val totalCell = row.createCell(5)
            totalCell.setCellValue(txn.total.toDouble())
            totalCell.cellStyle = currencyStyle
            
            val paymentCell = row.createCell(6)
            paymentCell.setCellValue(txn.payment.toDouble())
            paymentCell.cellStyle = currencyStyle
            
            val changeCell = row.createCell(7)
            changeCell.setCellValue(txn.change.toDouble())
            changeCell.cellStyle = currencyStyle
        }
        
        // Auto-size columns
        for (i in 0..7) {
            sheet.autoSizeColumn(i)
        }
    }
    
    private fun createTopItemsSheet(workbook: Workbook, report: FinancialReport) {
        val sheet = workbook.createSheet("Produk Terlaris")
        
        // Create header style
        val headerStyle = workbook.createCellStyle()
        val headerFont = workbook.createFont()
        headerFont.bold = true
        headerStyle.setFont(headerFont)
        headerStyle.fillForegroundColor = IndexedColors.GREY_25_PERCENT.index
        headerStyle.fillPattern = FillPatternType.SOLID_FOREGROUND
        
        // Header row
        val headerRow = sheet.createRow(0)
        headerRow.createCell(0).apply {
            setCellValue("Nama Produk")
            cellStyle = headerStyle
        }
        headerRow.createCell(1).apply {
            setCellValue("Jumlah Terjual")
            cellStyle = headerStyle
        }
        
        // Data rows
        report.topSellingItems.forEachIndexed { index, (name, quantity) ->
            val row = sheet.createRow(index + 1)
            row.createCell(0).setCellValue(name)
            row.createCell(1).setCellValue(quantity.toDouble())
        }
        
        // Auto-size columns
        sheet.autoSizeColumn(0)
        sheet.autoSizeColumn(1)
    }
    
    private fun createRow(sheet: Sheet, rowNum: Int, label: String, value: String, valueStyle: CellStyle? = null) {
        val row = sheet.createRow(rowNum)
        row.createCell(0).setCellValue(label)
        val valueCell = row.createCell(1)
        valueCell.setCellValue(value)
        if (valueStyle != null) {
            valueCell.cellStyle = valueStyle
        }
    }
    
    private fun formatCurrency(amount: Int): String {
        val format = NumberFormat.getCurrencyInstance(Locale("id", "ID"))
        return format.format(amount)
    }
}
