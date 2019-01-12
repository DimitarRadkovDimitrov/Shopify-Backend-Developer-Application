import graphene

import products.schema
import shoppingCart.schema

class Query(products.schema.Query, shoppingCart.schema.Query, graphene.ObjectType):
    """ All Queries in GraphQL schema """
    pass

class Mutation(products.schema.Mutation, shoppingCart.schema.Mutation, graphene.ObjectType):
    """ All Mutations in GraphQL schema """
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)