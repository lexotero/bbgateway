import random
from datetime import datetime
from unittest import TestCase

from bbgateway import *


def generate_random_ip():
    return str(random.choice(range(0,255))) + "." + str(random.choice(range(0,255))) + "." + str(random.choice(range(0,255))) + "." + str(random.choice(range(0,255)))


def generate_random_order():
    tax = random.random() * 100
    shipping_price = random.random() * 100
    total_amount = '{0:.2f}'.format(float(tax + shipping_price))
    return Order(datetime.now().strftime('%H%M%S%f%d%m%Y'), "Big Order", total_amount, generate_random_ip())


class TestMerchant(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.merchant = Merchant("demo", "password")
        cls.shipping = Shipping(first_name="John", last_name="Smith", address_1="123 Main St", city="Beverly Hills",
                                state="CA", zip="90210", country="US", email="support@example.com")
        cls.billing = Billing(first_name="John", last_name="Smith", address_1="123 Main St", city="Beverly Hills",
                              state="CA", zip="90210", country="US", phone="555-555-5556", email="support@example.com")
        cls.credit_card = CreditCard("4111111111111111", "1212", '999')

    def test_authorization(self):
        response = self.merchant.authorization(generate_random_order(), self.shipping, self.billing, self.credit_card)
        self.assertEquals(response['response'], "1")

    def test_sale(self):
        response = self.merchant.sale(generate_random_order(), self.shipping, self.billing, self.credit_card)
        self.assertEquals(response['response'], "1")

    def test_capture(self):
        order = generate_random_order()
        response = self.merchant.authorization(order, self.shipping, self.billing, self.credit_card)
        transaction_id = response['transactionid']
        amount = order.amount
        response = self.merchant.capture(transaction_id, amount)
        self.assertEquals(response['response'], "1")
