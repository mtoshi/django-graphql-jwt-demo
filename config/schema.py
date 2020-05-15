# -*- coding: utf-8 -*-
"""config.schema"""

import graphene
import users.schema


# Query for getting the data from the server.
# class Query(graphene.ObjectType):
#     pass


# Mutation for sending the data to the server.
class Mutation(users.schema.Mutation, graphene.ObjectType):
    pass


# Create schema
# schema = graphene.Schema(query=Query, mutation=Mutation)
schema = graphene.Schema(mutation=Mutation)
