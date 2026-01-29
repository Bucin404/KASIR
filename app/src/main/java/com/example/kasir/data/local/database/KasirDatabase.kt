package com.example.kasir.data.local.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.sqlite.db.SupportSQLiteDatabase
import com.example.kasir.data.local.database.dao.*
import com.example.kasir.data.local.database.entities.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.security.MessageDigest

@Database(
    entities = [
        MenuItemEntity::class,
        UserEntity::class,
        TransactionEntity::class,
        TransactionItemEntity::class,
        ExpenseEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class KasirDatabase : RoomDatabase() {
    
    abstract fun menuItemDao(): MenuItemDao
    abstract fun userDao(): UserDao
    abstract fun transactionDao(): TransactionDao
    abstract fun expenseDao(): ExpenseDao
    
    companion object {
        @Volatile
        private var INSTANCE: KasirDatabase? = null
        
        fun getDatabase(context: Context): KasirDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    KasirDatabase::class.java,
                    "kasir_database"
                )
                    .addCallback(DatabaseCallback())
                    .build()
                INSTANCE = instance
                instance
            }
        }
        
        private class DatabaseCallback : RoomDatabase.Callback() {
            override fun onCreate(db: SupportSQLiteDatabase) {
                super.onCreate(db)
                INSTANCE?.let { database ->
                    CoroutineScope(Dispatchers.IO).launch {
                        seedDatabase(database)
                    }
                }
            }
        }
        
        private suspend fun seedDatabase(database: KasirDatabase) {
            val menuItemDao = database.menuItemDao()
            val userDao = database.userDao()
            
            // Seed 24 menu items (exact dari Flask app)
            val menuItems = listOf(
                // Makanan (8 items)
                MenuItemEntity(
                    name = "Nasi Goreng Spesial",
                    category = "Makanan",
                    price = 25000.0,
                    description = "Nasi goreng dengan telur, ayam, dan sayuran",
                    imageUrl = "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Mie Ayam Bakso",
                    category = "Makanan",
                    price = 20000.0,
                    description = "Mie ayam dengan bakso kuah dan pangsit",
                    imageUrl = "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Ayam Goreng Crispy",
                    category = "Makanan",
                    price = 18000.0,
                    description = "Ayam goreng crispy dengan sambal",
                    imageUrl = "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400",
                    isPopular = false
                ),
                MenuItemEntity(
                    name = "Sate Ayam",
                    category = "Makanan",
                    price = 22000.0,
                    description = "10 tusuk sate ayam dengan bumbu kacang",
                    imageUrl = "https://images.unsplash.com/photo-1529563021893-cc83c992d75d?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Nasi Campur",
                    category = "Makanan",
                    price = 22000.0,
                    description = "Nasi dengan lauk pauk lengkap",
                    imageUrl = "https://images.unsplash.com/photo-1606490048664-49e1acb4ebb4?w=400",
                    isPopular = false
                ),
                MenuItemEntity(
                    name = "Rendang",
                    category = "Makanan",
                    price = 30000.0,
                    description = "Rendang daging sapi asli Padang",
                    imageUrl = "https://images.unsplash.com/photo-1595777216528-071e0127ccaf?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Soto Ayam",
                    category = "Makanan",
                    price = 22000.0,
                    description = "Soto ayam kuah kuning dengan nasi",
                    imageUrl = "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Gado-gado",
                    category = "Makanan",
                    price = 18000.0,
                    description = "Gado-gado dengan bumbu kacang",
                    imageUrl = "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=400",
                    isPopular = false
                ),
                
                // Minuman (8 items)
                MenuItemEntity(
                    name = "Es Teh Manis",
                    category = "Minuman",
                    price = 5000.0,
                    description = "Teh manis dingin segar",
                    imageUrl = "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Jus Alpukat",
                    category = "Minuman",
                    price = 15000.0,
                    description = "Jus alpukat segar dengan susu",
                    imageUrl = "https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Kopi Latte",
                    category = "Minuman",
                    price = 18000.0,
                    description = "Kopi latte premium dengan latte art",
                    imageUrl = "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Air Mineral",
                    category = "Minuman",
                    price = 4000.0,
                    description = "Air mineral dalam kemasan",
                    imageUrl = "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400",
                    isPopular = false
                ),
                MenuItemEntity(
                    name = "Es Jeruk",
                    category = "Minuman",
                    price = 8000.0,
                    description = "Jus jeruk segar dengan es",
                    imageUrl = "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Milkshake Coklat",
                    category = "Minuman",
                    price = 20000.0,
                    description = "Milkshake coklat dengan whipped cream",
                    imageUrl = "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Matcha Latte",
                    category = "Minuman",
                    price = 22000.0,
                    description = "Matcha latte premium Jepang",
                    imageUrl = "https://images.unsplash.com/photo-1536013992883-d2aa97c3a8cc?w=400",
                    isPopular = false
                ),
                MenuItemEntity(
                    name = "Boba Milk Tea",
                    category = "Minuman",
                    price = 18000.0,
                    description = "Milk tea dengan boba pearl",
                    imageUrl = "https://images.unsplash.com/photo-1525385133512-2f3bdd039054?w=400",
                    isPopular = true
                ),
                
                // Dessert (8 items)
                MenuItemEntity(
                    name = "Brownies",
                    category = "Dessert",
                    price = 12000.0,
                    description = "Brownies coklat dengan kacang",
                    imageUrl = "https://images.unsplash.com/photo-1607920591413-4ec007e70023?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Pisang Goreng",
                    category = "Dessert",
                    price = 8000.0,
                    description = "Pisang goreng crispy",
                    imageUrl = "https://images.unsplash.com/photo-1587573089046-da4b47a64e50?w=400",
                    isPopular = false
                ),
                MenuItemEntity(
                    name = "Donat Gula",
                    category = "Dessert",
                    price = 7000.0,
                    description = "Donat dengan taburan gula halus",
                    imageUrl = "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Puding Coklat",
                    category = "Dessert",
                    price = 10000.0,
                    description = "Puding coklat lembut",
                    imageUrl = "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400",
                    isPopular = false
                ),
                MenuItemEntity(
                    name = "Es Krim Vanilla",
                    category = "Dessert",
                    price = 15000.0,
                    description = "Es krim vanilla premium 2 scoop",
                    imageUrl = "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Cheesecake Berry",
                    category = "Dessert",
                    price = 25000.0,
                    description = "Cheesecake dengan berry topping",
                    imageUrl = "https://images.unsplash.com/photo-1533134242820-f3684c6e4c3c?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Tiramisu",
                    category = "Dessert",
                    price = 22000.0,
                    description = "Tiramisu klasik Italia",
                    imageUrl = "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400",
                    isPopular = true
                ),
                MenuItemEntity(
                    name = "Waffle Madu",
                    category = "Dessert",
                    price = 18000.0,
                    description = "Waffle dengan madu dan butter",
                    imageUrl = "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=400",
                    isPopular = false
                )
            )
            
            menuItems.forEach { item ->
                menuItemDao.insertMenuItem(item)
            }
            
            // Seed default admin user
            val adminUser = UserEntity(
                username = "admin",
                password = hashPassword("admin123"),
                fullName = "Administrator",
                role = "ADMIN",
                email = "admin@kasir.com",
                phone = "08123456789",
                isActive = true
            )
            userDao.insertUser(adminUser)
        }
        
        private fun hashPassword(password: String): String {
            val md = MessageDigest.getInstance("SHA-256")
            val hash = md.digest(password.toByteArray())
            return hash.joinToString("") { "%02x".format(it) }
        }
    }
}
