from django.test import TestCase, Client
from django.urls import reverse
from .models import Product

# Create your tests here.

class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Product.objects.create(name="Product 1", description="Description 1", price=10.00)
        Product.objects.create(name="Product 2", description="Description 2", price=20.00)

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_list.html')
        self.assertContains(response, "Product 1")
        self.assertContains(response, "Product 2")