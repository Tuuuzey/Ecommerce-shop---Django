from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Products
from checkout.models import PromoCode, Address, Transaction, Order, OrderItem
from seller.models import SellerUser

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.seller = SellerUser.objects.create(user=self.user, phone_number='123456789')
        self.product = Products.objects.create(
            name='Test Product',
            price=100.00,
            discount_price=80.00,
            category='electronics',
            description='A test product',
            image='test.jpg',
            seller=self.seller
        )
        self.promo_code = PromoCode.objects.create(code='DISCOUNT10', value=10)
        self.address = Address.objects.create(
            first_name='John', last_name='Doe', username='testuser',
            id_username=self.user, email='john@example.com',
            address='123 Test Street', phone_number=1234567890,
            country='Testland', city='Test City', zip='12345'
        )
        self.transaction = Transaction.objects.create(
            id_username=self.address, method='Credit Card',
            status='Completed', total=90.00, currency='USD'
        )
        self.order = Order.objects.create(
            user=self.user, address=self.address, transaction=self.transaction,
            promo_code=self.promo_code, total=90.00
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1, price=100.00, discount_price=80.00
        )

    def test_promo_code_str(self):
        self.assertEqual(str(self.promo_code), 'DISCOUNT10 10')

    def test_address_str(self):
        self.assertEqual(str(self.address), f'testuser {self.address.id}')

    def test_transaction_str(self):
        self.assertEqual(str(self.transaction), str(self.transaction.id_transaction))

    def test_order_str(self):
        self.assertEqual(str(self.order), f'Order {self.order.id} by testuser')

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), f'Order items {self.order.id}')

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_seller_user_str(self):
        self.assertEqual(str(self.seller), 'testuser')
