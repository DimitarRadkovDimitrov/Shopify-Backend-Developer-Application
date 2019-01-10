import graphene
from graphene_django import DjangoObjectType

from .models import ShoppingCart


class ShoppingCartType(DjangoObjectType):
    class Meta:
        model = ShoppingCart


class Query(graphene.ObjectType):
    shoppingCart = graphene.Field(ShoppingCartType, id=graphene.Int())

    def resolve_shoppingCart(self, info, **kwargs):
        """ Query for shopping cart product by id """

        id = kwargs.get('id')

        if id is not None:
            return ShoppingCart.objects.get(id=id)