package com.kasir.data.local.database.dao

import androidx.room.*
import com.kasir.data.local.database.entities.UserEntity

@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE username = :username LIMIT 1")
    suspend fun getUserByUsername(username: String): UserEntity?
    
    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getUserById(id: Int): UserEntity?
    
    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insert(user: UserEntity): Long
    
    @Query("SELECT COUNT(*) FROM users")
    suspend fun getUserCount(): Int
    
    @Update
    suspend fun update(user: UserEntity)
    
    @Delete
    suspend fun delete(user: UserEntity)
}
