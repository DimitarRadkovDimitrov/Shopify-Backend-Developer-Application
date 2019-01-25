# Django GraphQL Shopping Cart API

Unit tests can be found at products/tests.py and shoppingCart/tests.py. You can run all tests in the project's root with:

``` pipenv run python manage.py test -v 2 ```

## How to Run ##
<em>Note: Python 3 is required for this project</em>
1. Clone or download this repository
2. Change directory to one with Pipfile ('/shopify' - project root)
3. Install all project dependencies with pipenv

    ``` pipenv install ```
4. If you don't want to make your own products you can load pre-defined test data

    ``` pipenv run python manage.py loaddata data/sample.json```
5. Run django server

    ``` pipenv run python manage.py runserver ```
6. Go to localhost:8000/graphiql on browser to use built-in GraphQL GUI or make requests directly to localhost:8000/
<br><br>

## Use Cases ##
Below are some of the use cases this API supports. I've also included a [postman collection](./postman/GraphQL_Shopping_Cart.postman_collection.json) in the root of this project with example requests.
<br><br>

### Query for all Products ###
<em>Search all products in database</em>

![All Products Query](./images/all_products.png)
<br><br>

### Query for all Products with Available Inventory ###
<em>Search all products with inventory greater than 0</em>

![All Products with Inventory](./images/all_products_with_inventory.png)
<br><br>

### Create Empty Cart ###
<em>Create shopping cart if none in current session</em>

![Create Empty Cart](./images/create_empty_cart.png)

### Create Cart with Products ###
<em>Create shopping cart initialized with 3 items (item 3 has no inventory)</em>

![Create Cart with Items](./images/create_cart_with_items.png)
<br><br>

### Add Product to Cart ###
<em>Add product with id 1 (deep work) to shopping cart</em>

![Add to Empty Cart](./images/add_to_empty_cart.png)
<br><br>

### Add Extra Products to Cart ###
<em>Add one more product to shopping cart (clean code)</em>

![Add to Existing Cart](./images/add_to_existing_cart.png)
<br><br>

### Remove from Cart ###
<em>Remove product from shopping cart (deep work)</em>

![Remove from Cart](./images/remove_from_cart.png)
<br><br>

### Complete Cart ###
<em>Complete cart in current session</em>

![Submit Cart - 1](./images/submit_cart_1.png)

<em>Products in db after submission</em>

![Submit Cart - 2](./images/submit_cart_2.png)
<br><br>
