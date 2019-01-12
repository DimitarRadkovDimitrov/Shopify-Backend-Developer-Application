import graphene
from graphene_django import DjangoObjectType
from products.schema import ProductType
from products.models import Product
from .models import ShoppingCart

class ShoppingCartType(DjangoObjectType):
    class Meta:
        model = ShoppingCart

#Queries
class Query(graphene.ObjectType):
    """ All Queries declared in Shopping Cart API """

    shoppingCart = graphene.Field(ShoppingCartType, id=graphene.Int())
    all_shopping_carts = graphene.List(ShoppingCartType)

    def resolve_shoppingCart(self, info, **kwargs):
        """ Query for getting shopping cart by id """

        id = kwargs.get('id')
        if id is not None:
            return ShoppingCart.objects.get(id=id)

    def resolve_all_shopping_carts(self, info, **kwargs):
        """ Query for getting all shopping carts in db """

        return ShoppingCart.objects.all()

#Mutations
class AddToCart(graphene.Mutation):
    """ Adds a product to the shopping cart by id """

    cart = graphene.Field(ShoppingCartType)

    class Arguments:
        cartId = graphene.Int(required=True)
        productId = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        cartId = kwargs.get("cartId")
        productId = kwargs.get("productId")

        if productId is not None and cartId is not None:
            cart = ShoppingCart.objects.get(id=cartId)
            toAdd = Product.objects.get(id=productId)

            if toAdd is not None and toAdd.inventory_count > 0:
                cart.items.add(toAdd)
            
            cart.calcTotal()
            return AddToCart(cart=cart)

class RemoveFromCart(graphene.Mutation):
    """ Removes a product from the shopping cart by id """

    cart = graphene.Field(ShoppingCartType)

    class Arguments:
        cartId = graphene.Int(required=True)
        productId = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        cartId = kwargs.get("cartId")
        productId = kwargs.get("productId")

        if productId is not None and cartId is not None:
            cart = ShoppingCart.objects.get(id=cartId)
            toRemove = Product.objects.get(id=productId)

            if toRemove is not None:
                cart.items.remove(toRemove)  
                cart.calcTotal()

            return RemoveFromCart(cart=cart)

class CreateCart(graphene.Mutation):
    """ Creates a shopping cart with list of product ids as an optional arg """

    cart = graphene.Field(ShoppingCartType)

    class Arguments:
        items = graphene.List(graphene.Int, required=False)
    
    def mutate(self, info, **kwargs):
        cart = ShoppingCart(total=0)
        cart.save()
        itemsList = kwargs.get("items")

        if itemsList is not None:
            for itemId in itemsList:
                if itemId > 0:
                    product = Product.objects.get(id=itemId)
                    if product.inventory_count > 0:
                        cart.items.add(product)
                        cart.total = cart.total + product.price

        return CreateCart(cart=cart)        

class DeleteCart(graphene.Mutation):
    """ Deletes a cart from the db """

    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        id = kwargs.get("id")
        msg = ""

        if id is not None:
            cart = ShoppingCart.objects.get(id=id)
            if cart is not None:
                cart.delete()
                msg = f"Cart with id {id} was deleted successfully"
            else:
                msg = f"No cart with id {id}"

            return DeleteCart(message=msg)

class SubmitCart(graphene.Mutation):
    """ Completes the cart by reducing inventory and clearing cart of products """

    cart = graphene.Field(ShoppingCartType)

    class Arguments:
        cartId = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        id = kwargs.get("cartId")
        if id is not None:
            cart = ShoppingCart.objects.get(id=id)
            if cart is not None:
                for item in cart.items.all():
                    product = Product.objects.get(id=item.id)
                    if product.inventory_count > 0:
                        product.inventory_count = product.inventory_count - 1
                        product.save()
                        cart.items.remove(product)

                cart.calcTotal()  
            return SubmitCart(cart=cart)

class Mutation(graphene.ObjectType):
    """ All Mutations declared in Shopping Cart API """

    create_cart = CreateCart.Field()
    delete_cart = DeleteCart.Field()
    add_to_cart = AddToCart.Field()
    remove_from_cart = RemoveFromCart.Field()
    submit_cart = SubmitCart.Field()
    

