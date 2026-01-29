package com.kasir.data.local.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.sqlite.db.SupportSQLiteDatabase
import com.kasir.data.local.database.dao.*
import com.kasir.data.local.database.entities.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

@Database(
    entities = [
        MenuItemEntity::class,
        TransactionEntity::class,
        TransactionItemEntity::class,
        ExpenseEntity::class,
        UserEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class KasirDatabase : RoomDatabase() {
    abstract fun menuItemDao(): MenuItemDao
    abstract fun transactionDao(): TransactionDao
    abstract fun expenseDao(): ExpenseDao
    abstract fun userDao(): UserDao
    
    companion object {
        @Volatile
        private var INSTANCE: KasirDatabase? = null
        private val applicationScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
        
        fun getDatabase(context: Context): KasirDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    KasirDatabase::class.java,
                    "kasir_database"
                )
                    .fallbackToDestructiveMigration()
                    .addCallback(DatabaseCallback(applicationScope))
                    .build()
                INSTANCE = instance
                instance
            }
        }
        
        private class DatabaseCallback(
            private val scope: CoroutineScope
        ) : RoomDatabase.Callback() {
            override fun onCreate(db: SupportSQLiteDatabase) {
                super.onCreate(db)
                INSTANCE?.let { database ->
                    scope.launch {
                        populateDatabase(database.menuItemDao(), database.userDao())
                    }
                }
            }
        }
        
        private suspend fun populateDatabase(menuDao: MenuItemDao, userDao: UserDao) {
            // Clear existing data
            menuDao.deleteAll()
            
            // Insert 24 menu items (exact dari Flask app)
            val menuItems = listOf(
                // Makanan (8 items)
                MenuItemEntity(
                    id = 1,
                    name = "Nasi Goreng Spesial",
                    price = 25000,
                    category = "Makanan",
                    imageUrl = "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=300&h=200&fit=crop&auto=format",
                    description = "Nasi goreng dengan telur, ayam, dan sayuran segar",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 2,
                    name = "Mie Ayam Bakso",
                    price = 20000,
                    category = "Makanan",
                    imageUrl = "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=300&h=200&fit=crop&auto=format",
                    description = "Mie ayam dengan bakso sapi pilihan",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 3,
                    name = "Ayam Goreng Crispy",
                    price = 18000,
                    category = "Makanan",
                    imageUrl = "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=300&h=200&fit=crop&auto=format",
                    description = "Ayam goreng crispy dengan bumbu rempah",
                    isPopular = false
                ),
                MenuItemEntity(
                    id = 4,
                    name = "Sate Ayam (10 tusuk)",
                    price = 22000,
                    category = "Makanan",
                    imageUrl = "https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?w=300&h=200&fit=crop&auto=format",
                    description = "Sate ayam dengan bumbu kacang spesial",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 5,
                    name = "Nasi Campur Komplit",
                    price = 22000,
                    category = "Makanan",
                    imageUrl = "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200&fit=crop&auto=format",
                    description = "Nasi dengan lauk lengkap dan sayuran",
                    isPopular = false
                ),
                MenuItemEntity(
                    id = 6,
                    name = "Rendang Daging Sapi",
                    price = 30000,
                    category = "Makanan",
                    imageUrl = "https://images.unsplash.com/photo-1555939614-8674f6df1389?w=300&h=200&fit=crop&auto=format",
                    description = "Rendang daging sapi dengan bumbu rempah pilihan",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 7,
                    name = "Soto Ayam Lamongan",
                    price = 22000,
                    category = "Makanan",
                    imageUrl = "https://images.unsplash.com/photo-1553909489-cd47e0907980?w=300&h=200&fit=crop&auto=format",
                    description = "Soto ayam dengan bumbu koya dan sambal",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 8,
                    name = "Gado-gado",
                    price = 18000,
                    category = "Makanan",
                    imageUrl = "https://images.unsplash.com/photo-1559054663-e8d23213f55c?w=300&h=200&fit=crop&auto=format",
                    description = "Sayuran segar dengan bumbu kacang khas",
                    isPopular = false
                ),
                
                // Minuman (8 items)
                MenuItemEntity(
                    id = 9,
                    name = "Es Teh Manis",
                    price = 5000,
                    category = "Minuman",
                    imageUrl = "https://images.unsplash.com/photo-1597481499753-6e63aca6d3f3?w=300&h=200&fit=crop&auto=format",
                    description = "Es teh manis dengan gula aren",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 10,
                    name = "Jus Alpukat",
                    price = 15000,
                    category = "Minuman",
                    imageUrl = "https://images.unsplash.com/photo-1623063878630-7c10b5f6d0c9?w=300&h=200&fit=crop&auto=format",
                    description = "Jus alpukat segar dengan susu kental",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 11,
                    name = "Kopi Latte",
                    price = 18000,
                    category = "Minuman",
                    imageUrl = "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=200&fit=crop&auto=format",
                    description = "Kopi latte dengan susu segar",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 12,
                    name = "Air Mineral",
                    price = 4000,
                    category = "Minuman",
                    imageUrl = "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=300&h=200&fit=crop&auto=format",
                    description = "Air mineral botolan 600ml",
                    isPopular = false
                ),
                MenuItemEntity(
                    id = 13,
                    name = "Es Jeruk Segar",
                    price = 8000,
                    category = "Minuman",
                    imageUrl = "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=300&h=200&fit=crop&auto=format",
                    description = "Es jeruk peras tanpa biji",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 14,
                    name = "Milkshake Coklat",
                    price = 20000,
                    category = "Minuman",
                    imageUrl = "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=300&h=200&fit=crop&auto=format",
                    description = "Milkshake coklat dengan topping whipped cream",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 15,
                    name = "Matcha Latte",
                    price = 22000,
                    category = "Minuman",
                    imageUrl = "https://images.unsplash.com/photo-1561047029-3000c68339ca?w=300&h=200&fit=crop&auto=format",
                    description = "Matcha latte dengan susu oat",
                    isPopular = false
                ),
                MenuItemEntity(
                    id = 16,
                    name = "Boba Milk Tea",
                    price = 18000,
                    category = "Minuman",
                    imageUrl = "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=300&h=200&fit=crop&auto=format",
                    description = "Milk tea dengan bubble boba",
                    isPopular = true
                ),
                
                // Dessert (8 items)
                MenuItemEntity(
                    id = 17,
                    name = "Brownies Coklat",
                    price = 12000,
                    category = "Dessert",
                    imageUrl = "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=300&h=200&fit=crop&auto=format",
                    description = "Brownies coklat premium dengan kacang",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 18,
                    name = "Pisang Goreng",
                    price = 8000,
                    category = "Dessert",
                    imageUrl = "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop&auto=format",
                    description = "Pisang goreng dengan keju parut",
                    isPopular = false
                ),
                MenuItemEntity(
                    id = 19,
                    name = "Donat Gula",
                    price = 7000,
                    category = "Dessert",
                    imageUrl = "https://images.unsplash.com/photo-1551106652-a5bcf4b29ab6?w=300&h=200&fit=crop&auto=format",
                    description = "Donat lembut dengan taburan gula",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 20,
                    name = "Puding Coklat",
                    price = 10000,
                    category = "Dessert",
                    imageUrl = "https://images.unsplash.com/photo-1623334044303-241021148842?w=300&h=200&fit=crop&auto=format",
                    description = "Puding coklat dengan saus karamel",
                    isPopular = false
                ),
                MenuItemEntity(
                    id = 21,
                    name = "Es Krim Vanilla",
                    price = 15000,
                    category = "Dessert",
                    imageUrl = "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop&auto=format",
                    description = "Es krim vanilla dengan topping coklat",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 22,
                    name = "Cheesecake Berry",
                    price = 25000,
                    category = "Dessert",
                    imageUrl = "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=300&h=200&fit=crop&auto=format",
                    description = "Cheesecake dengan saus berry segar",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 23,
                    name = "Tiramisu",
                    price = 22000,
                    category = "Dessert",
                    imageUrl = "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=300&h=200&fit=crop&auto=format",
                    description = "Tiramisu klasik Italia",
                    isPopular = true
                ),
                MenuItemEntity(
                    id = 24,
                    name = "Waffle Madu",
                    price = 18000,
                    category = "Dessert",
                    imageUrl = "https://images.unsplash.com/photo-1562376552-0d160a2f238d?w=300&h=200&fit=crop&auto=format",
                    description = "Waffle renyah dengan madu dan buah",
                    isPopular = false
                )
            )
            
            menuDao.insertAll(menuItems)
            
            // Insert default admin user
            // Simple hash for demo - gunakan BCrypt di production
            val adminUser = UserEntity(
                username = "admin",
                email = "admin@kasir.com",
                passwordHash = "admin123".hashCode().toString(), // Simple hash
                role = "ADMIN",
                createdAt = System.currentTimeMillis()
            )
            
            try {
                userDao.insert(adminUser)
            } catch (e: Exception) {
                // User already exists, ignore
            }
        }
    }
}
