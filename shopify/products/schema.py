import sys
import graphene
from graphql import GraphQLError
from django.db import IntegrityError
from graphene_django import DjangoObjectType
from .models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

#Queries
class Query(graphene.ObjectType):
    """ All Queries declared in Products API """

    product = graphene.Field(ProductType, id=graphene.Int(), title=graphene.String())
    all_products = graphene.List(ProductType, inventory_count_gt=graphene.Int())

    def resolve_product(self, info, **kwargs):
        """ Query for getting product by id, id takes precedence over title """

        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Product.objects.get(id=id)
        
        if title is not None:
            return Product.objects.get(title=title)

    def resolve_all_products(self, info, **kwargs):
        """ Query for getting all products in db, optional argument for product inventories greater than x """

        inventory_gt = kwargs.get('inventory_count_gt')
        
        if inventory_gt is not None:
            return Product.objects.all().filter(inventory_count__gt=inventory_gt)

        return Product.objects.all()

#Mutations
class CreateProduct(graphene.Mutation):
    """ Creates a product in db """

    product = graphene.Field(ProductType)

    class Arguments: 
        title = graphene.String(required=True)
        price = graphene.Float(required=True)
        inventory_count = graphene.Int(required=False)

    def mutate(self, info, **kwargs):    
        title = kwargs.get('title')
        price = kwargs.get('price')
        inventory_count = kwargs.get('inventory_count')

        if inventory_count is None or inventory_count < 0:
            inventory_count = 0

        if price is None or price < 0:
            price = 0.00
        
        try:
            product = Product(title=title, price=price, inventory_count=inventory_count)
            product.save()
            return CreateProduct(product=product)
        except IntegrityError as e:
            sys.stderr.write(e.args[0])
            raise GraphQLError(message=e.args[0])
     
        return CreateProduct(product=None)
        
class DeleteProduct(graphene.Mutation):
    """ Delete product from db by id """

    message = graphene.String()

    class Arguments: 
        id = graphene.Int(required=True)

    def mutate(self, info, **kwargs):    
        id = kwargs.get('id')
        msg = ""

        if id is not None:
            product = Product.objects.get(id=id)

            if product is not None:
                product.delete()
                msg = f"Product with id {id} was deleted successfully"
            else:
                msg = f"No product with id {id}"
            return DeleteProduct(message=msg)

class Mutation(graphene.ObjectType):
    """ All Mutations declared in Products API """
    
    create_product = CreateProduct.Field()       
    delete_product = DeleteProduct.Field() 

