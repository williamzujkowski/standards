# TS:unit - Unit Testing Micro Standard (500 tokens max)

## Quick Rules
- 85% coverage minimum
- Test one thing per test
- Fast execution (<100ms per test)
- Independent tests (no order dependency)
- Clear naming: `test_should_[expected]_when_[condition]`

## Test Structure (AAA)
```python
def test_calculate_total_with_discount():
    # Arrange
    cart = ShoppingCart()
    cart.add_item(Item("Book", 10.00))
    
    # Act
    total = cart.calculate_total(discount=0.1)
    
    # Assert
    assert total == 9.00
```

## Mocking
```python
# Mock external dependencies
@patch('requests.get')
def test_fetch_user(mock_get):
    mock_get.return_value.json.return_value = {"id": 1, "name": "Test"}
    user = fetch_user(1)
    assert user.name == "Test"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

## Coverage Requirements
- Overall: 85%
- Critical paths: 95%
- New code: 90%
- Exclude: tests, migrations, configs

## Best Practices
✓ Use fixtures for setup
✓ Parameterize similar tests
✓ Mock external calls
✓ Test edge cases
✓ Test error conditions
✓ Keep tests simple

## Example Fixture
```python
@pytest.fixture
def sample_user():
    return User(email="test@example.com", name="Test User")

def test_user_full_name(sample_user):
    assert sample_user.full_name == "Test User"
```

## Common Assertions
```python
assert result == expected
assert error_func raises ValueError
assert mock.called_with(expected_args)
assert len(items) == 3
assert "substring" in result
```