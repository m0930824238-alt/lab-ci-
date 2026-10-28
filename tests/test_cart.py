import pytest
from unittest.mock import Mock
from shop.cart import Cart


# 1. Параметризований тест з граничними значеннями (знижка)
@pytest.mark.parametrize(("discount", "expected"), [(0, 50.0), (10, 45.0), (50, 25.0), (100, 0.0)])
def test_total_with_various_discounts(
    cart_with_items: Cart, discount: float, expected: float
) -> None:
    assert cart_with_items.total(discount_percent=discount) == expected


# 2. Перевірка винятків (від'ємна ціна, нульова кількість, знижка, курс, відсутній товар)
def test_add_negative_price_raises(empty_cart: Cart) -> None:
    with pytest.raises(ValueError, match="price must be non-negative"):
        empty_cart.add("apple", price=-5.0)


@pytest.mark.parametrize("qty", [0, -1, -10])
def test_add_invalid_qty_raises(empty_cart: Cart, qty: int) -> None:
    with pytest.raises(ValueError, match="qty must be positive"):
        empty_cart.add("apple", price=10.0, qty=qty)


def test_total_invalid_discount_raises(cart_with_items: Cart) -> None:
    with pytest.raises(ValueError, match="discount_percent must be in"):
        cart_with_items.total(discount_percent=110.0)


def test_remove_missing_item_raises(empty_cart: Cart) -> None:
    with pytest.raises(KeyError):
        empty_cart.remove("orange")


def test_total_in_negative_rate_raises(cart_with_items: Cart) -> None:
    rates = Mock()
    rates.get_rate.return_value = -5.0
    with pytest.raises(ValueError, match="rate must be positive"):
        cart_with_items.total_in("USD", rates)


# 3. Тест з Mock (тестовий дублер)
def test_total_in_usd(cart_with_items: Cart) -> None:
    rates = Mock()
    rates.get_rate.return_value = 40.0
    assert cart_with_items.total_in("USD", rates) == 1.25
    rates.get_rate.assert_called_once_with("USD")


# 4. Базові тести функціоналу
def test_items_count(cart_with_items: Cart) -> None:
    assert cart_with_items.items_count() == 4


def test_remove_item(cart_with_items: Cart) -> None:
    cart_with_items.remove("apple")
    assert cart_with_items.items_count() == 1


# 5. TDD: тести для методу most_expensive (якого ще немає)
def test_most_expensive_empty(empty_cart: Cart) -> None:
    assert empty_cart.most_expensive() is None


def test_most_expensive_with_items(cart_with_items: Cart) -> None:
    expensive = cart_with_items.most_expensive()
    assert expensive is not None
    assert expensive.name == "banana"
    assert expensive.price == 20.0


# 6. Фіксація рішення: додавання однакового товару з іншою ціною
def test_add_same_item_different_price(empty_cart: Cart) -> None:
    empty_cart.add("apple", price=10.0)
    with pytest.raises(ValueError, match="Item already exists with a different price"):
        empty_cart.add("apple", price=15.0)
