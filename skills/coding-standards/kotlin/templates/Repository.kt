package com.example.app.data.repository

import com.example.app.data.local.UserDao
import com.example.app.data.remote.ApiService
import com.example.app.model.User
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository pattern implementation with Flow
 * Demonstrates single source of truth, caching, and error handling
 */
@Singleton
class UserRepository @Inject constructor(
    private val apiService: ApiService,
    private val userDao: UserDao
) {

    /**
     * Get users as Flow (reactive)
     * Database is single source of truth
     */
    fun getUsers(): Flow<List<User>> {
        return userDao.getUsersFlow()
            .onStart { refreshUsers() }
            .catch { e ->
                emit(emptyList())
                throw RepositoryException("Failed to load users", e)
            }
    }

    /**
     * Get single user by ID
     */
    fun getUser(userId: String): Flow<User?> {
        return userDao.getUserFlow(userId)
            .onStart {
                // Fetch from network if not in cache
                fetchAndCacheUser(userId)
            }
    }

    /**
     * Get active users only
     */
    fun getActiveUsers(): Flow<List<User>> {
        return userDao.getUsersFlow()
            .map { users -> users.filter { it.isActive } }
            .distinctUntilChanged()
    }

    /**
     * Search users by name or email
     */
    fun searchUsers(query: String): Flow<List<User>> {
        return userDao.searchUsers("%$query%")
    }

    /**
     * Save user (create or update)
     */
    suspend fun saveUser(user: User) {
        withContext(Dispatchers.IO) {
            try {
                // Save to network
                apiService.saveUser(user)

                // Update local cache
                userDao.insertUser(user)
            } catch (e: Exception) {
                throw RepositoryException("Failed to save user", e)
            }
        }
    }

    /**
     * Delete user
     */
    suspend fun deleteUser(userId: String) {
        withContext(Dispatchers.IO) {
            try {
                apiService.deleteUser(userId)
                userDao.deleteUser(userId)
            } catch (e: Exception) {
                throw RepositoryException("Failed to delete user", e)
            }
        }
    }

    /**
     * Refresh users from network
     */
    suspend fun refreshUsers() {
        withContext(Dispatchers.IO) {
            try {
                val users = apiService.getUsers()
                userDao.deleteAllUsers()
                userDao.insertUsers(users)
            } catch (e: Exception) {
                // Fail silently, use cached data
                // In production, log error or emit specific state
            }
        }
    }

    /**
     * Fetch single user from network and cache
     */
    private suspend fun fetchAndCacheUser(userId: String) {
        withContext(Dispatchers.IO) {
            try {
                val user = apiService.getUser(userId)
                userDao.insertUser(user)
            } catch (e: Exception) {
                // Use cached version if available
            }
        }
    }

    /**
     * Sync local changes to server
     */
    suspend fun syncPendingChanges() {
        withContext(Dispatchers.IO) {
            val pendingUsers = userDao.getPendingUsers()

            pendingUsers.forEach { user ->
                try {
                    apiService.saveUser(user)
                    userDao.updateUser(user.copy(isPending = false))
                } catch (e: Exception) {
                    // Keep as pending, will retry later
                }
            }
        }
    }

    /**
     * Clear all cached data
     */
    suspend fun clearCache() {
        withContext(Dispatchers.IO) {
            userDao.deleteAllUsers()
        }
    }
}

/**
 * Repository-specific exception
 */
class RepositoryException(
    message: String,
    cause: Throwable? = null
) : Exception(message, cause)

/**
 * Result wrapper for operations
 */
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

/**
 * Extension to convert Flow to Result Flow
 */
fun <T> Flow<T>.asResult(): Flow<Result<T>> {
    return this
        .map<T, Result<T>> { Result.Success(it) }
        .onStart { emit(Result.Loading) }
        .catch { emit(Result.Error(Exception(it))) }
}
