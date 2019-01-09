import graphene
from graphene_django import DjangoObjectType

from .models import Product


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    product = graphene.Field(ProductType, id=graphene.Int(), title=graphene.String())
    all_products = graphene.List(ProductType, inventory_count_gt=graphene.Int())

    def resolve_product(self, info, **kwargs):
        """ Query for individual product, id always takes precedence over title """

        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Product.objects.get(id=id)
        
        if title is not None:
            return Product.objects.get(title=title)

    def resolve_all_products(self, info, **kwargs):
        """ Query for all products in db, optional argument for product inventories greater than x """

        inventory_gt = kwargs.get('inventory_count_gt')
        
        if inventory_gt is not None:
            return Product.objects.all().filter(inventory_count__gt=inventory_gt)

        return Product.objects.all()