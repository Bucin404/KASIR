package com.kasir.services

import com.auth0.jwt.JWT
import com.auth0.jwt.algorithms.Algorithm
import com.kasir.models.*
import com.kasir.repositories.DatabaseRepository
import org.mindrot.jbcrypt.BCrypt
import java.util.*

class AuthService(private val database: DatabaseRepository) {
    
    private val secret = System.getenv("JWT_SECRET") ?: "kasir-secret-key-change-in-production"
    private val algorithm = Algorithm.HMAC256(secret)
    
    fun register(registration: UserRegistration): User? {
        return database.createUser(registration)
    }
    
    fun login(credentials: UserCredentials): AuthResponse? {
        val (user, passwordHash) = database.getUserByUsername(credentials.username) ?: return null
        
        if (!BCrypt.checkpw(credentials.password, passwordHash)) {
            return null
        }
        
        val token = generateToken(user)
        return AuthResponse(token = token, user = user)
    }
    
    fun generateToken(user: User): String {
        return JWT.create()
            .withIssuer("kasir-kotlin")
            .withSubject(user.id.toString())
            .withClaim("username", user.username)
            .withClaim("role", user.role.name)
            .withExpiresAt(Date(System.currentTimeMillis() + 24 * 60 * 60 * 1000)) // 24 hours
            .sign(algorithm)
    }
    
    fun verifyToken(token: String): Int? {
        return try {
            val verifier = JWT.require(algorithm)
                .withIssuer("kasir-kotlin")
                .build()
            val jwt = verifier.verify(token)
            jwt.subject.toInt()
        } catch (e: Exception) {
            null
        }
    }
    
    fun hasRole(userId: Int, requiredRole: UserRole): Boolean {
        // TODO: Implement role checking from database
        return true
    }
}
