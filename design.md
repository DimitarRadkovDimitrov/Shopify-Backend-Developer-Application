# Design #

## Django ##
I used the Django framework to build this project. It seemed like the perfect candidate as it was quick to set up with a database, object relational mapper, and graphQL. 

I did find that there was a lack of documentation specifically in the django-graphql area which made development take much longer.

I didn't end up using any of django's authentication features since users should be able to buy products without having to log in (checkout as guest).

### Documentation ###
For documentation I used python docstrings. These are similar to javadoc comments which can be used to generate documentation.

### Unit Testing ###
I used Django's test framework to test the essential functionality of this app. You can find instructions on how to run these in my [README](./README.md).

### Products ###
For products I made a model in django with the required fields and used an id as the primary key with auto_incrementing so the client didn't have to pass in an id parameter everytime they wanted to create a product.

Titles for products were made unique since there can be multiple products with the same name (inventory count > 1).

In django you can make a decimal field which rounds up to the decimal places you specify so I specified 2 for price.

Products have mutations for creating and deleting and handle incorrect values like a negative price or inventory value.

Products also have queries for fetching from the database. For simplicity, there is one to fetch product by id or title and another for all products with an optional parameter for inventory count.

### Shopping Cart ###
I decided to make a model for shopping cart as well. This made sense to me because I could specify the items field as a list of products, making adding and remove products simple.

Because we don't want multiple carts per user, I needed a way to limit the amount of shopping carts created per user. Each session is unique to the current user so I store the user's cart (by id) in their session.

Because we can't control what happens when a session ends, I'll have to run something at regular intervals to purge the expired sessions and delete the old shopping carts. But this is outside the scope of this assignment.
