/**
 * Vitest Component Test Template
 * Demonstrates: component testing, user interactions, async operations, mocking
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { mount, VueWrapper } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import UserProfile from '@/components/UserProfile.vue';
import { useUserStore } from '@/stores/user';

// ============================================================================
// Test Setup
// ============================================================================

describe('UserProfile', () => {
  let wrapper: VueWrapper;
  let pinia: ReturnType<typeof createPinia>;

  // Sample test data
  const mockUser = {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    role: 'user' as const
  };

  beforeEach(() => {
    // Create fresh Pinia instance for each test
    pinia = createPinia();
    setActivePinia(pinia);
  });

  afterEach(() => {
    // Cleanup after each test
    if (wrapper) {
      wrapper.unmount();
    }
  });

  // ==========================================================================
  // Rendering Tests
  // ==========================================================================

  describe('Rendering', () => {
    it('renders user information correctly', () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      expect(wrapper.text()).toContain('John Doe');
      expect(wrapper.text()).toContain('john@example.com');
      expect(wrapper.text()).toContain('user');
    });

    it('displays admin badge for admin users', () => {
      const adminUser = { ...mockUser, role: 'admin' as const };
      
      wrapper = mount(UserProfile, {
        props: { user: adminUser },
        global: { plugins: [pinia] }
      });

      expect(wrapper.find('.badge').exists()).toBe(true);
      expect(wrapper.find('.badge').text()).toBe('Admin');
    });

    it('renders custom header via slot', () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        slots: {
          header: '<h1>Custom Header</h1>'
        },
        global: { plugins: [pinia] }
      });

      expect(wrapper.find('h1').text()).toBe('Custom Header');
    });

    it('hides edit button when not editable', () => {
      wrapper = mount(UserProfile, {
        props: {
          user: mockUser,
          isEditable: false
        },
        global: { plugins: [pinia] }
      });

      expect(wrapper.find('button.btn-primary').exists()).toBe(false);
    });
  });

  // ==========================================================================
  // User Interaction Tests
  // ==========================================================================

  describe('User Interactions', () => {
    it('enters edit mode when edit button clicked', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      await wrapper.find('button.btn-primary').trigger('click');

      expect(wrapper.classes()).toContain('is-editing');
      expect(wrapper.find('form').exists()).toBe(true);
    });

    it('updates local state when editing', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      // Enter edit mode
      await wrapper.find('button.btn-primary').trigger('click');

      // Update name field
      const nameInput = wrapper.find('input#name');
      await nameInput.setValue('Jane Smith');

      expect((nameInput.element as HTMLInputElement).value).toBe('Jane Smith');
    });

    it('emits update event when form submitted', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      // Enter edit mode
      await wrapper.find('button.btn-primary').trigger('click');

      // Update fields
      await wrapper.find('input#name').setValue('Jane Smith');
      await wrapper.find('input#email').setValue('jane@example.com');

      // Submit form
      await wrapper.find('form').trigger('submit.prevent');

      // Wait for async operations
      await wrapper.vm.$nextTick();

      // Check emitted event
      expect(wrapper.emitted('update')).toBeTruthy();
      expect(wrapper.emitted('update')?.[0]).toEqual([
        {
          id: 1,
          name: 'Jane Smith',
          email: 'jane@example.com',
          role: 'user'
        }
      ]);
    });

    it('cancels editing and resets state', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      // Enter edit mode
      await wrapper.find('button.btn-primary').trigger('click');

      // Change name
      await wrapper.find('input#name').setValue('Changed Name');

      // Cancel
      await wrapper.find('button.btn-secondary').trigger('click');

      // Should exit edit mode
      expect(wrapper.classes()).not.toContain('is-editing');
      
      // Should emit cancel event
      expect(wrapper.emitted('cancel')).toBeTruthy();
    });

    it('confirms before deleting', async () => {
      const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(true);
      
      wrapper = mount(UserProfile, {
        props: { user: { ...mockUser, role: 'admin' } },
        global: { plugins: [pinia] }
      });

      await wrapper.find('button.btn-danger').trigger('click');

      expect(confirmSpy).toHaveBeenCalledWith(
        'Are you sure you want to delete this user?'
      );
      expect(wrapper.emitted('delete')).toBeTruthy();
      expect(wrapper.emitted('delete')?.[0]).toEqual([1]);

      confirmSpy.mockRestore();
    });
  });

  // ==========================================================================
  // Validation Tests
  // ==========================================================================

  describe('Validation', () => {
    it('disables save button for invalid email', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      await wrapper.find('button.btn-primary').trigger('click');
      await wrapper.find('input#email').setValue('invalid-email');

      const saveButton = wrapper.find('form button[type="submit"]');
      expect((saveButton.element as HTMLButtonElement).disabled).toBe(true);
    });

    it('shows character count for name field', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser, maxLength: 50 },
        global: { plugins: [pinia] }
      });

      await wrapper.find('button.btn-primary').trigger('click');
      await wrapper.find('input#name').setValue('Test Name');

      expect(wrapper.find('.character-count').text()).toBe('9 / 50');
    });

    it('enforces max length on name field', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser, maxLength: 10 },
        global: { plugins: [pinia] }
      });

      await wrapper.find('button.btn-primary').trigger('click');

      const nameInput = wrapper.find('input#name');
      expect(nameInput.attributes('maxlength')).toBe('10');
    });
  });

  // ==========================================================================
  // Computed Properties Tests
  // ==========================================================================

  describe('Computed Properties', () => {
    it('computes display name correctly', () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      expect(wrapper.text()).toContain('JOHN DOE');
    });

    it('identifies admin users', () => {
      const adminUser = { ...mockUser, role: 'admin' as const };
      
      wrapper = mount(UserProfile, {
        props: { user: adminUser },
        global: { plugins: [pinia] }
      });

      expect(wrapper.vm.isAdmin).toBe(true);
    });
  });

  // ==========================================================================
  // Async Operations Tests
  // ==========================================================================

  describe('Async Operations', () => {
    it('shows loading state during save', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      await wrapper.find('button.btn-primary').trigger('click');
      
      // Trigger save
      const savePromise = wrapper.find('form').trigger('submit.prevent');

      // Check loading state
      await wrapper.vm.$nextTick();
      const saveButton = wrapper.find('form button[type="submit"]');
      expect(saveButton.text()).toBe('Saving...');

      // Wait for completion
      await savePromise;
      await new Promise(resolve => setTimeout(resolve, 1100));
      await wrapper.vm.$nextTick();
    });

    it('handles save errors gracefully', async () => {
      // Mock failed API call
      vi.spyOn(window, 'setTimeout').mockImplementation((cb: any) => {
        throw new Error('Network error');
      });

      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      await wrapper.find('button.btn-primary').trigger('click');
      await wrapper.find('form').trigger('submit.prevent');
      await wrapper.vm.$nextTick();

      // Should remain in edit mode
      expect(wrapper.classes()).toContain('is-editing');
    });
  });

  // ==========================================================================
  // Store Integration Tests
  // ==========================================================================

  describe('Store Integration', () => {
    it('updates store when user changes', async () => {
      const store = useUserStore(pinia);
      
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      // Simulate store update
      store.user = { ...mockUser, name: 'Updated Name' };
      await wrapper.vm.$nextTick();

      // Component should not update (prop hasn't changed)
      expect(wrapper.text()).toContain('John Doe');
    });
  });

  // ==========================================================================
  // Accessibility Tests
  // ==========================================================================

  describe('Accessibility', () => {
    it('has proper form labels', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      await wrapper.find('button.btn-primary').trigger('click');

      const nameLabel = wrapper.find('label[for="name"]');
      const emailLabel = wrapper.find('label[for="email"]');

      expect(nameLabel.exists()).toBe(true);
      expect(emailLabel.exists()).toBe(true);
    });

    it('shows error with role="alert"', async () => {
      wrapper = mount(UserProfile, {
        props: { user: mockUser },
        global: { plugins: [pinia] }
      });

      // Force error state
      await wrapper.find('button.btn-primary').trigger('click');
      await wrapper.find('input#email').setValue('');
      await wrapper.find('form').trigger('submit.prevent');
      await wrapper.vm.$nextTick();

      const errorMessage = wrapper.find('[role="alert"]');
      expect(errorMessage.exists()).toBe(true);
    });
  });
});
