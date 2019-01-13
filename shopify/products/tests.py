import json
from collections import OrderedDict
from django.test import TestCase
from .models import Product
from shopify.schema import schema

class ProductQueryTest(TestCase):
    def setUp(self):
        Product.objects.create(id=1, title="FIFA 19", price="29.99", inventory_count=5)
        Product.objects.create(id=2, title="Fallout 4", price="39.99", inventory_count=5)
        Product.objects.create(id=3, title="Star Wars Battlefront ||", price="19.99", inventory_count=5)
        Product.objects.create(id=4, title="Gears of War 3", price="9.99", inventory_count=0)

    def test_all_products(self):
        """ Fetch all fields for products in db """

        query = """
            query
            {
                allProducts
                {
                    id
                    title
                    price
                    inventoryCount
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "allProducts": [
                        {
                            "id": "1",
                            "title": "FIFA 19",
                            "price": 29.99,
                            "inventoryCount": 5
                        },
                        {
                            "id": "2",
                            "title": "Fallout 4",
                            "price": 39.99,
                            "inventoryCount": 5
                        },
                        {
                            "id": "3",
                            "title": "Star Wars Battlefront ||",
                            "price": 19.99,
                            "inventoryCount": 5
                        },
                        {
                            "id": "4",
                            "title": "Gears of War 3",
                            "price": 9.99,
                            "inventoryCount": 0
                        }
                    ]
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(query)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_all_products_with_inventory(self):
        """ Fetch all fields for products in db with inventory greater than 0"""

        query = """
            query
            {
                allProducts(inventoryCountGt: 0)
                {
                    id
                    title
                    price
                    inventoryCount
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "allProducts": [
                        {
                            "id": "1",
                            "title": "FIFA 19",
                            "price": 29.99,
                            "inventoryCount": 5
                        },
                        {
                            "id": "2",
                            "title": "Fallout 4",
                            "price": 39.99,
                            "inventoryCount": 5
                        },
                        {
                            "id": "3",
                            "title": "Star Wars Battlefront ||",
                            "price": 19.99,
                            "inventoryCount": 5
                        }
                    ]
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(query)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_product_by_id(self):
        """ Fetch all fields for product with id 2"""

        query = """
            query
            {
                product(id: 2)
                {
                    id
                    title
                    price
                    inventoryCount
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "product": {
                        "id": "2",
                        "title": "Fallout 4",
                        "price": 39.99,
                        "inventoryCount": 5
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(query)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_product_by_title(self):
        """ Fetch all fields for product by title """

        query = """
            query
            {
                product(title: "Star Wars Battlefront ||")
                {
                    id
                    title
                    price
                    inventoryCount
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "product": {
                        "id": "3",
                        "title": "Star Wars Battlefront ||",
                        "price": 19.99,
                        "inventoryCount": 5
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(query)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

class ProductMutationTest(TestCase):
    def setUp(self):
        Product.objects.create(id=50, title="Fallout 4", price="39.99", inventory_count=5)

    def test_create_product_simple(self):
        """ Create product with all fields """

        mutation = """
            mutation
            {
                createProduct(title: "Test 1", price: 1, inventoryCount: 0)
                {
                    product
                    {
                        title
                        price
                        inventoryCount
                    }
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "createProduct": {
                        "product": {
                            "title": "Test 1",
                            "price": 1,
                            "inventoryCount": 0
                        }
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation)
        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_create_product_no_inv(self):
        """ Create product without inventory argument """

        mutation = """
            mutation
            {
                createProduct(title: "Test 2", price: 5.00000)
                {
                    product
                    {
                        title
                        price
                        inventoryCount
                    }
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "createProduct": {
                        "product": {
                            "title": "Test 2",
                            "price": 5.00,
                            "inventoryCount": 0
                        }
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation)
        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_create_product_negative_price(self):
        """ Create product using negative price argument """

        mutation = """
            mutation
            {
                createProduct(title: "Test", price: -15039242)
                {
                    product
                    {
                        title
                        price
                        inventoryCount
                    }
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "createProduct": {
                        "product": {
                            "title": "Test",
                            "price": 0,
                            "inventoryCount": 0
                        }
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation)
        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_delete_product_by_id(self):
        """ Delete product using its id """

        mutation = """
            mutation
            {
                deleteProduct(id: 50)
                {
                    message
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "deleteProduct": {
                        "message": "Product with id 50 was deleted successfully"
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation)
        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)