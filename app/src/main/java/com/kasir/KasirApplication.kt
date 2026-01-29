package com.kasir

import android.app.Application
import com.kasir.data.KasirDatabase

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
    }
}
