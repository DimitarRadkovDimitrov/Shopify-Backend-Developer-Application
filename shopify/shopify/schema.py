import graphene

import products.schema
import shoppingCart.schema

class Query(products.schema.Query, shoppingCart.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)