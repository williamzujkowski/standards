package com.example.app.ui.user

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.app.data.repository.UserRepository
import com.example.app.model.User
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * ViewModel for user management screen
 * Demonstrates coroutines, StateFlow, SharedFlow, and error handling
 */
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository
) : ViewModel() {

    // UI state using StateFlow
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    // One-time events using SharedFlow
    private val _events = MutableSharedFlow<UserEvent>()
    val events: SharedFlow<UserEvent> = _events.asSharedFlow()

    // Search query
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    // Filtered users based on search
    val filteredUsers: StateFlow<List<User>> = combine(
        uiState,
        searchQuery
    ) { state, query ->
        when (state) {
            is UiState.Success -> {
                if (query.isBlank()) {
                    state.users
                } else {
                    state.users.filter { user ->
                        user.name.contains(query, ignoreCase = true) ||
                            user.email.contains(query, ignoreCase = true)
                    }
                }
            }
            else -> emptyList()
        }
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = emptyList()
    )

    init {
        loadUsers()
    }

    /**
     * Load users from repository
     */
    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading

            try {
                userRepository.getUsers()
                    .catch { exception ->
                        _uiState.value = UiState.Error(
                            exception.message ?: "Unknown error occurred"
                        )
                        _events.emit(UserEvent.ShowError(exception.message))
                    }
                    .collect { users ->
                        _uiState.value = UiState.Success(users)
                    }
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Unknown error")
                _events.emit(UserEvent.ShowError(e.message))
            }
        }
    }

    /**
     * Create a new user
     */
    fun createUser(name: String, email: String) {
        viewModelScope.launch {
            try {
                val user = User(
                    id = generateUserId(),
                    name = name,
                    email = email,
                    isActive = true
                )

                userRepository.saveUser(user)
                _events.emit(UserEvent.UserCreated(user))
                loadUsers() // Refresh list
            } catch (e: Exception) {
                _events.emit(UserEvent.ShowError("Failed to create user: ${e.message}"))
            }
        }
    }

    /**
     * Update existing user
     */
    fun updateUser(userId: String, name: String, email: String) {
        viewModelScope.launch {
            try {
                val currentState = _uiState.value
                if (currentState !is UiState.Success) {
                    _events.emit(UserEvent.ShowError("Cannot update user while loading"))
                    return@launch
                }

                val user = currentState.users.find { it.id == userId }
                if (user == null) {
                    _events.emit(UserEvent.ShowError("User not found"))
                    return@launch
                }

                val updatedUser = user.copy(
                    name = name,
                    email = email
                )

                userRepository.saveUser(updatedUser)
                _events.emit(UserEvent.UserUpdated(updatedUser))
                loadUsers()
            } catch (e: Exception) {
                _events.emit(UserEvent.ShowError("Failed to update user: ${e.message}"))
            }
        }
    }

    /**
     * Delete user
     */
    fun deleteUser(userId: String) {
        viewModelScope.launch {
            try {
                userRepository.deleteUser(userId)
                _events.emit(UserEvent.UserDeleted(userId))
                loadUsers()
            } catch (e: Exception) {
                _events.emit(UserEvent.ShowError("Failed to delete user: ${e.message}"))
            }
        }
    }

    /**
     * Update search query
     */
    fun updateSearchQuery(query: String) {
        _searchQuery.value = query
    }

    /**
     * Toggle user active status
     */
    fun toggleUserActiveStatus(userId: String) {
        viewModelScope.launch {
            try {
                val currentState = _uiState.value
                if (currentState !is UiState.Success) return@launch

                val user = currentState.users.find { it.id == userId } ?: return@launch
                val updatedUser = user.copy(isActive = !user.isActive)

                userRepository.saveUser(updatedUser)
                loadUsers()
            } catch (e: Exception) {
                _events.emit(UserEvent.ShowError("Failed to update status: ${e.message}"))
            }
        }
    }

    /**
     * Refresh users (pull-to-refresh)
     */
    fun refreshUsers() {
        loadUsers()
    }

    private fun generateUserId(): String {
        return "user_${System.currentTimeMillis()}"
    }
}

/**
 * UI State sealed class
 */
sealed class UiState {
    object Loading : UiState()
    data class Success(val users: List<User>) : UiState()
    data class Error(val message: String) : UiState()
}

/**
 * One-time events
 */
sealed class UserEvent {
    data class ShowError(val message: String?) : UserEvent()
    data class UserCreated(val user: User) : UserEvent()
    data class UserUpdated(val user: User) : UserEvent()
    data class UserDeleted(val userId: String) : UserEvent()
}
