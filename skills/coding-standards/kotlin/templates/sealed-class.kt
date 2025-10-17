package com.example.app.model

/**
 * Sealed class for UI state management
 * Demonstrates exhaustive when expressions and type-safe state handling
 */
sealed class UiState<out T> {
    /**
     * Initial state - no data loaded yet
     */
    object Initial : UiState<Nothing>()

    /**
     * Loading state - operation in progress
     */
    object Loading : UiState<Nothing>()

    /**
     * Success state with data
     */
    data class Success<T>(val data: T) : UiState<T>()

    /**
     * Error state with message and optional throwable
     */
    data class Error(
        val message: String,
        val throwable: Throwable? = null
    ) : UiState<Nothing>()

    /**
     * Empty state - successful load but no data
     */
    object Empty : UiState<Nothing>()
}

/**
 * Extension functions for UiState
 */
fun <T> UiState<T>.isLoading(): Boolean = this is UiState.Loading
fun <T> UiState<T>.isSuccess(): Boolean = this is UiState.Success
fun <T> UiState<T>.isError(): Boolean = this is UiState.Error

fun <T> UiState<T>.getOrNull(): T? = when (this) {
    is UiState.Success -> data
    else -> null
}

fun <T> UiState<T>.getOrDefault(default: T): T = when (this) {
    is UiState.Success -> data
    else -> default
}

/**
 * Sealed class for network result
 */
sealed class NetworkResult<out T> {
    data class Success<T>(
        val data: T,
        val code: Int = 200
    ) : NetworkResult<T>()

    data class Error(
        val code: Int,
        val message: String,
        val exception: Throwable? = null
    ) : NetworkResult<Nothing>()

    object NetworkError : NetworkResult<Nothing>()
    object Timeout : NetworkResult<Nothing>()
}

/**
 * Transform NetworkResult to UiState
 */
fun <T> NetworkResult<T>.toUiState(): UiState<T> = when (this) {
    is NetworkResult.Success -> UiState.Success(data)
    is NetworkResult.Error -> UiState.Error(message, exception)
    is NetworkResult.NetworkError -> UiState.Error("Network error occurred")
    is NetworkResult.Timeout -> UiState.Error("Request timed out")
}

/**
 * Sealed class for user actions
 */
sealed class UserAction {
    data class LoadUser(val userId: String) : UserAction()
    data class UpdateUser(val userId: String, val name: String) : UserAction()
    data class DeleteUser(val userId: String) : UserAction()
    object RefreshUsers : UserAction()
    data class SearchUsers(val query: String) : UserAction()
}

/**
 * Sealed class for navigation events
 */
sealed class NavigationEvent {
    object NavigateBack : NavigationEvent()
    data class NavigateToDetail(val userId: String) : NavigationEvent()
    data class NavigateToEdit(val userId: String) : NavigationEvent()
    object NavigateToSettings : NavigationEvent()
}

/**
 * Sealed class for form validation
 */
sealed class ValidationResult {
    object Valid : ValidationResult()

    sealed class Invalid : ValidationResult() {
        data class EmptyField(val fieldName: String) : Invalid()
        data class InvalidFormat(val fieldName: String, val format: String) : Invalid()
        data class TooShort(val fieldName: String, val minLength: Int) : Invalid()
        data class TooLong(val fieldName: String, val maxLength: Int) : Invalid()
    }
}

/**
 * Example usage in ViewModel
 */
class ExampleViewModel {
    fun handleState(state: UiState<List<String>>) {
        // Exhaustive when expression (compiler enforces all cases)
        when (state) {
            is UiState.Initial -> showPlaceholder()
            is UiState.Loading -> showLoading()
            is UiState.Success -> showData(state.data)
            is UiState.Error -> showError(state.message)
            is UiState.Empty -> showEmptyState()
        }
    }

    fun handleUserAction(action: UserAction) {
        when (action) {
            is UserAction.LoadUser -> loadUser(action.userId)
            is UserAction.UpdateUser -> updateUser(action.userId, action.name)
            is UserAction.DeleteUser -> deleteUser(action.userId)
            is UserAction.RefreshUsers -> refreshUsers()
            is UserAction.SearchUsers -> searchUsers(action.query)
        }
    }

    fun validateEmail(email: String): ValidationResult {
        return when {
            email.isBlank() -> ValidationResult.Invalid.EmptyField("Email")
            !email.contains("@") -> ValidationResult.Invalid.InvalidFormat("Email", "user@domain.com")
            email.length < 5 -> ValidationResult.Invalid.TooShort("Email", 5)
            email.length > 100 -> ValidationResult.Invalid.TooLong("Email", 100)
            else -> ValidationResult.Valid
        }
    }

    // Placeholder methods
    private fun showPlaceholder() {}
    private fun showLoading() {}
    private fun showData(data: List<String>) {}
    private fun showError(message: String) {}
    private fun showEmptyState() {}
    private fun loadUser(userId: String) {}
    private fun updateUser(userId: String, name: String) {}
    private fun deleteUser(userId: String) {}
    private fun refreshUsers() {}
    private fun searchUsers(query: String) {}
}

/**
 * Sealed interface for more flexibility (Kotlin 1.5+)
 */
sealed interface PaymentMethod {
    data class CreditCard(
        val number: String,
        val cvv: String,
        val expiry: String
    ) : PaymentMethod

    data class PayPal(val email: String) : PaymentMethod

    data class BankTransfer(
        val accountNumber: String,
        val routingNumber: String
    ) : PaymentMethod

    object Cash : PaymentMethod
}
