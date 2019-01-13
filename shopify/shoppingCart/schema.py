import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from products.schema import ProductType
from products.models import Product
from .models import ShoppingCart

SESSION_CART = "cartId"

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
        
        session = info.context.session

        if SESSION_CART in session:
            cartId = session.get(SESSION_CART)
            return ShoppingCart.objects.get(id=cartId)
        else:
            return None

    def resolve_all_shopping_carts(self, info, **kwargs):
        """ Query for getting all shopping carts in db """

        return ShoppingCart.objects.all()

#Mutations
class AddToCart(graphene.Mutation):
    """ Adds a product to the shopping cart by id """

    cart = graphene.Field(ShoppingCartType)

    class Arguments:
        productId = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        session = info.context.session

        if SESSION_CART in session:
            cartId = session.get(SESSION_CART)
            cart = ShoppingCart.objects.get(id=cartId)
            productId = kwargs.get("productId")

            if productId is not None:
                toAdd = Product.objects.get(id=productId)

                if toAdd is not None and toAdd.inventory_count > 0:
                    cart.items.add(toAdd)
                    cart.calcTotal()
                
            return AddToCart(cart=cart)
        else:
            return AddToCart(cart=None)

class RemoveFromCart(graphene.Mutation):
    """ Removes a product from the shopping cart by id """

    cart = graphene.Field(ShoppingCartType)

    class Arguments:
        productId = graphene.Int(required=True)

    def mutate(self, info, **kwargs):
        session = info.context.session

        if SESSION_CART in session:
            cartId = session.get(SESSION_CART)
            cart = ShoppingCart.objects.get(id=cartId)
            productId = kwargs.get("productId")

            if productId is not None:
                toRemove = Product.objects.get(id=productId)

                if toRemove is not None:
                    cart.items.remove(toRemove)  
                    cart.calcTotal()
                
            return RemoveFromCart(cart=cart)
        else:
            return RemoveFromCart(cart=None)

class CreateCart(graphene.Mutation):
    """ Creates a shopping cart with list of product ids as an optional arg """

    cart = graphene.Field(ShoppingCartType)

    class Arguments:
        items = graphene.List(graphene.Int, required=False)
    
    def mutate(self, info, **kwargs):
        session = info.context.session

        if SESSION_CART in session:
            cartId = session.get(SESSION_CART)
            cart = ShoppingCart.objects.get(id=cartId)
        else:
            cart = ShoppingCart(total=0)
            cart.save()
            session[SESSION_CART] = cart.id

            itemsList = kwargs.get("items")
            if itemsList is not None:
                for itemId in itemsList:
                    if itemId > 0:
                        product = Product.objects.get(id=itemId)
                        if product.inventory_count > 0:
                            cart.items.add(product)

                cart.calcTotal()
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
    message = graphene.String()

    class Arguments:
        pass

    def mutate(self, info, **kwargs):
        msg = ""
        session = info.context.session

        if SESSION_CART in session:
            cartId = session.get(SESSION_CART)
            cart = ShoppingCart.objects.get(id=cartId)

            if len(cart.items.all()) == 0:
                msg = "No cart items to complete"
                return SubmitCart(cart=cart, message=msg)
            else:
                for item in cart.items.all():
                    product = Product.objects.get(id=item.id)
                    if product.inventory_count > 0:
                        product.inventory_count = product.inventory_count - 1
                        product.save()
                        cart.items.remove(product)

                cart.calcTotal()
                msg = "Shopping cart was successfully completed"
                return SubmitCart(cart=cart, message=msg)
        else:
            msg = "No shopping cart to complete"
            return SubmitCart(cart=None, message=msg)

class Mutation(graphene.ObjectType):
    """ All Mutations declared in Shopping Cart API """

    create_cart = CreateCart.Field()
    delete_cart = DeleteCart.Field()
    add_to_cart = AddToCart.Field()
    remove_from_cart = RemoveFromCart.Field()
    submit_cart = SubmitCart.Field()
    

