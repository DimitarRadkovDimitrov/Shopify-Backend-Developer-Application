import json
from collections import OrderedDict
from django.test import TestCase
from django.conf import settings
from .models import ShoppingCart
from products.models import Product
from shopify.schema import schema

SESSION_CART = "cartId"

def initTestDB():
    """ Products for test runs """

    Product.objects.create(id=1, title="FIFA 19", price="29.99", inventory_count=5)
    Product.objects.create(id=2, title="Fallout 4", price="39.99", inventory_count=5)
    Product.objects.create(id=3, title="Star Wars Battlefront ||", price="19.99", inventory_count=5)
    Product.objects.create(id=4, title="Gears of War 3", price="9.99", inventory_count=0)

def initCart(session):
    """ Cart for testing """

    cart = ShoppingCart(id=1, total=0)
    cart.save()
    session[SESSION_CART] = cart.id
    session.save()


class ShoppingCartQueryTest(TestCase):
    def setUp(self):   
        cart = ShoppingCart(id=1, total=0)
        cart.save()

        #initialize session for test
        session = self.client.session
        session[SESSION_CART] = cart.id
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

        initTestDB()

    def test_get_cart(self):
        """ Fetch empty shopping cart """

        query = """
            query
            {
                shoppingCart
                {
                    id
                    items
                    {
                        id
                        title
                        price
                    }
                    total
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "shoppingCart": {
                        "id": "1",
                        "items": [],
                        "total": 0
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(query, context_value=self.client)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_get_all_carts(self):
        """ Fetch all shopping carts in db """

        query = """
            query
            {
                allShoppingCarts
                {
                    id
                    items
                    {
                        id
                        title
                        price
                    }
                    total
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "allShoppingCarts": [
                        {
                            "id": "1",
                            "items": [],
                            "total": 0
                        }
                    ]
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(query, context_value=self.client)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

class ShoppingCartMutationTest(TestCase):
    def setUp(self):
        initTestDB()

        #initialize session for test
        session = self.client.session
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

    def test_create_cart(self):
        """ Create cart if it doesn't exist (no items) """

        mutation = """
            mutation
            {
                createCart
                {
                    cart
                    {
                        id
                        items
                        {
                            id
                            title
                            price
                        }
                        total
                    }     
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "createCart": {
                        "cart": {
                            "id": "1",
                            "items": [],
                            "total": 0
                        }
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation, context_value=self.client)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_create_cart_with_items(self):
        """ Create cart if it doesn't exist with list of items """

        mutation = """
            mutation
            {
                createCart(items: [1, 2, 3, 4])
                {
                    cart
                    {
                        id
                        items
                        {
                            id
                            title
                            price
                            inventoryCount
                        }
                        total
                    }     
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "createCart": {
                        "cart": {
                            "id": "1",
                            "items": [
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
                            ],
                            "total": 89.97
                        }
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation, context_value=self.client)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_add_to_cart(self):
        """ Add item to empty cart """

        initCart(self.client.session)

        mutation = """
            mutation
            {
                addToCart(productId: 1)
                {
                    cart
                    {
                        id
                        items
                        {
                            id
                            title
                            price
                            inventoryCount
                        }
                        total
                    }     
                }
            }
        """
        expected_result = """
            {
                "data": {
                    "addToCart": {
                        "cart": {
                            "id": "1",
                            "items": [
                                {
                                    "id": "1",
                                    "title": "FIFA 19",
                                    "price": 29.99,
                                    "inventoryCount": 5
                                }
                            ],
                            "total": 29.99
                        }
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation, context_value=self.client)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)
    
    def test_add_to_cart_multiple(self):
        """ Add 2 consecutive items to empty cart """

        initCart(self.client.session)

        mutation1 = """
            mutation
            {
                addToCart(productId: 1)
                {
                    cart
                    {
                        id
                        items
                        {
                            id
                            title
                            price
                            inventoryCount
                        }
                        total
                    }     
                }
            }
        """

        mutation2 = """
            mutation
            {
                addToCart(productId: 2)
                {
                    cart
                    {
                        id
                        items
                        {
                            id
                            title
                            price
                            inventoryCount
                        }
                        total
                    }     
                }
            }
        """
        actual_result = schema.execute(mutation1, context_value=self.client)
        actual_result = schema.execute(mutation2, context_value=self.client)

        expected_result = """
            {
                "data": {
                    "addToCart": {
                        "cart": {
                            "id": "1",
                            "items": [
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
                                }
                            ],
                            "total": 69.98
                        }
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_remove_from_cart(self):
        """ Remove item from cart, leaving it empty """

        initCart(self.client.session)

        #adding item 3 as product to remove
        cartId = self.client.session[SESSION_CART]
        cart = ShoppingCart.objects.get(id=cartId)
        product = Product.objects.get(id=3)
        cart.items.add(product)

        mutation = """
            mutation
            {
                removeFromCart(productId: 3)
                {
                    cart
                    {
                        id
                        items
                        {
                            id
                            title
                            price
                            inventoryCount
                        }
                        total
                    }     
                }
            }
        """

        expected_result = """
            {
                "data": {
                    "removeFromCart": {
                        "cart": {
                            "id": "1",
                            "items": [],                            
                            "total": 0
                        }
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation, context_value=self.client)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_delete_cart(self):
        """ Delete cart from db """

        initCart(self.client.session)

        mutation = """
            mutation
            {
                deleteCart(id: 1)
                {
                    message  
                }
            }
        """

        expected_result = """
            {
                "data": {
                    "deleteCart": {
                        "message": "Cart with id 1 was deleted successfully"
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation, context_value=self.client)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)

    def test_submit_cart(self):
        """ Submit current cart """

        initCart(self.client.session)

        #adding first 3 as test
        cartId = self.client.session[SESSION_CART]
        cart = ShoppingCart.objects.get(id=cartId)
        for i in range(1, 4):
            product = Product.objects.get(id=i)
            cart.items.add(product)

        mutation = """
            mutation
            {
                submitCart
                {
                    cart 
                    {
                        id
                        items
                        {
                            id
                            title
                            price
                            inventoryCount
                        }
                        total
                    }
                    message  
                }
            }
        """

        expected_result = """
            {
                "data": {
                    "submitCart": {
                        "cart": {
                            "id": "1",
                            "items": [],                            
                            "total": 0
                        },
                        "message": "Shopping cart was successfully completed"
                    }
                }
            }
        """

        expected_result = json.loads(expected_result, object_pairs_hook=OrderedDict).get("data")
        actual_result = schema.execute(mutation, context_value=self.client)

        self.assertNotEqual(actual_result.errors, True)
        self.assertEqual(actual_result.data, expected_result)