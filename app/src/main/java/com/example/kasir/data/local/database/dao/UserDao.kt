package com.example.kasir.data.local.database.dao

import androidx.room.*
import com.example.kasir.data.local.database.entities.UserEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface UserDao {
    
    @Query("SELECT * FROM users WHERE username = :username AND isActive = 1")
    suspend fun getUserByUsername(username: String): UserEntity?
    
    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun getUserById(id: Long): UserEntity?
    
    @Query("SELECT * FROM users WHERE isActive = 1 ORDER BY fullName")
    fun getAllUsers(): Flow<List<UserEntity>>
    
    @Query("SELECT * FROM users WHERE role = :role AND isActive = 1")
    fun getUsersByRole(role: String): Flow<List<UserEntity>>
    
    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertUser(user: UserEntity): Long
    
    @Update
    suspend fun updateUser(user: UserEntity)
    
    @Query("UPDATE users SET lastLoginAt = :timestamp WHERE id = :userId")
    suspend fun updateLastLogin(userId: Long, timestamp: Long)
    
    @Query("UPDATE users SET isActive = 0 WHERE id = :userId")
    suspend fun deactivateUser(userId: Long)
    
    @Delete
    suspend fun deleteUser(user: UserEntity)
}
