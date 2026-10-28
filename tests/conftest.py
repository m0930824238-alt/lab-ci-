import pytest

from shop.cart import Cart


@pytest.fixture
def empty_cart() -> Cart:
    """Фікстура: порожній кошик."""
    return Cart()


@pytest.fixture
def cart_with_items() -> Cart:
    """Фікстура: кошик з двома товарами."""
    cart = Cart()
    cart.add("apple", price=10.0, qty=3)
    cart.add("banana", price=20.0, qty=1)
    return cart
