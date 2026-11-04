from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP


def money(amount):
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass(eq=False)
class Product:
    name: str
    price: Decimal
    stock: int
    category: str


@dataclass(frozen=True)
class Order:
    items: tuple
    subtotal: Decimal
    discount: Decimal
    tax: Decimal

    @property
    def total(self):
        return self.subtotal - self.discount + self.tax

    @classmethod
    def checkout(cls, cart, customer, discount_rate=Decimal(0), tax_rate=Decimal(0)):
        if not Decimal(0) <= discount_rate <= Decimal(1) or tax_rate < 0:
            raise ValueError("Некорректная ставка скидки или налога.")

        entries = tuple(cart.items.items())
        if not entries:
            raise ValueError("Корзина пуста.")
        for product, quantity in entries:
            if quantity > product.stock:
                raise ValueError(f"Товара «{product.name}» не хватает на складе.")

        items = tuple((p.name, p.price, q) for p, q in entries)
        subtotal = money(sum(price * quantity for _, price, quantity in items))
        discount = money(subtotal * discount_rate)
        tax = money((subtotal - discount) * tax_rate)
        order = cls(items, subtotal, discount, tax)

        for product, quantity in entries:
            product.stock -= quantity
        customer.orders.append(order)
        cart.items.clear()
        return order


@dataclass
class Customer:
    name: str
    email: str
    orders: list[Order] = field(default_factory=list)


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add(self, product, quantity=1):
        if type(quantity) is not int or quantity < 1:
            raise ValueError("Количество должно быть положительным целым числом.")
        self.update_quantity(product, self.items.get(product, 0) + quantity)

    def remove(self, product):
        self.items.pop(product, None)

    def update_quantity(self, product, quantity):
        if type(quantity) is not int or not 0 <= quantity <= product.stock:
            raise ValueError("Недопустимое количество товара.")
        if quantity == 0:
            self.remove(product)
        else:
            self.items[product] = quantity


if __name__ == "__main__":
    book = Product("Учебник Python", Decimal("1200.00"), 5, "Книги")
    pen = Product("Ручка", Decimal("80.00"), 10, "Канцтовары")
    customer = Customer("Анна", "anna@example.com")
    cart = ShoppingCart()
    cart.add(book)
    cart.update_quantity(book, 2)
    cart.add(pen)
    cart.remove(pen)
    order = Order.checkout(cart, customer, Decimal("0.10"), Decimal("0.20"))
    print(f"Сумма товаров — {order.subtotal} руб.")
    print(f"Скидка — {order.discount} руб., налог — {order.tax} руб.")
    print(f"Итого — {order.total} руб.")
    print(f"Заказов у покупателя — {len(customer.orders)}")
