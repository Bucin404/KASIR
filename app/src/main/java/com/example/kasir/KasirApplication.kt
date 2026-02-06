package com.example.kasir

import android.app.Application
import com.example.kasir.data.local.database.KasirDatabase

class KasirApplication : Application() {
    
    // Lazy initialization of database
    val database: KasirDatabase by lazy {
        KasirDatabase.getDatabase(this)
    }
    
    override fun onCreate() {
        super.onCreate()
        instance = this
    }
    
    companion object {
        lateinit var instance: KasirApplication
            private set
            
        fun getDatabase(): KasirDatabase {
            return instance.database
        }
    }
}
