<!--
  Complete Vue 3 Composition API Component Template
  Demonstrates: TypeScript, props, emits, slots, composables, lifecycle
-->
<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import type { Ref } from 'vue';

// ============================================================================
// Types & Interfaces
// ============================================================================

interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface Props {
  user: User;
  title?: string;
  isEditable?: boolean;
  maxLength?: number;
}

interface Emits {
  update: [user: User];
  delete: [userId: number];
  cancel: [];
}

// ============================================================================
// Props & Emits
// ============================================================================

const props = withDefaults(defineProps<Props>(), {
  title: 'User Profile',
  isEditable: true,
  maxLength: 100
});

const emit = defineEmits<Emits>();

// ============================================================================
// Reactive State
// ============================================================================

const isEditing = ref(false);
const isSaving = ref(false);
const error = ref<string | null>(null);

// Local copy for editing
const localUser = ref<User>({ ...props.user });

// ============================================================================
// Computed Properties
// ============================================================================

const displayName = computed(() => {
  return props.user.name.toUpperCase();
});

const isAdmin = computed(() => {
  return props.user.role === 'admin';
});

const canEdit = computed(() => {
  return props.isEditable && !isSaving.value;
});

const characterCount = computed(() => {
  return localUser.value.name.length;
});

const isValid = computed(() => {
  return (
    localUser.value.name.length > 0 &&
    localUser.value.name.length <= props.maxLength &&
    localUser.value.email.includes('@')
  );
});

// ============================================================================
// Watchers
// ============================================================================

// Watch prop changes
watch(
  () => props.user,
  (newUser) => {
    if (!isEditing.value) {
      localUser.value = { ...newUser };
    }
  },
  { deep: true }
);

// Watch editing state
watch(isEditing, (editing) => {
  if (editing) {
    console.log('Started editing');
  } else {
    console.log('Stopped editing');
  }
});

// ============================================================================
// Methods
// ============================================================================

function startEdit() {
  if (!canEdit.value) return;
  
  isEditing.value = true;
  localUser.value = { ...props.user };
  error.value = null;
}

async function saveEdit() {
  if (!isValid.value) {
    error.value = 'Please enter valid information';
    return;
  }
  
  isSaving.value = true;
  error.value = null;
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    emit('update', localUser.value);
    isEditing.value = false;
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Save failed';
  } finally {
    isSaving.value = false;
  }
}

function cancelEdit() {
  isEditing.value = false;
  localUser.value = { ...props.user };
  error.value = null;
  emit('cancel');
}

function handleDelete() {
  if (window.confirm('Are you sure you want to delete this user?')) {
    emit('delete', props.user.id);
  }
}

// ============================================================================
// Composables
// ============================================================================

// Custom composable for keyboard shortcuts
function useKeyboardShortcuts() {
  function handleKeydown(event: KeyboardEvent) {
    // Cmd/Ctrl + E to edit
    if ((event.metaKey || event.ctrlKey) && event.key === 'e') {
      event.preventDefault();
      startEdit();
    }
    
    // Escape to cancel
    if (event.key === 'Escape' && isEditing.value) {
      cancelEdit();
    }
  }
  
  onMounted(() => {
    window.addEventListener('keydown', handleKeydown);
  });
  
  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown);
  });
}

useKeyboardShortcuts();

// ============================================================================
// Lifecycle Hooks
// ============================================================================

onMounted(() => {
  console.log('Component mounted');
});

onUnmounted(() => {
  console.log('Component unmounted');
});

// ============================================================================
// Expose (for parent component refs)
// ============================================================================

defineExpose({
  startEdit,
  cancelEdit,
  isEditing
});
</script>

<template>
  <div class="user-profile" :class="{ 'is-editing': isEditing }">
    <!-- Header with slot -->
    <header class="profile-header">
      <slot name="header" :title="title" :is-admin="isAdmin">
        <h2>{{ title }}</h2>
        <span v-if="isAdmin" class="badge">Admin</span>
      </slot>
    </header>

    <!-- Error message -->
    <div v-if="error" role="alert" class="error-message">
      {{ error }}
    </div>

    <!-- View mode -->
    <div v-if="!isEditing" class="profile-view">
      <dl>
        <dt>Name:</dt>
        <dd>{{ displayName }}</dd>
        
        <dt>Email:</dt>
        <dd>{{ user.email }}</dd>
        
        <dt>Role:</dt>
        <dd>{{ user.role }}</dd>
      </dl>

      <!-- Scoped slot for custom content -->
      <slot name="content" :user="user" />

      <!-- Actions -->
      <div class="actions">
        <button
          v-if="canEdit"
          @click="startEdit"
          class="btn btn-primary"
          :disabled="!canEdit"
        >
          Edit
        </button>
        
        <button
          v-if="isAdmin"
          @click="handleDelete"
          class="btn btn-danger"
        >
          Delete
        </button>
        
        <!-- Default slot -->
        <slot />
      </div>
    </div>

    <!-- Edit mode -->
    <form v-else @submit.prevent="saveEdit" class="profile-edit">
      <div class="form-group">
        <label for="name">Name:</label>
        <input
          id="name"
          v-model="localUser.name"
          type="text"
          :maxlength="maxLength"
          required
          :disabled="isSaving"
        />
        <span class="character-count">
          {{ characterCount }} / {{ maxLength }}
        </span>
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input
          id="email"
          v-model="localUser.email"
          type="email"
          required
          :disabled="isSaving"
        />
      </div>

      <div class="form-group">
        <label for="role">Role:</label>
        <select
          id="role"
          v-model="localUser.role"
          :disabled="isSaving"
        >
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      <!-- Actions -->
      <div class="actions">
        <button
          type="submit"
          class="btn btn-primary"
          :disabled="!isValid || isSaving"
        >
          {{ isSaving ? 'Saving...' : 'Save' }}
        </button>
        
        <button
          type="button"
          @click="cancelEdit"
          class="btn btn-secondary"
          :disabled="isSaving"
        >
          Cancel
        </button>
      </div>
    </form>

    <!-- Footer slot -->
    <footer>
      <slot name="footer" />
    </footer>
  </div>
</template>

<style scoped>
.user-profile {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
}

.user-profile.is-editing {
  border-color: #2196f3;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.badge {
  padding: 0.25rem 0.5rem;
  background: #ff9800;
  color: white;
  border-radius: 4px;
  font-size: 0.875rem;
}

.error-message {
  padding: 0.75rem;
  margin-bottom: 1rem;
  background: #ffebee;
  color: #c62828;
  border-radius: 4px;
}

.profile-view dl {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.5rem 1rem;
}

.profile-view dt {
  font-weight: 600;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #2196f3;
}

.character-count {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #666;
}

.actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #2196f3;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #1976d2;
}

.btn-secondary {
  background: #e0e0e0;
  color: #333;
}

.btn-secondary:hover:not(:disabled) {
  background: #bdbdbd;
}

.btn-danger {
  background: #f44336;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #d32f2f;
}
</style>
